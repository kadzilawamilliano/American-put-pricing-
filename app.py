import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# =====================================================
# American Put Option Pricing Using Finite Difference Methods
#
# Developer: Milliano Benjamin Kadzilawa
#
# Methods:
# 1. Explicit Finite Difference Method
# 2. Implicit Finite Difference Method
# 3. Crank-Nicolson Method
# =====================================================


# ==========================
# Title and Description
# ==========================

st.title("American Put Option Pricing Using Finite Difference Methods")

st.write("""
## Developer
**Milliano Benjamin Kadzilawa**

## Problem Description

American options allow the holder to exercise the option at any time
before maturity.

Unlike European options, American options generally do not have a
closed-form analytical solution, therefore numerical methods are required.

This project compares:

- Explicit Finite Difference Method
- Implicit Finite Difference Method
- Crank-Nicolson Method

for pricing an American put option.
""")


# ==========================
# Black-Scholes PDE
# ==========================

st.subheader("Black-Scholes PDE")

st.latex(
r"""
\frac{\partial V}{\partial t}
+
\frac{1}{2}\sigma^2S^2
\frac{\partial^2 V}{\partial S^2}
+
rS\frac{\partial V}{\partial S}
-rV=0
"""
)


# ==========================
# American Put Conditions
# ==========================

st.subheader("American Put Conditions")

st.write("""
Terminal payoff:
""")

st.latex(
r"""
V(S,T)=\max(K-S,0)
"""
)

st.write("""
Early exercise condition:
""")

st.latex(
r"""
V(S,t)=\max(V(S,t),K-S)
"""
)


# ==========================
# User Inputs
# ==========================

st.sidebar.header("Option Parameters")


K = st.sidebar.number_input(
    "Strike Price (K)",
    value=50.0
)


S0 = st.sidebar.number_input(
    "Current Stock Price (S0)",
    value=50.0
)


T = st.sidebar.number_input(
    "Time to Maturity (Years)",
    value=1.0
)


r = st.sidebar.number_input(
    "Risk Free Rate",
    value=0.05
)


sigma = st.sidebar.number_input(
    "Volatility",
    value=0.20
)


# Numerical grid parameters

M = st.sidebar.number_input(
    "Space Steps (M)",
    value=100
)


N = st.sidebar.number_input(
    "Time Steps (N)",
    value=1000
)


st.write("Parameters loaded successfully ✅")
# ==========================================
# Explicit Finite Difference Method
# American Put
# ==========================================

def explicit_american_put(K, S0, T, r, sigma, M, N):

    S_max = 2*K

    dS = S_max / M
    dt = T / N

    # Stock price grid
    S = np.linspace(0, S_max, M+1)


    # Terminal payoff
    V = np.maximum(K-S, 0)


    # Coefficients

    i = np.arange(1, M)

    a = 0.5*dt*(sigma**2*i**2 - r*i)

    b = 1 - dt*(sigma**2*i**2 + r)

    c = 0.5*dt*(sigma**2*i**2 + r*i)



    # Backward time stepping

    for n in range(N):

        V_old = V.copy()


        for j in range(1, M):

            V[j] = (
                a[j-1]*V_old[j-1]
                +
                b[j-1]*V_old[j]
                +
                c[j-1]*V_old[j+1]
            )


        # American early exercise condition

        V = np.maximum(
            V,
            K-S
        )


        # Boundary conditions

        V[0] = K

        V[-1] = 0



    # Option value at S0

    price = np.interp(
        S0,
        S,
        V
    )


    return price, S, V

# ==========================================
# Run Explicit Method
# ==========================================

if st.button("Calculate American Put Price"):


    price, S, V = explicit_american_put(
        K,
        S0,
        T,
        r,
        sigma,
        M,
        N
    )


    st.success(
        f"Explicit Method Price = {price:.4f}"
    )


    fig, ax = plt.subplots()

    ax.plot(S,V)

    ax.set_xlabel("Stock Price")

    ax.set_ylabel("Option Value")

    ax.set_title(
        "American Put Price - Explicit Method"
    )

    ax.grid()


    st.pyplot(fig)
# ==========================================
# Implicit Finite Difference Method
# American Put
# ==========================================

def implicit_american_put(K, S0, T, r, sigma, M, N):

    S_max = 2*K

    dS = S_max/M
    dt = T/N

    S = np.linspace(0, S_max, M+1)

    V = np.maximum(K-S,0)


    i = np.arange(1,M)


    a = 0.5*dt*(sigma**2*i**2-r*i)

    b = 1+dt*(sigma**2*i**2+r)

    c = 0.5*dt*(sigma**2*i**2+r*i)


    # Matrix construction

    A = np.zeros((M-1,M-1))


    for j in range(M-1):

        A[j,j] = b[j]

        if j > 0:
            A[j,j-1] = -a[j]

        if j < M-2:
            A[j,j+1] = -c[j]



    # Time stepping

    for n in range(N):

        rhs = V[1:M].copy()


        V_new = np.linalg.solve(A,rhs)


        V[1:M] = V_new


        # Early exercise

        V = np.maximum(V,K-S)


        # Boundary conditions

        V[0] = K

        V[-1] = 0



    price = np.interp(S0,S,V)


    return price,S,V

if st.button("Calculate Implicit Method"):

    price,S,V = implicit_american_put(
        K,
        S0,
        T,
        r,
        sigma,
        M,
        N
    )

    st.success(
        f"Implicit Method Price = {price:.4f}"
    )


    fig,ax = plt.subplots()

    ax.plot(S,V)

    ax.set_title(
        "American Put - Implicit Method"
    )

    ax.set_xlabel("Stock Price")
    ax.set_ylabel("Option Value")

    ax.grid()

    st.pyplot(fig)
