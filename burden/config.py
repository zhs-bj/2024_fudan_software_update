"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : config.py
@Author : Hongcheng Chen

Reference:
1. Weiße, A. Y., Oyarzún, D. A., Danos, V., & Swain, P. S. (2015).
   Mechanistic links between cellular trade-offs, gene expression, and growth.
   Proceedings of the National Academy of Sciences, 112(9), E1038-E1047.
2. Nikolados, E.-M., Weiße, A. Y., Ceroni, F., & Oyarzún, D. A. (2019).
   Growth Defects and Loss-of-Function in Synthetic Gene Circuits.
   ACS Synthetic Biology, 8(6), 1231-1240.
"""

START_CODON = 'ATG'
STOP_CODONS = ['TAA', 'TAG', 'TGA']

PROMOTER_UPSTREAM_SEQ = 'TTTCAGATAAAAAAAATCCTTAGCTTTCGCTAAGGATGATTTCTGGAATTCGCGGCCGCATCTAGAG'
PROMOTER_RBS_SCAR = 'TCTAGAG'
RBS_CDS_SCAR = 'TACTAG'
PRAP_RBS_PRE_SEQ = 'AGACAACCAGGAGTCTATAAAATAATCACTGAAGAGACTGGACGAAACCAATAGGTC'
PRAP_RBS_CDS_SEQ = 'TATACAT'

# fitted parameters
growth_WT = 20246867.33991941
beta_prom = 69.49128805
beta_rbs = 50.31487379
K_prom = 0.15280587748456265
B_prom = -57.82880923545156
K_rbs = 0.1823668
b_rbs = 0.28549235
beta_copy_number = 200