from common import (
    math,
    np,
    QPSK,
    Result,
    SimulationResults,
    SimulationRunner,
    dB2Linear,
    randn_c,
)


class AWGNSimulator(SimulationRunner):
    def __init__(self, sinr_db_values):
        super().__init__()

        # 'params' attribute에 simulation parameters 추가
        self.params.add("SNR_db", sinr_db_values)

        # SNR_db를 "unpacked" 로 정의해야 함
        # 파라미터 스윕할 때 리스트 전체로 한 번에 넘어가는 게 아닌, 하나씩 꺼내서 시뮬레이션 여러 번 돌리라는 뜻
        self.params.set_unpack_parameter("SNR_db")

        self.rep_max = 500
        self.modulator = QPSK()

    def _run_simulation(self, current_parameters):
        sinr_db = current_parameters["SNR_db"]
        num_symbols = 1000

        snr_linear = dB2Linear(sinr_db)
        noise_power = 1 / snr_linear

        data = np.random.randint(0, self.modulator.M, size=num_symbols)
        modulated_data = self.modulator.modulate(data)

        n = math.sqrt(noise_power) * randn_c(num_symbols)
        received_data = modulated_data + n

        demodulated_data = self.modulator.demodulate(received_data)
        symbol_errors = (demodulated_data != data).sum()

        sim_results = SimulationResults()
        sim_results.add_new_result(
            "symbol_error_rate",
            Result.RATIOTYPE, # 결과는 ratio(비율) 타입 / 분자는 symbol_errors, 분모는 num_symbols
            value=symbol_errors, # 분자는 에러 개수
            total=num_symbols, # 분모는 전체 심볼 개수
        )
        return sim_results
    

class AWGNSimulator2(SimulationRunner):
    def __init__(self, sinr_db_values):
        super().__init__()

        self.params.add("SNR_db", sinr_db_values)
        self.params.set_unpack_parameter("SNR_db")

        self.rep_max = 50000
        self.num_symbols = 1000
        self.max_symbol_errors = 1.0 / 1000.0 * self.num_symbols * self.rep_max

        self.modulator = QPSK()
        self.progressbar_message = "Simulating for SNR {SNR_db}"
        self.update_progress_function_style = "ipython"
    
    def _keep_going(self, current_params, current_sim_results, current_rep):
        cumulated_symbol_errors = current_sim_results["symbol_errors"][-1].get_result()
        return cumulated_symbol_errors < self.max_symbol_errors
    
    def _run_simulation(self, current_parameters):
        sinr_db = current_parameters["SNR_db"]

        snr_linear = dB2Linear(sinr_db)
        noise_power = 1 / snr_linear

        data = np.random.randint(0, self.modulator.M, size=self.num_symbols)
        modulated_data = self.modulator.modulate(data)

        n = math.sqrt(noise_power) * randn_c(self.num_symbols)
        received_data = modulated_data + n

        demodulated_data = self.modulator.demodulate(received_data)
        symbol_errors = (demodulated_data != data).sum()

        sim_results = SimulationResults()
        sim_results.add_new_result(
            "symbol_error_rate",
            Result.RATIOTYPE,
            value=symbol_errors,
            total=self.num_symbols,
        )
        sim_results.add_new_result(
            "symbol_errors",
            Result.SUMTYPE,
            value=symbol_errors,
        )
        return sim_results