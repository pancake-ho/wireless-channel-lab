from common import np, plt, QPSK, pretty_time
from visualization import plot_constellation
from qpsk_trasmission import run_qpsk_transmission
from simulate_awgn import demo_simulate_awgn
from simulators import AWGNSimulator, AWGNSimulator2

def run_awgn_simulator_demo():
    qpsk = QPSK()
    snr_db = np.linspace(-5, 15, 9)

    runner = AWGNSimulator(snr_db)
    print(runner.params)

    runner.simulate()

    print("Symbol Error Rate:\n", np.array(runner.results.get_result_values_list("symbol_error_rate")))
    elapsed_times = runner.results.get_result_values_list("elapsed_time")
    print("\nElapsed times:\n", np.array(elapsed_times))
    print(f"\nTotal elapsed time: {pretty_time(sum(elapsed_times))}")

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.semilogy(snr_db, qpsk.calcTheoreticalSER(snr_db), "--", label="Theoretical")
    ax.semilogy(
        snr_db,
        runner.results.get_result_values_list("symbol_error_rate"),
        label="Simulated",
    )
    ax.set_title("QPSK Symbol Error Rate (AWGN channel)")
    ax.set_ylabel("Symbol Error Rate")
    ax.set_xlabel("SNR (dB)")
    ax.legend()
    plt.show()


def run_awgn_simulator2_demo():
    qpsk = QPSK()
    snr_db = np.linspace(-5, 15, 9)

    runner2 = AWGNSimulator2(snr_db)
    runner2.set_results_filename("results_qpsk_awgn")
    runner2.simulate()

    print(runner2.results.get_result_names())
    print(runner2.results["elapsed_time"])
    print(runner2.results.get_result_values_list("elapsed_time"))
    print(runner2.results.get_result_values_confidence_intervals("symbol_error_rate"))

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.semilogy(snr_db, qpsk.calcTheoreticalSER(snr_db), "--", label="Theoretical")
    ax.semilogy(
        snr_db,
        runner2.results.get_result_values_list("symbol_error_rate"),
        label="Simulated",
    )
    ax.set_title("QPSK Symbol Error Rate (AWGN channel)")
    ax.set_ylabel("Symbol Error Rate")
    ax.set_xlabel("SNR (dB)")
    ax.legend()
    plt.show()


def main():
    print("[1] Plotting constellations...")
    plot_constellation()

    print("[2] Running single QPSK transmission example...")
    run_qpsk_transmission()

    print("[3] Running AWGN function demo...")
    demo_simulate_awgn()

    print("[4] Running AWGN simulator demo...")
    run_awgn_simulator_demo()

    print("[5] Running AWGN simulator2 demo...")
    run_awgn_simulator2_demo()



if __name__ == "__main__":
    main()