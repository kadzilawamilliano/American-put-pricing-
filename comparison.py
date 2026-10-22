import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def comparison_tab(
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
):

    st.header("Comparison of Numerical Methods")

    st.write("""
This section compares the three finite difference methods
for pricing an American put option.
""")

    if st.button("Run All Methods"):

        explicit_price, S, V_explicit = explicit_american_put(
            K, S0, T, r, sigma, M, N
        )

        implicit_price, S, V_implicit = implicit_american_put(
            K, S0, T, r, sigma, M, N
        )

        cn_price, S, V_cn = crank_nicolson_american_put(
            K, S0, T, r, sigma, M, N
        )

        results = pd.DataFrame(
            {
                "Method": [
                    "Explicit",
                    "Implicit",
                    "Crank-Nicolson"
                ],
                "Option Price": [
                    explicit_price,
                    implicit_price,
                    cn_price
                ]
            }
        )

        st.subheader("Option Prices")

        st.dataframe(results)

        fig, ax = plt.subplots(figsize=(8,5))

        ax.plot(
            S,
            V_explicit,
            label="Explicit"
        )

        ax.plot(
            S,
            V_implicit,
            label="Implicit"
        )

        ax.plot(
            S,
            V_cn,
            label="Crank-Nicolson"
        )

        ax.set_xlabel("Stock Price")

        ax.set_ylabel("Option Value")

        ax.set_title(
            "Comparison of Numerical Methods"
        )

        ax.legend()

        ax.grid(True)

        st.pyplot(fig)

        st.subheader("Discussion")

        st.write("""
The Explicit method is computationally simple but is conditionally stable.

The Implicit method is unconditionally stable and generally produces smoother
solutions.

The Crank–Nicolson method combines the advantages of both methods and
typically provides the most accurate numerical approximation.
""")
