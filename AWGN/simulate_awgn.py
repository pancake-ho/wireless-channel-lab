from common import math, np, Modulator, dB2Linear, randn_c, QPSK


def simulate_awgn(
    modulator: Modulator,
    num_symbols: int,
    noise_power: float,
    num_reps: int,
) -> float:
    """
    symbol error rate를 반환하는 함수
    """
    symbol_error_rate = 0.0
    for _ in range(num_reps):
        data = np.random.randint(0, modulator.M, size=num_symbols)
        modulated_data = modulator.modulate(data)

        # noise vector
        n = math.sqrt(noise_power) * randn_c(num_symbols)

        # received_data_qam
        received_data = modulated_data + n

        demodulated_data = modulator.demodulate(received_data)
        symbol_error_rate += 1 - (
            (demodulated_data == data).sum()/ demodulated_data.size
        )
    
    return symbol_error_rate / num_reps


def demo_simulate_awgn() -> None:
    qpsk = QPSK()
    num_symbols = int(1e3)

    snr_db = 5
    snr_linear = dB2Linear(snr_db)
    noise_power = 1 / snr_linear

    symbol_error1 = simulate_awgn(qpsk, num_symbols, noise_power, num_reps=5000)
    symbol_error2 = simulate_awgn(qpsk, num_symbols, noise_power, num_reps=5000)

    print(f"Obtained symbol error for SNR {snr_db}: {symbol_error1}")
    print(f"Obtained symbol error for SNR {snr_db}: {symbol_error2}")
    print(f"\nTheoretical symbol error for SNR {snr_db}: {qpsk.calcTheoreticalSER(snr_db)}")