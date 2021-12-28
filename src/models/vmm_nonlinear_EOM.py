"""
Simulation model with nonlinear Equation Of Motion (EOM) but still linear system forces X_qs, Y_qs, N_qs

References:
"""


import sympy as sp
from src.symbols import *
import pandas as pd
from src.nonlinear_vmm_equations import *
from src.models.vmm import Simulator

p = df_parameters["symbol"]

subs = [
    (p.Xvdot, 0),
    (p.Xrdot, 0),
    (p.Yudot, 0),
    # (p.Yrdot,0),  # this is probably not true
    (p.Nudot, 0),
    # (p.Nvdot,0),# this is probably not true
]

## X

X_qs_eq = sp.Eq(
    X_D,
    p.Xu * u + p.Xv * v + p.Xr * r + p.Xdelta * delta + p.Xrr * r ** 2 + p.Xvr * v * r,
)

fx_eq = fx_eq.subs(subs)
X_eq = X_eom.subs(
    [
        (X_force, sp.solve(fx_eq, X_force)[0]),
        # (X_qs,sp.solve(X_qs_eq,X_qs)[0])
    ]
)

## Y

# Linearizing the EOM:

Y_qs_eq = sp.Eq(Y_D, p.Yu * u + p.Yv * v + p.Yr * r + p.Ydelta * delta + p.Yur * u * r)

fy_eq = fy_eq.subs(subs)
Y_eq = Y_eom.subs(
    [
        (Y_force, sp.solve(fy_eq, Y_force)[0]),
        # (Y_qs,sp.solve(Y_qs_eq,Y_qs)[0]),
    ]
)

## N

N_qs_eq = sp.Eq(N_D, p.Nu * u + p.Nv * v + p.Nr * r + p.Ndelta * delta + p.Nur * u * r)

mz_eq = mz_eq.subs(subs)
N_eq = N_eom.subs(
    [
        (N_force, sp.solve(mz_eq, N_force)[0]),
        # (N_qs,sp.solve(N_qs_eq,N_qs)[0]),
    ]
)

# Create a simulator for this model:
simulator = Simulator(X_eq=X_eq, Y_eq=Y_eq, N_eq=N_eq)
simulator.define_quasi_static_forces(X_qs_eq=X_qs_eq, Y_qs_eq=Y_qs_eq, N_qs_eq=N_qs_eq)