import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Import extra tabs
from comparison import comparison_tab
from convergence import convergence_tab
from export_report import export_report_tab


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
# Page Configuration
# ==========================

st.set_page_config(
    page_title="American Put FDM",
    layout="wide"
)


# ==========================
# Title
# ==========================

st.title(
    "American Put Option Pricing Using Finite Difference Methods"
)


st.write("""
### Developer
**Milliano Benjamin Kadzilawa**

### Problem Description

American options allow the holder to exercise the option at any time
before maturity.

Unlike European options, American options generally do not have a
closed-form analytical solution. Therefore numerical methods are required.

This project compares:

- Explicit Finite Difference Method
- Implicit Finite Difference Method
- Crank-Nicolson Method

for pricing an American put option.
""")


# ==========================
# Mathematical Model
# ==========================

with st.expander("Show Mathematical Formulation"):

    st.subheader("Black-Scholes PDE")

    st.latex(
    r"""
    \frac{\partial V}{\partial t}
    +
    \frac{1}{2}\sigma^2S^2
    \frac{\partial^2V}{\partial S^2}
    +
    rS\frac{\partial V}{\partial S}
    -
    rV=0
    """
    )


    st.subheader("Terminal Condition")

    st.latex(
    r"""
    V(S,T)=\max(K-S,0)
    """
    )


    st.subheader("Early Exercise Condition")

    st.latex(
    r"""
    V(S,t)=\max(V(S,t),K-S)
    """
    )



# ==========================
# Sidebar Inputs
# ==========================

st.sidebar.header(
    "Option Parameters"
)


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


M = st.sidebar.number_input(
    "Space Steps (M)",
    value=100
)


N = st.sidebar.number_input(
    "Time Steps (N)",
    value=1000
)



# ==========================
# Tabs
# ==========================

tab1, tab2, tab3, tab4 = st.tabs(
[
    "🧮 Numerical Methods",
    "📊 Comparison",
    "📈 Convergence",
    "📄 Export Report"
]
)

# =====================================================
# Numerical Methods
# =====================================================


# ==========================================
# Explicit Finite Difference Method
# American Put
# ==========================================

def explicit_american_put(K, S0, T, r, sigma, M, N):

    S_max = 2*K

    dt = T/N

    S = np.linspace(0, S_max, M+1)

    V = np.maximum(K-S,0)


    i = np.arange(1,M)


    a = 0.5*dt*(sigma**2*i**2-r*i)

    b = 1-dt*(sigma**2*i**2+r)

    c = 0.5*dt*(sigma**2*i**2+r*i)



    for n in range(N):

        V_old = V.copy()


        for j in range(1,M):

            V[j] = (
                a[j-1]*V_old[j-1]
                +
                b[j-1]*V_old[j]
                +
                c[j-1]*V_old[j+1]
            )


        # Early exercise

        V = np.maximum(
            V,
            K-S
        )


        # Boundary conditions

        V[0] = K
        V[-1] = 0



    price = np.interp(
        S0,
        S,
        V
    )


    return price,S,V





# ==========================================
# Implicit Finite Difference Method
# American Put
# ==========================================


def implicit_american_put(K, S0, T, r, sigma, M, N):

    S_max = 2*K

    dt = T/N


    S = np.linspace(
        0,
        S_max,
        M+1
    )


    V = np.maximum(K-S,0)


    i = np.arange(1,M)



    a = 0.5*dt*(sigma**2*i**2-r*i)

    b = 1+dt*(sigma**2*i**2+r)

    c = 0.5*dt*(sigma**2*i**2+r*i)



    A = np.zeros(
        (M-1,M-1)
    )


    for j in range(M-1):

        A[j,j] = b[j]


        if j > 0:

            A[j,j-1] = -a[j]


        if j < M-2:

            A[j,j+1] = -c[j]




    for n in range(N):


        rhs = V[1:M].copy()


        V_new = np.linalg.solve(
            A,
            rhs
        )


        V[1:M] = V_new



        # Early exercise

        V = np.maximum(
            V,
            K-S
        )



        V[0] = K

        V[-1] = 0



    price = np.interp(
        S0,
        S,
        V
    )


    return price,S,V





# ==========================================
# Crank-Nicolson Method
# American Put
# ==========================================


def crank_nicolson_american_put(
    K,
    S0,
    T,
    r,
    sigma,
    M,
    N
):

    S_max = 2*K

    dt = T/N


    S = np.linspace(
        0,
        S_max,
        M+1
    )


    V = np.maximum(
        K-S,
        0
    )


    i = np.arange(1,M)



    a = 0.25*dt*(sigma**2*i**2-r*i)

    b = -0.5*dt*(sigma**2*i**2+r)

    c = 0.25*dt*(sigma**2*i**2+r*i)




    A = np.zeros(
        (M-1,M-1)
    )


    B = np.zeros(
        (M-1,M-1)
    )



    for j in range(M-1):

        A[j,j] = 1-b[j]

        B[j,j] = 1+b[j]



        if j > 0:

            A[j,j-1] = -a[j]

            B[j,j-1] = a[j]



        if j < M-2:

            A[j,j+1] = -c[j]

            B[j,j+1] = c[j]




    for n in range(N):


        rhs = B @ V[1:M]


        V_new = np.linalg.solve(
            A,
            rhs
        )


        V[1:M] = V_new



        # Early exercise

        V = np.maximum(
            V,
            K-S
        )



        V[0] = K

        V[-1] = 0




    price = np.interp(
        S0,
        S,
        V
    )


    return price,S,V

# =====================================================
# Tab 1: Numerical Methods
# =====================================================

with tab1:

    st.header("Individual Finite Difference Methods")


    method = st.selectbox(
        "Choose Method",
        [
            "Explicit",
            "Implicit",
            "Crank-Nicolson"
        ]
    )


    if st.button("Calculate Price"):


        if method == "Explicit":

            price,S,V = explicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )


        elif method == "Implicit":

            price,S,V = implicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )


        else:

            price,S,V = crank_nicolson_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )



        st.success(
            f"{method} Method Price = {price:.4f}"
        )



        fig, ax = plt.subplots()


        ax.plot(
            S,
            V
        )


        ax.set_xlabel(
            "Stock Price"
        )


        ax.set_ylabel(
            "Option Value"
        )


        ax.set_title(
            f"American Put - {method}"
        )


        ax.grid(True)


        st.pyplot(fig)



# =====================================================
# Tab 2: Comparison
# =====================================================

with tab2:

    comparison_tab(
        K,
        S0,
        T,
        r,
        sigma,
        M,
        N,
        explicit_american_put,
        implicit_american_put,
        crank_nicolson_american_put
    )



# =====================================================
# Tab 3: Convergence Analysis
# =====================================================

with tab3:

      convergence_tab(
    K,
    S0,
    T,
    r,
    sigma,
    M,
    N,
    explicit_american_put,
    implicit_american_put,
    crank_nicolson_american_put
)



# =====================================================
# Tab 4: Export Report
# =====================================================

with tab4:

    export_report_tab(
        K,
        S0,
        T,
        r,
        sigma,
        M,
        N,
        explicit_american_put,
        implicit_american_put,
        crank_nicolson_american_put
    )



# =====================================================
# Footer
# =====================================================

st.markdown("---")

st.caption(
"""
Developed by:

Milliano Benjamin Kadzilawa

BSc Actuarial Science (Honours)

University of Malawi
"""
)
