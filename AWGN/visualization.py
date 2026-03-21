from common import plt, BPSK, QAM, QPSK


def plot_constellation() -> None:
    qpsk = QPSK()
    bpsk = BPSK()
    qam16 = QAM(16)
    qam64 = QAM(64)

    fig, [[ax11, ax12], [ax21, ax22]] = plt.subplots(figsize=(10, 10),
                                                     nrows=2,
                                                     ncols=2,)
    
    ax11.set_title("BPSK")
    ax11.plot(bpsk.symbols.real, bpsk.symbols.imag, "*r", label="BPSK")
    ax11.axis("equal")
    
    ax12.set_title("QPSK")
    ax12.plot(qpsk.symbols.real, qpsk.symbols.imag, "*r", label="QPSK")
    ax12.axis("equal")
    
    ax21.set_title("16-QAM")
    ax21.plot(qam16.symbols.real, qam16.symbols.imag, "*r", label="16-QAM")
    ax21.axis("equal")
    
    ax22.set_title("64-QAM")
    ax22.plot(qam64.symbols.real, qam64.symbols.imag, "*r", label="64-QAM")
    ax22.axis("equal")

    plt.tight_layout()
    plt.savefig("awgn_constellation.png")
    print("awgn_constellation.png 파일이 저장되었습니다.")