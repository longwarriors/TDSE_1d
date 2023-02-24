# -*- coding: utf-8 -*-
# @Author: Zhangxiaoxu
# @Date:   2023-02-24 10:19:41
# @Last Modified by:   longwarriors
# @Last Modified time: 2023-02-24 18:03:06
import torch
from torch import tensor
import matplotlib.pyplot as plt
from celluloid import Camera
from potential import barrier, well
from wavelet import Gaussian_Wave_Packet
from solver import CrankNicolson

engine = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
plt.style.use(["science", "notebook", "grid"])

def scene():
    dt = 0.005
    ts = 80 # time steps 0, 1, 2, ..., t
    dx = 0.001
    xNodes = torch.arange(start=0, end=3, step=dx) # x轴格点
    Nx = xNodes.numel()
    potent_dist = barrier(start=1.5, end=1.6, height=3000, xNodes=xNodes) # x轴势能分布

    # construct coefficient matrix
    fdm = CrankNicolson(dt, dx, potent_dist[1:-1]) # finite difference method
    lhs = fdm.next_mat()
    rhs = fdm.now_mat()

    # initial condition
    sigma, miu = 0.1, 0.7
    init_wave = Gaussian_Wave_Packet(k=100, sigma=sigma, miu=miu, x=xNodes)
    init_wave = torch.where((xNodes < miu + 3*sigma) & (xNodes > miu - 3*sigma), init_wave, 0.0) # 只取 μ ± 3σ 区间
    init_wave = init_wave / init_wave.norm(p=1) # normalized probability L1范数 = psi.abs().sum()

    # evolving points
    iter_wave = init_wave[1:-1]

    # solve linear eqs
    sol_mat = torch.linalg.inv(lhs) @ rhs
    for t in range(ts):
        iter_wave = sol_mat @ iter_wave # iter_wave = torch.matrix_power(sol_mat, ts) @ iter_wave
    result = torch.nn.functional.pad(iter_wave, (1, 1), mode="constant", value=0)

    # 画图演示
    fig = plt.figure(num="Evolving process", figsize=(8, 3)) # 创建画板，num是画板编号int or str
    fig.set_tight_layout(True) # 紧凑组排
    fig.text(x=0.0, y=1.0, s="Designed by longwarriors", style='italic', fontsize=8, color="red")
    ax1 = plt.subplot(1, 1, 1)
    ax1.plot(xNodes, potent_dist, "black")
    ax1.plot(xNodes, result.abs(), label=f"$|\psi_{{{t}}}|^2$"+"={:.2f}".format(result.norm(p=1)))
    ax1.plot(xNodes, result.real, animated=True)
    ax1.plot(xNodes, result.imag, animated=True)
    ax1.set_ylim(bottom=-0.005, top=0.005)
    ax1.legend()
    # ax1.plot(xNodes, init_wave.abs(), label="$|\psi_0|^2=${:.2f}".format(init_wave.norm(p=1)))


    plt.show()



def abstract():
    xs = torch.linspace(0, 10, 6000)
    y1 = barrier(4, 6, 3.5, xs)
    y2 = well(4, 6, 2.5, xs)
    state = Gaussian_Wave_Packet(100, 0.1, 0.7, xs)


    # 画势垒和势阱
    fig = plt.figure(num="subplots-axes", figsize=(8, 6)) # 创建画板，num是画板编号int or str
    fig.text(x=0.0, y=0.98, s="Designed by longwarriors", style='italic', fontsize=8, color="red")
    fig.set_tight_layout(True) # 紧凑组排

    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(xs, y1, "black") # "格式控制字符串"="颜色"+"点型"+"线型"
    ax1.set_ylim(bottom=-5, top=5)
    ax1.set_title("Potential barrier")

    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(xs, y2, "magenta")
    ax2.set_ylim(bottom=-5, top=5)
    ax2.set_title("Potential well")

    ax3 = plt.subplot(2, 1, 2)
    ax3.plot(xs, state.real, label="$Re(\psi)$")
    ax3.plot(xs, state.imag, label="$Im(\psi)$")
    ax3.plot(xs, state.abs(), label="$P(\psi)$")
    ax3.plot(xs, barrier(2, 2.2, 4, xs), label="$V(x)$")
    ax3.set_xlim(left=0, right=3)
    ax3.set_title("Gaussian Wavelet")
    ax3.legend()

    # plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    scene()
