import torch

class CrankNicolson:

    def __init__(self, tStep, xStep, vNodes):
        self.dt = tStep
        self.dx = xStep
        self.Nx = vNodes.numel() # 待求解点不包括边界端点
        self.Vx = vNodes # 位势不含时 V=V(x)
        self.rx = 1j * self.dt / (2 * self.dx**2) # 离散格式中的重要常数

    def now_mat(self):
        """
        now @ t0  注意：Vx是排除边界端点的
        """
        shift_arr = torch.ones(self.Nx - 1) * self.rx
        diag_arr = torch.ones(self.Nx) * (2 - 2 * self.rx) - 1j * self.dt * self.Vx
        fMat = torch.diag(shift_arr, -1) + torch.diag(diag_arr) + torch.diag(shift_arr, 1)
        return fMat

    def next_mat(self):
        """
        next @ t1  注意：Vx是排除边界端点的
        """
        shift_arr = torch.ones(self.Nx - 1) * (-self.rx)
        diag_arr = torch.ones(self.Nx) * (2 + 2 * self.rx) + 1j * self.dt * self.Vx
        bMat = torch.diag(shift_arr, -1) + torch.diag(diag_arr) + torch.diag(shift_arr, 1)
        return bMat
