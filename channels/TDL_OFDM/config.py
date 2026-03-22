from dataclasses import dataclass

@dataclass
class TDLOFDMConfig:
    M: int = 16                 # size of the modulation constellation
    noise_var: float = 1e-3
    bandwidth: float = 5e6      # in hertz
    Fd: float = 10.0            # Doppler frequency (in Hz)

    # OFDM에는 전체 FFT 크기(fft_size)만큼 주파수 bin이 생김
    # 또, 이를 전부 데이터용으로 쓰지는 않고 일부는 DC 성분, 양 끝 보호 대역 같은 용도로 비워두거나 따로 씀
    # 따라서, 실제 데이터에 쓰는 subcarrier 수만 따로 정하는 것이 num_used_subcarriers
    fft_size: int = 1024
    num_used_subcarriers: int = 600 # 실제로 데이터 전송에 사용하는 subcarrier 개수

    # OFDM에는 한 번에 한 개의 OFDM symbol만 보내는 게 아니라, 보통 여러 symbol이 연속으로 감
    # 또한 multipath 때문에 ISI가 생길 수 있어, 각 symbol 앞에 원래 신호의 뒷부분을 잘라서 붙임. 이게 CP
    num_ofdm_symbols: int = 10
    cp_size: int = 10

    @property
    def Ts(self) -> float:
        return 1.0 / self.bandwidth
    
    @property
    def num_symbols(self) -> float:
        return self.num_ofdm_symbols * self.num_used_subcarriers