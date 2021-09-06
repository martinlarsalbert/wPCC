"""[summary]

[1] Clarke, D., P. Gedling, and G. Hine. “The Application of Manoeuvring Criteria in Hull Design Using Linear Theory.” Transactions of the Royal Institution of Naval Architects, RINA., 1982. https://repository.tudelft.nl/islandora/object/uuid%3A2a5671ac-a502-43e1-9683-f27c50de3570.
[2] Brix, Jochim E. Manoeuvring Technical Manual. Seehafen-Verlag, 1993.

"""

import sympy as sp
from sympy.physics.mechanics import (dynamicsymbols, ReferenceFrame,
                                      Particle, Point)
from src.substitute_dynamic_symbols import lambdify
import pandas as pd
import numpy as np

u, v, r, delta, thrust = dynamicsymbols('u v r delta thrust')
m,x_G,U,I_z,volume = sp.symbols('m x_G U I_z volume')
π = sp.pi
T,L,CB,B,rho,t,dt = sp.symbols('T L CB B rho t dt')

f_ext_x,f_ext_y,m_ext_z = sp.symbols('f_ext_x,f_ext_y,m_ext_z')  # external forces


X_X, X_Y, X_N = sp.symbols('X_X X_Y X_N')  # State matrixes

X_force, Y_force, N_force = sp.symbols('X_force Y_force N_force')  # Force models

X_qs = sp.Function('X_qs')(u,v,r,delta)  # quasi static force
Y_qs = sp.Function('Y_qs')(u,v,r,delta)  # quasi static force
N_qs = sp.Function('N_qs')(u,v,r,delta)  # quasi static force

n,delta_t = sp.symbols('n delta_t')  # Time step n

A_coeff, B_coeff, C_coeff = sp.symbols('A_coeff, B_coeff, C_coeff')  
X_coeff, Y_coeff, N_coeff = sp.symbols('X_coeff, Y_coeff, N_coeff')  


X_n = sp.Function('X')(n)  # X features
Y_n = sp.Function('Y')(n)  # X features
N_n = sp.Function('N')(n)  # X features



