from common import math, np, plt, QPSK, dB2Linear, randn_c

def run_qpsk_transmission(
    num_symbols: int = 1000,
    snr_db: float = 100.0,
) -> float:
    """
    QPSK를 이용한 전송 구현 함수로,
    QPSK는 한 symbol에 2비트를 실어 보내는 디지털 변조 방식.

    """
    qpsk = QPSK()
    
    data_qpsk = np.random.randint(0, qpsk.M, size=num_symbols)
    modulated_data_qpsk = qpsk.modulate(data_qpsk)

    snr_linear = dB2Linear(snr_db)
    noise_power = 1 / snr_linear

    # noise vector
    n = math.sqrt(noise_power) * randn_c(num_symbols)
    received_data_qpsk = modulated_data_qpsk + n

    # received data
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(received_data_qpsk.real, received_data_qpsk.imag, "*")
    ax.axis("equal")
    ax.set_title(f"Received QPSK symbols (SNR={snr_db} dB)")

    plt.savefig("QPSK_modulation_received.png")
    print("QPSK_modulation_received.png 파일이 저장되었습니다.")

    demodulated_data_qpsk = qpsk.demodulate(received_data_qpsk)
    symbol_error_rate_qpsk = 1 - (
        (demodulated_data_qpsk == data_qpsk).sum() / demodulated_data_qpsk.size
    )

    print("Error QPSK:", symbol_error_rate_qpsk)
    return symbol_error_rate_qpsk