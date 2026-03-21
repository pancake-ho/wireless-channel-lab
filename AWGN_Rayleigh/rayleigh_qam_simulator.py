import math
import numpy as np

from pyphysim.modulators.fundamental import BPSK, QAM
from pyphysim.simulations import Result, SimulationResults, SimulationRunner
from pyphysim.util.conversion import dB2Linear
from pyphysim.util.misc import randn_c, count_bit_errors


class RayleighOrAWGNSimulator(SimulationRunner):
    def __init__(self, SINR_dB_values, simulate_with_rayleigh=False):
        super().__init__()

        self._simulate_with_rayleigh = simulate_with_rayleigh

        self.params.add('EbN0_db', SINR_dB_values) # 비트당 SNR
        self.params.set_unpack_parameter('EbN0_db')

        self.params.add("M", [2, 4, 16, 64, 256])
        self.params.set_unpack_parameter("M")
        
        self.rep_max = 50000
        self.num_symbols = 1000
        self.max_symbol_errors = 1. / 300. * self.num_symbols * self.rep_max

        self.progressbar_message = (
            f"Simulating for {self.params.get_num_unpacked_variations()} configurations"
        )
        self.update_progress_function_style = "text1"

    def _keep_going(self, current_params, current_sim_results, current_rep):
        cumulated_symbol_errors = current_sim_results['symbol_errors'][-1].get_result()
        return cumulated_symbol_errors < self.max_symbol_errors
    
    def _run_simulation(self, current_parameters):
        sinr_dB = current_parameters['EbN0_db']
        M = current_parameters['M']

        modulator = BPSK() if M == 2 else QAM(M)

        EbN0_linear = dB2Linear(sinr_dB)
        snr_linear = EbN0_linear * math.log2(M)
        noise_power = 1 / snr_linear

        data = np.random.randint(0, modulator.M, size=self.num_symbols)
        modulated_data = modulator.modulate(data)

        n = math.sqrt(noise_power) * randn_c(self.num_symbols)

        if self._simulate_with_rayleigh:
            h = randn_c(modulated_data.size)
            received_data = h * modulated_data + n
            received_data /= h
        else:
            received_data = modulated_data + n
        
        demodulated_data = modulator.demodulate(received_data)
        symbol_errors = np.sum(demodulated_data != data)
        num_bit_errors = count_bit_errors(data, demodulated_data)

        results = SimulationResults()
        results.add_new_result("symbol_errors", Result.SUMTYPE, symbol_errors)
        results.add_new_result(
            "symbol_error_rate",
            Result.RATIOTYPE,
            value=symbol_errors,
            total=self.num_symbols,
        )
        results.add_new_result("bit_errors", Result.SUMTYPE, num_bit_errors)

        return results