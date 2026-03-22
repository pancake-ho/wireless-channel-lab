import numpy as np
from pyphysim.modulators import OFDM, QAM


def create_modem_objects(cfg):
    qam = QAM(cfg.M)
    ofdm = OFDM(cfg.fft_size, cfg.cp_size, cfg.num_used_subcarriers)
    return qam, ofdm


def generate_random_data(cfg):
    return np.random.randint(0, cfg.M, cfg.num_symbols)


def tx_chain(data, qam, ofdm):
    qam_symbols = qam.modulate(data)
    ofdm_symbols = ofdm.modulate(data)
    return qam_symbols, ofdm_symbols