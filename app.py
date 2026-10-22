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
