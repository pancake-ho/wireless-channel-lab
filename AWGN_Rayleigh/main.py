import numpy as np

from rayleigh_qam_simulator import RayleighOrAWGNSimulator
from visualization import plot_constellations, extract_ser, plot_ser

# 병렬 사용할 때 대비
USE_PARALLEL = True
if USE_PARALLEL:
    from run_parallel import get_parallel_view


def run_simulation():
    """
    BPSK/다중 QAM 변조를 AWGN 채널과 Rayleigh Fading 채널에서 돌려서 SER을 비교하는 함수
    다음과 같은 과정으로 수행됨.

    1) BPSK, QAM의 constellations 점들을 시각화
    2) Rayleigh용과 AWGN용으로 각각 Eb/N0 구간을 -5dB부터 30dB까지 8개 점으로 만듦
    """
    plot_constellations()


    EbN0_db_rayleigh = np.linspace(-5, 30, 8)
    EbN0_db_awgn = np.linspace(-5, 30, 8)

    runner_rayleigh = RayleighOrAWGNSimulator(
        EbN0_db_rayleigh,
        simulate_with_rayleigh=True,
    )
    runner_rayleigh.set_results_filename("results/qam_rayleigh")

    runner_awgn = RayleighOrAWGNSimulator(
        EbN0_db_awgn,
        simulate_with_rayleigh=False,
    )
    runner_awgn.set_results_filename("results/qam_awgn")

    if USE_PARALLEL:
        lview = get_parallel_view()
        runner_rayleigh.simulate_in_parallel(lview)
        runner_awgn.simulate_in_parallel(lview)
    else:
        runner_rayleigh.simulate()
        runner_awgn.simulate()
    
    print("Rayleigh elapsed:", runner_rayleigh.elapsed_time)
    print("AWGN elaped:", runner_awgn.elapsed_time)

    ser_rayleigh = extract_ser(runner_rayleigh)
    ser_awgn = extract_ser(runner_awgn)

    print("SER Rayleigh:", ser_rayleigh)
    print("SER AWGN", ser_awgn)

    plot_ser(EbN0_db_rayleigh, ser_rayleigh, EbN0_db_awgn, ser_awgn)


if __name__ == "__main__":
    run_simulation()