import numpy as np
import matplotlib.pyplot as plt
from pyphysim.modulators.fundamental import BPSK, QAM
from pyphysim.util.conversion import linear2dB


def plot_constellations():
    bpsk = BPSK()
    qam4 = QAM(4)
    qam16 = QAM(16)
    qam64 = QAM(64)
    qam256 = QAM(256)

    fig_bpsk, ax_bpsk = plt.subplots(figsize=(4, 4))
    ax_bpsk.set_title("BPSK")
    ax_bpsk.plot(bpsk.symbols.real, bpsk.symbols.imag, "*r")
    ax_bpsk.axis("equal")

    fig, axes = plt.subplots(figsize=(8, 8), nrows=2, ncols=2)
    ax11, ax12 = axes[0]
    ax21, ax22 = axes[1]

    ax11.set_title("4-QAM")
    ax11.plot(qam4.symbols.real, qam4.symbols.imag, "*r")
    ax11.axis("equal")

    ax12.set_title("16-QAM")
    ax12.plot(qam16.symbols.real, qam16.symbols.imag, "*r")
    ax12.axis("equal")

    ax21.set_title("64-QAM")
    ax21.plot(qam64.symbols.real, qam64.symbols.imag, "*r")
    ax21.axis("equal")

    ax22.set_title("256-QAM")
    ax22.plot(qam256.symbols.real, qam256.symbols.imag, "*r")
    ax22.axis("equal")

    plt.tight_layout()
    plt.show()


def extract_ser(runner):
    return {
        2: runner.results.get_result_values_list("symbol_error_rate", fixed_params={"M": 2}),
        4: runner.results.get_result_values_list("symbol_error_rate", fixed_params={"M": 4}),
        16: runner.results.get_result_values_list("symbol_error_rate", fixed_params={"M": 16}),
        64: runner.results.get_result_values_list("symbol_error_rate", fixed_params={"M": 64}),
        256: runner.results.get_result_values_list("symbol_error_rate", fixed_params={"M": 256}),
    }


def plot_ser(EbN0_db_rayleigh, ser_rayleigh, EbN0_db_awgn, ser_awgn):
    fig, (ax1, ax2) = plt.subplots(figsize=(15, 6), ncols=2)

    colors = {2: "red", 4: "orange", 16: "blue", 64: "lightgreen", 256: "magenta"}

    for M, values in ser_rayleigh.items():
        label = "BPSK Simulation" if M == 2 else f"{M}-QAM Simulation"
        ax1.semilogy(EbN0_db_rayleigh, values, "-", color=colors[M], label=label)
    
    ax1.set_title("Symbol Error Rate (Rayleigh Channel)")
    ax1.set_ylabel("Symbol Error Rate")
    ax1.set_xlabel("EbN0 (dB)")
    ax1.grid(True, which="both")
    ax1.set_ylim((1e-4, 1e0))
    ax1.legend()

    ax2.semilogy(EbN0_db_awgn, ser_awgn[2], "o", color="red", label="BPSK Simulation")
    ax2.semilogy(EbN0_db_awgn, BPSK().calcTheoreticalSER(EbN0_db_awgn),
                 color="red", label="BPSK Theory")
    
    for M in [4, 16, 64, 256]:
        ax2.semilogy(EbN0_db_awgn, ser_awgn[M], "o", colors=colors[M], label=f"{M}-QAM Simulation")
        ax2.semilogy(
            EbN0_db_awgn,
            QAM(M).calcTheoreticalSER(EbN0_db_awgn + linear2dB(np.log2(M))),
            colors=colors[M],
            label=f"{M}-QAM Theory",
        )

    ax2.set_title("Symbol Error Rate (AWGN channel)")
    ax2.set_ylabel("Symbol Error Rate")
    ax2.set_xlabel("EbN0 (dB)")
    ax2.grid(True, which="both")
    ax2.set_ylim((1e-5, 1e0))
    ax2.legend()

    plt.tight_layout()
    plt.show()