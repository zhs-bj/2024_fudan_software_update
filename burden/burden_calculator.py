"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : burden_calculator.py
@Author : Hongcheng Chen

Reference:
1. Weiße, A. Y., Oyarzún, D. A., Danos, V., & Swain, P. S. (2015).
   Mechanistic links between cellular trade-offs, gene expression, and growth.
   Proceedings of the National Academy of Sciences, 112(9), E1038-E1047.
2. Nikolados, E.-M., Weiße, A. Y., Ceroni, F., & Oyarzún, D. A. (2019).
   Growth Defects and Loss-of-Function in Synthetic Gene Circuits.
   ACS Synthetic Biology, 8(6), 1231-1240.
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.integrate import solve_ivp
from cellmodel import cellmodel_odes
from sklearn.metrics import mean_squared_error

# constant parameters
growth0 = 20246867.33991941
beta_prom = 35.75
beta_rbs = 15.6851227
K_rbs = 0.21170254
b_rbs = 0.24290994

def BurdenCalculator(copy_number: float,prom_strength: float, tl_units: list[tuple[float, str]]):
    rbsH = [tl_units[i][0] for i in range(len(tl_units))] * beta_rbs
    # parameters
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
    wic = copy_number * prom_strength / beta_prom  # 500
    nq = 4
    nr = 7459.0
    ns = 0.5
    nic = 233 # BFP # GFP:238
    thetaic = 4.38
    Ric = 1  # 0.8
    gmaxic = 1260 * rbsH  # 1260.0
    parameters = (thetar, s0, gmax, thetax, Kt, M, we, Km, vm, nx, Kq, Kg, vt, wr, wq, wic, nq, nr, ns, nic, thetaic, Ric, gmaxic)

    # define rate constants
    b = 0
    dm = 0.1
    kb = 0.0095
    ku = 1.0
    kbic = 1e-2*rbsH
    kuic = 1e-2/rbsH
    dmic = np.log(2) / 2
    dpic = np.log(2) / 4
    rates = (b, dm, kb, ku, kbic, kuic, dmic, dpic)

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
    mic_0 = 0
    rmic_0 = 0
    pic_0 = 0
    r_0 = 10.0
    a_0 = 1000.0
    lam_0 = 0
    init = (rmr_0, em_0, rmq_0, rmt_0, et_0, rmm_0, mt_0, mm_0, q_0, si_0, mq_0, mr_0, mic_0, rmic_0, pic_0, r_0, a_0, lam_0)

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
    mic = y[12]
    rmic = y[13]
    pic = y[14]
    r = y[15]
    a = y[16]
    lam = y[17]
    return 1-lam[-1]/growth0