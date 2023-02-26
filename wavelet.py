import torch


def Gaussian_Wave_Packet(k, sigma, miu, x):
    # k = torch.tensor([k])
    # sigma = torch.tensor([sigma])
    # miu = torch.tensor([miu])
    envelope = torch.exp(-((x - miu) ** 2) / (2 * sigma**2))
    oscillate = torch.exp(
        1j * k * (x - miu)
    )  # planner wave traveling in the positive x direction
    wavelet = envelope * oscillate
    return wavelet


class GaussianPacket:
    """
    1d: https://zhuanlan.zhihu.com/p/343847938
        https://zhuanlan.zhihu.com/p/608469189
    """

    def __init__(self) -> None:
        pass

    def dimension_1(k, sigma, miu, x):
        k = torch.tensor([k])
        sigma = torch.tensor([sigma])
        miu = torch.tensor([miu])

        wave = torch.exp(-((x - miu) ** 2) / (2 * sigma**2)) * torch.exp(1j * k * x)
        wave = wave / wave.norm(p=1)  # L1范数 = wave.abs().sum()
        return wave


if __name__ == "__main__":
    import matplotlib.pyplot as plt
