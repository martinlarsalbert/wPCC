"""
References:
[1] : Wang, Tongtong, Guoyuan Li, Baiheng Wu, Vilmar Æsøy, and Houxiang Zhang. “Parameter Identification of Ship Manoeuvring Model Under Disturbance Using Support Vector Machine Method.” Ships and Offshore Structures, May 19, 2021.
"""


import sympy as sp
from src.symbols import *
import pandas as pd
from src.nonlinear_vmm_equations import *

p = df_parameters['symbol']

## X

#[1] eq.2-a:
X_qs_eq = sp.Eq(X_D,
        p.Xu*u + 
        p.Xuu*u**2 + 
        #p.Xuuu*u**3 + 
        #p.Xvv*v**2 + 
        #p.Xrr*r**2 + 
        #p.Xvr*v*r +
        p.Xdeltadelta*delta**2 + 
        #p.Xudeltadelta*u*delta**2 + 
        #p.Xvdelta*v*delta + 
        #p.Xuvdelta*u*v*delta + 
        #p.Xuvv*u*v**2 +
        #p.Xurr*u*r**2 + 
        #p.Xuvr*u*v*r + 
        #p.Xrdelta*r*delta + 
        #p.Xurdelta*u*r*delta +
        p.Xthrust*thrust  
                
        )

X_eq = X_eom.subs([
    (X_force,sp.solve(fx_eq,X_force)[0]),
    (X_D,sp.solve(X_qs_eq,X_D)[0])
])

## Y

#[1] eq.2-b:
Y_qs_eq = sp.Eq(Y_D,
        
        p.Yv*v + 
        p.Yr*r + 
        #p.Yvvv*v**3 + 
        #p.Yvvr*v**2*r + 
        #p.Yrrr*r**3 +
        #p.Yvrr*v*r**2 + 
        #p.Yuuv*u**2*v + 
        #p.Yuur*u**2*r + 
        #p.Yuv*u*v + 
        #p.Yur*u*r + 
        p.Ydelta*delta
        #p.Ydeltadeltadelta*delta**3 + 
        #p.Yudelta*u*delta + 
        #p.Yuudelta*u**2*delta + 
        #p.Yvdeltadelta*v*delta**2 + 
        #p.Yvvdelta*v**2*delta + 
        #p.Yrdeltadelta*r*delta**2 +
        #p.Yrrdelta*r**2*delta + 
        #p.Yvrdelta*v*r*delta + 
        #p.Y0 + 
        #p.Y0u*u + p.Y0uu*u**2
    )

Y_eq = Y_eom.subs([
    (Y_force,sp.solve(fy_eq,Y_force)[0]),
    (Y_D,sp.solve(Y_qs_eq,Y_D)[0]),
    ])

## N
#[1] eq.2-c:
N_qs_eq = sp.Eq(N_D,
        
        p.Nv*v + 
        p.Nr*r + 
        #p.Nvvv*v**3 + 
        #p.Nvvr*v**2*r + 
        #p.Nrrr*r**3 +
        #p.Nvrr*v*r**2 + 
        #p.Nuuv*u**2*v + 
        #p.Nuur*u**2*r + 
        #p.Nuv*u*v +
        #p.Nur*u*r + 
        p.Ndelta*delta
        #p.Ndeltadeltadelta*delta**3 + 
        #p.Nudelta*u*delta + 
        #p.Nuudelta*u**2*delta +
        #p.Nrrdelta*r**2*delta + 
        #p.Nvrdelta*v*r*delta + 
        #p.Nvdeltadelta*v*delta**2 + 
        #p.Nrdeltadelta*r*delta**2 + 
        #p.Nvvdelta*v**2*delta + 
        #p.N0 + 
        #p.N0u*u + p.N0uu*u**2
        
    )

N_eq = N_eom.subs([
    (N_force,sp.solve(mz_eq,N_force)[0]),
    (N_D,sp.solve(N_qs_eq,N_D)[0]),
])
