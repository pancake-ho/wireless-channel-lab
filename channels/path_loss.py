import numpy as np
import matplotlib.pyplot as plt
from pyphysim.channels import pathloss


def main() -> None:
    # path loss model objects
    pl_general = pathloss.PathLossGeneral(n=3.7, C=120)
    pl_general.handle_small_distances_bool = True

    pl_3gpp = pathloss.PathLoss3GPP1()
    pl_3gpp.handle_small_distances_bool = True
    
    pl_fs = pathloss.PathLossFreeSpace()
    pl_fs.n = 2
    pl_fs.fc = 900
    pl_fs.handle_small_distances_bool = True

    # distance range in km
    d = np.linspace(0.01, 0.5, 100)

    # plot
    fig, ax = plt.subplots()

    pl_general.plot_deterministic_path_loss_in_dB(
        d,
        ax,
        extra_args={"label": "General"},
    )
    pl_fs.plot_deterministic_path_loss_in_dB(
        d,
        ax,
        extra_args={"label": "Free Space"},
    )
    pl_3gpp.plot_deterministic_path_loss_in_dB(
        d,
        ax,
        extra_args={"label": "3GPP"},
    )

    ax.grid()
    ax.set_ylabel("Path Loss (in dB)")
    ax.set_xlabel("Distance (in Km)")
    ax.legend(loc=5)

    plt.show()


if __name__ == "__main__":
    main()