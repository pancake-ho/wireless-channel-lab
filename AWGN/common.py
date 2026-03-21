import math

import numpy as np
import matplotlib.pyplot as plt

from pyphysim.modulators.fundamental import BPSK, QAM, QPSK, Modulator
from pyphysim.simulations import Result, SimulationResults, SimulationRunner
from pyphysim.util.conversion import dB2Linear
from pyphysim.util.misc import pretty_time, randn_c

np.set_printoptions(precision=2, linewidth=120)