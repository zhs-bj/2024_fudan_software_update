"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : burden_calculator.py
@Author : Hongcheng Chen
"""
# Reference:
# 1. Weiße, A. Y., Oyarzún, D. A., Danos, V., & Swain, P. S. (2015).
#    Mechanistic links between cellular trade-offs, gene expression, and growth.
#    Proceedings of the National Academy of Sciences, 112(9), E1038-E1047.
# 2. Nikolados, E.-M., Weiße, A. Y., Ceroni, F., & Oyarzún, D. A. (2019).
#    Growth Defects and Loss-of-Function in Synthetic Gene Circuits.
#    ACS Synthetic Biology, 8(6), 1231-1240.

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.integrate import solve_ivp
from burden.cellmodel import cellmodel_odes

from burden.config import *

def burden_calculator(copy_number: float, prom_strength: float, tl_units: list[tuple[float, int, str]]):
    rbs_strengths = np.array([tl_units[i][0] for i in range(len(tl_units))])
    len_aa = np.array([tl_units[i][1] for i in range(len(tl_units))])
    cds_seqs = np.array([tl_units[i][2] for i in range(len(tl_units))])
    # parameters
    # - endogeneous
    thetar = 426.8693338968694
    s0 = 1.0e4
    gmax = 1260.0
    thetax = 4.379733394834643
    Kt = 1.0e3
    M = 1.0e8
    we = 4.139172187824451
    Km = 1.0e3
    vm = 5800.0
    nx = 300.0
    Kq = 1.522190403737490e+05
    Kg = 7
    vt = 726.0
    wr = 929.9678874564831
    wq = 948.9349882947897
    nq = 4
    nr = 7459.0
    ns = 0.5
    # - heterologous
    wic = (copy_number / beta_copy_number) * (prom_strength / beta_prom)
    rbsH = rbs_strengths * beta_rbs # array
    nic = len_aa # array
    thetaic = 4.38 * np.ones(len(rbsH)) # array
    Ric = np.ones(len(rbsH)) # array
    gmaxic = 1260 * np.ones(len(rbsH)) # array
    parameters = [thetar, s0, gmax, thetax, Kt, M, we, Km, vm, nx, Kq, Kg, vt, wr, wq, wic, nq, nr, ns]
    for i in nic, thetaic, Ric, gmaxic:
        for j in i:
            parameters.append(j)

    # define rate constants
    # - endogeneous
    b = 0
    dm = 0.1
    kb = 0.0095
    ku = 1.0
    # - heterologous
    kbic = 1e-2 * rbsH # array
    kuic = 1e-2 * np.ones(len(rbsH)) # array
    dmic = np.log(2) / 2 * np.ones(len(rbsH)) # array
    dpic = np.log(2) / 4 * np.ones(len(rbsH)) # array
    rates = [b, dm, kb, ku]
    for i in kbic, kuic, dmic, dpic:
        for j in i:
            rates.append(j)

    # define initial conditions
    rmr_0 = 0
    em_0 = 0
    rmq_0 = 0
    rmt_0 = 0
    et_0 = 0
    rmm_0 = 0
    mt_0 = 0
    mm_0 = 0
    q_0 = 0
    si_0 = 0
    mq_0 = 0
    mr_0 = 0
    r_0 = 10.0
    a_0 = 1000.0
    lam_0 = 0
    mic_0 = np.zeros(len(rbsH)) # array
    rmic_0 = np.zeros(len(rbsH)) # array
    pic_0 = np.zeros(len(rbsH)) # array
    init = [rmr_0, em_0, rmq_0, rmt_0, et_0, rmm_0, mt_0, mm_0, q_0, si_0, mq_0, mr_0, r_0, a_0, lam_0]
    for i in mic_0, rmic_0, pic_0:
        for j in i:
            init.append(j)

    # call solver routine 
    t0 = 0
    tf = 1e9
    sol = solve_ivp(cellmodel_odes, (t0, tf), init, method='LSODA', args=(rates, parameters))
    t = sol.t
    y = sol.y

    rmr = y[0]
    em = y[1]
    rmq = y[2]
    rmt = y[3]
    et = y[4]
    rmm = y[5]
    mt = y[6]
    mm = y[7]
    q = y[8]
    si = y[9]
    mq = y[10]
    mr = y[11]
    r = y[12]
    a = y[13]
    lam = y[14]
    mic = y[15:15+len(rbsH)]
    rmic = y[15+len(rbsH):15+2*len(rbsH)]
    pic = y[15+2*len(rbsH):15+3*len(rbsH)]
    return 1 - lam[-1] / growth_WT
