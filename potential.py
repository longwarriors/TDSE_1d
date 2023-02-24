# -*- coding: utf-8 -*-
# @Author: Zhangxiaoxu
# @Date:   2023-02-24 10:16:58
# @Last Modified by:   longwarriors
# @Last Modified time: 2023-02-24 14:12:24
import torch
from torch import tensor


def barrier(start, end, height, xNodes):
    """输入x离散点"""
    if xNodes[0] < start and xNodes[-1] > end:
        # 阶跃函数heaviside是可以求导的，布尔函数不行torch.where()
        potential = torch.heaviside(xNodes-start, tensor([0.5])) + torch.heaviside(end-xNodes, tensor([0.5]))
        potential -= 1.0
        potential *= height
        return potential
    else:
        raise ValueError("Not a potential well!")


def step(start, height, xNodes):
    """one-dimensional step potential"""
    potential = height * torch.heaviside(xNodes - start, tensor([1.0]))
    return potential


def well(start, end, depth, xNodes):
    """输入x离散点"""
    if xNodes[0] < start and xNodes[-1] > end:
        potential = torch.heaviside(start-xNodes, tensor([0.5])) + torch.heaviside(xNodes-end, tensor([0.5]))
        potential -= 1.0
        potential *= depth
        return potential
    else:
        raise ValueError("Not a potential well!")
