"""[summary]

[1] Clarke, D., P. Gedling, and G. Hine. “The Application of Manoeuvring Criteria in Hull Design Using Linear Theory.” Transactions of the Royal Institution of Naval Architects, RINA., 1982. https://repository.tudelft.nl/islandora/object/uuid%3A2a5671ac-a502-43e1-9683-f27c50de3570.
[2] Brix, Jochim E. Manoeuvring Technical Manual. Seehafen-Verlag, 1993.

"""

import sympy as sp
import sympy.physics.mechanics
from src.substitute_dynamic_symbols import lambdify
import pandas as pd
import numpy as np


def dynamicsymbols(s):
    """Overlaying this to append a fix for pickle"""

    symbols = sympy.physics.mechanics.dynamicsymbols(s)

    try:
        iter(symbols)
    except TypeError:
        symbols.__class__.__module__ = "__main__"
    else:
        for symbol in symbols:
            symbol.__class__.__module__ = "__main__"

    return symbols


"""Fossen, T., 2011. Nonlinear maneuvering theory and path-following control. Marine Technology and Engineering 1, 445–460.
"""
M = sp.symbols("M")  # Inertia matrix
C = sp.symbols("C")  # Coriolis matrix
D = sp.symbols("D")  # Damping matrix
x, y, z, phi, theta, psi = dynamicsymbols("x, y, z, phi, theta, psi")
u, v, w, p, q, r = dynamicsymbols("u, v, w, p, q, r")
u_c, v_c, w_c = dynamicsymbols("u_c, v_c, w_c")
eta = dynamicsymbols("eta")  # Positions
nu = dynamicsymbols("nu")  # Velocities
nu_r = dynamicsymbols("nu_r")  # Relative velocities (including current)
nu_c = dynamicsymbols("nu_c")  # Velocities (current)


tau, tau_wind, tau_wave = dynamicsymbols("tau, tau_wind, tau_wave")
g = dynamicsymbols("g")  # Gravitational and buoyancy forces.
g_0 = dynamicsymbols(
    "g_0"
)  # Static restoring forces and moments due to ballast systems

eq_6DOF = sp.Eq(M * nu.diff() + C * nu + D * nu + g + g_0, tau + tau_wind + tau_wave)
#
eq_eta = sp.Eq(
    eta, sp.UnevaluatedExpr(sp.Matrix([[x, y, z, phi, theta, psi]]).transpose())
)
eq_nu = sp.Eq(nu, sp.UnevaluatedExpr(sp.Matrix([[u, v, w, p, q, r]]).transpose()))
eq_nu_c = sp.Eq(
    nu_c, sp.UnevaluatedExpr(sp.Matrix([[u_c, v_c, w_c, 0, 0, 0]]).transpose())
)
eq_nu_r = sp.Eq(nu_r, sp.UnevaluatedExpr(eq_nu.rhs.doit() - eq_nu_c.rhs.doit()))

M_RB = sp.symbols("M_RB")  # Rigid body intertia matrix
M_A = sp.symbols("M_A")  # Added mass matrix

C_RB = sp.symbols("C_RB")  # Coriolis centrepetal matrix
C_A = sp.symbols("C_A")  # Coriolis centrepetal added mass matrix

eq_M = sp.Eq(M, M_RB + M_A)
eq_C = sp.Eq(C, C_RB + C_A)

eq_6DOF_expanded = sp.Eq(
    M_RB * nu.diff() + M_A * nu_r.diff() + C_RB * nu + C_A * nu_r + D * nu_r + g + g_0,
    tau + tau_wind + tau_wave,
)

eq_nu_steady = sp.Eq(nu_r.diff(), nu.diff())

eq_6DOF_expanded_r = sp.Eq(
    M_RB * nu_r.diff()
    + M_A * nu_r.diff()
    + C_RB * nu_r
    + C_A * nu_r
    + D * nu_r
    + g
    + g_0,
    tau + tau_wind + tau_wave,
)

u, v, r, delta, thrust = dynamicsymbols("u v r delta thrust")
m, x_G, U, I_z, volume = sp.symbols("m x_G U I_z volume")
π = sp.pi
T, L, CB, B, rho, t, dt = sp.symbols("T L CB B rho t dt")

f_ext_x, f_ext_y, m_ext_z = sp.symbols("f_ext_x,f_ext_y,m_ext_z")  # external forces


X_X, X_Y, X_N = sp.symbols("X_X X_Y X_N")  # State matrixes

X_force, Y_force, N_force = sp.symbols("X_force Y_force N_force")  # Force models

X_D = sp.Function("X_D")(u, v, r, delta)  # damping
Y_D = sp.Function("Y_D")(u, v, r, delta)  # damping
N_D = sp.Function("N_D")(u, v, r, delta)  # damping
for item in [X_D, Y_D, N_D]:
    item.__class__.__module__ = "__main__"  # Fix for pickle

n, delta_t = sp.symbols("n delta_t")  # Time step n

A_coeff, B_coeff, C_coeff = sp.symbols("A_coeff, B_coeff, C_coeff")
X_coeff, Y_coeff, N_coeff = sp.symbols("X_coeff, Y_coeff, N_coeff")


X_n = sp.Function("X")(n)  # X features
Y_n = sp.Function("Y")(n)  # X features
N_n = sp.Function("N")(n)  # X features


def glue_equations(module):
    # Glue equations
    from myst_nb import glue

    from sympy.physics.vector.printing import vlatex
    from IPython.display import Math

    for key, value in module.__dict__.items():
        if isinstance(value, sp.Eq):
            glue(key, Math(vlatex(value)), display=False)
            print(f"gluing:{key}")
