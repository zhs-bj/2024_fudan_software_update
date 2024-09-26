"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : cellmodel.py
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

def cellmodel_odes(t, y, rates, parameters):
    assert len(rates) % 4 == 0
    n_cds = (len(rates) - 4) // 4
    b = rates[0]
    dm = rates[1]
    kb = rates[2]
    ku = rates[3]
    kbic = np.array(rates[4:4+n_cds])
    kuic = np.array(rates[4+n_cds:4+2*n_cds])
    dmic = np.array(rates[4+2*n_cds:4+3*n_cds])
    dpic = np.array(rates[4+3*n_cds:4+4*n_cds])

    thetar = parameters[0]
    s0 = parameters[1]
    gmax = parameters[2]
    thetax = parameters[3]
    Kt = parameters[4]
    M = parameters[5]
    we = parameters[6]
    Km = parameters[7]
    vm = parameters[8]
    nx = parameters[9]
    Kq = parameters[10]
    Kg = parameters[11]
    vt = parameters[12]
    wr = parameters[13]
    wq = parameters[14]
    wic = parameters[15]
    nq = parameters[16]
    nr = parameters[17]
    ns = parameters[18]
    nic = np.array(parameters[19:19+n_cds])
    thetaic = np.array(parameters[19+n_cds:19+2*n_cds])
    Ric = np.array(parameters[19+2*n_cds:19+3*n_cds])
    gmaxic = np.array(parameters[19+3*n_cds:19+4*n_cds])

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
    mic = np.array(y[15:15+n_cds])
    rmic = np.array(y[15+n_cds:15+2*n_cds])
    pic = np.array(y[15+2*n_cds:15+3*n_cds])

    gamma = gmax * a / (Kg + a)
    gammaic = gmaxic * a / (Kg + a)
    ttrate = (rmq + rmr + rmt + rmm) * gamma
    lam = (ttrate + gamma * np.sum(rmic)) / M
    vcat = em * vm * si / (Km + si)

    dydt = np.zeros(len(y))
    dydt[0] = kb * r * mr - ku * rmr - gamma / nr * rmr - lam * rmr
    dydt[1] = gamma / nx * rmm - lam * em
    dydt[2] = kb * r * mq - ku * rmq - gamma / nx * rmq - lam * rmq
    dydt[3] = kb * r * mt - ku * rmt - gamma / nx * rmt - lam * rmt
    dydt[4] = gamma / nx * rmt - lam * et
    dydt[5] = kb * r * mm - ku * rmm - gamma / nx * rmm - lam * rmm
    dydt[6] = (we * a / (thetax + a)) + ku * rmt + gamma / nx * rmt - kb * r * mt - dm * mt - lam * mt
    dydt[7] = (we * a / (thetax + a)) + ku * rmm + gamma / nx * rmm - kb * r * mm - dm * mm - lam * mm
    dydt[8] = gamma / nx * rmq - lam * q
    dydt[9] = (et * vt * s0 / (Kt + s0)) - vcat - lam * si
    dydt[10] = (wq * a / (thetax + a) / (1 + (q / Kq) ** nq)) + ku * rmq + gamma / nx * rmq - kb * r * mq - dm * mq - lam * mq
    dydt[11] = (wr * a / (thetar + a)) + ku * rmr + gamma / nr * rmr - kb * r * mr - dm * mr - lam * mr
    dydt[12] = ku * rmr + ku * rmt + ku * rmm + ku * rmq + gamma / nr * rmr + gamma / nr * rmr + gamma / nx * rmt + gamma / nx * rmm + gamma / nx * rmq - kb * r * mr - kb * r * mt - kb * r * mm - kb * r * mq - lam * r + np.sum(gammaic / nic * rmic - kbic * r * mic + kuic * rmic)
    dydt[13] = ns * vcat - ttrate - np.sum(gammaic * rmic) - lam * a
    dydt[14] = lam
    dydt[15:15+n_cds] = (wic * a / (thetaic + a) * Ric) + kuic * rmic - kbic * r * mic + gammaic / nic * rmic - dmic * mic - lam * mic
    dydt[15+n_cds:15+2*n_cds] = kbic * r * mic - kuic * rmic - gammaic / nic * rmic - lam * rmic
    dydt[15+2*n_cds:15+3*n_cds] = gammaic / nic * rmic - lam * pic - dpic * pic

    return dydt