import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from comparison_analysis import run_comparison


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


        # ==========================================
        # Run comparison analysis
        # ==========================================

        comparison_df, recommendation = run_comparison(
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


        # ==========================================
        # Save comparison results for PDF export
        # ==========================================

        st.session_state["comparison_results"] = comparison_df

        st.session_state["comparison_recommendation"] = recommendation



        # ==========================================
        # Display Results
        # ==========================================

        st.subheader("Numerical Comparison")


        st.dataframe(
            comparison_df,
            use_container_width=True
        )



        # ==========================================
        # Error Comparison Plot
        # ==========================================

        st.subheader(
            "Accuracy Comparison"
        )


        fig1, ax1 = plt.subplots(
            figsize=(8,5)
        )


        ax1.bar(
            comparison_df["Method"],
            comparison_df["Percentage Error (%)"]
        )


        ax1.set_ylabel(
            "Percentage Error (%)"
        )


        ax1.set_title(
            "Numerical Error Compared With Crank-Nicolson"
        )


        ax1.grid(True)


        st.pyplot(fig1)



        # ==========================================
        # Runtime Comparison
        # ==========================================

        st.subheader(
            "Computational Efficiency"
        )


        fig2, ax2 = plt.subplots(
            figsize=(8,5)
        )


        ax2.bar(
            comparison_df["Method"],
            comparison_df["Runtime (seconds)"]
        )


        ax2.set_ylabel(
            "Runtime (seconds)"
        )


        ax2.set_title(
            "Computational Time Comparison"
        )


        ax2.grid(True)


        st.pyplot(fig2)



        # ==========================================
        # Recommendation
        # ==========================================

        st.subheader(
            "Method Selection"
        )


        st.info(
            recommendation
        )



        # ==========================================
        # Download Results
        # ==========================================

        csv = comparison_df.to_csv(
            index=False
        )


        st.download_button(

            label="Download Comparison Results",

            data=csv,

            file_name="finite_difference_comparison.csv",

            mime="text/csv"

        )    
            
