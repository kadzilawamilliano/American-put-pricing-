import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time


def convergence_tab(
    K,
    S0,
    T,
    r,
    sigma,
    explicit_american_put,
    implicit_american_put,
    crank_nicolson_american_put
):

    st.header("Convergence Analysis")

    st.write("""
Convergence analysis investigates how the numerical solution changes
as the computational grid becomes finer.

A convergent finite difference method should approach a stable
solution as the mesh is refined.
""")


    # ==========================================
    # Analysis Level
    # ==========================================
  # ==========================================
# Analysis Level
# ==========================================

analysis_level = st.selectbox(
    "Select Analysis Level",
    [
        "Quick",
        "Standard",
        "Detailed"
    ]
)


# Use the user's chosen grid as the maximum grid
max_M = int(M)
max_N = int(N)


if analysis_level == "Quick":

    grids = [

        (
            max(10, max_M//4),
            max(50, max_N//4)
        ),

        (
            max(20, max_M//2),
            max(100, max_N//2)
        ),

        (
            max_M,
            max_N
        )
    ]


elif analysis_level == "Standard":

    grids = [

        (
            max(10, max_M//4),
            max(50, max_N//4)
        ),

        (
            max(20, max_M//2),
            max(100, max_N//2)
        ),

        (
            max(30, (3*max_M)//4),
            max(150, (3*max_N)//4)
        ),

        (
            max_M,
            max_N
        )
    ]


else:

    grids = [

        (
            max(10, max_M//5),
            max(40, max_N//5)
        ),

        (
            max(20, (2*max_M)//5),
            max(80, (2*max_N)//5)
        ),

        (
            max(30, (3*max_M)//5),
            max(120, (3*max_N)//5)
        ),

        (
            max(40, (4*max_M)//5),
            max(160, (4*max_N)//5)
        ),

        (
            max_M,
            max_N
        )
    ]
    st.info(
f"""
Analysis Level: **{analysis_level}**

Maximum Grid Selected

• Space Steps (M) = {max_M}

• Time Steps (N) = {max_N}

The convergence study will automatically build
progressively finer computational grids ending
at your selected values.
"""
    )



            # ===================================
            # Explicit Stability Check
            # ===================================

            S_max = 2*K

            dS = S_max/M

            dt = T/N


            stability_parameter = (
                sigma**2 *
                S_max**2 *
                dt /
                (dS**2)
            )


            if stability_parameter <= 1:

                explicit_status = "Stable"

            else:

                explicit_status = "Unstable"



            # ===================================
            # Explicit Method
            # ===================================

            explicit_price,_,_ = explicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )



            # ===================================
            # Implicit Method
            # ===================================

            implicit_price,_,_ = implicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )



            # ===================================
            # Crank-Nicolson Method
            # ===================================

            cn_price,_,_ = crank_nicolson_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )



            results.append(
                [
                    M,
                    N,
                    round(explicit_price,6),
                    explicit_status,
                    round(implicit_price,6),
                    round(cn_price,6)
                ]
            )


            convergence_df = pd.DataFrame(

                results,

                columns=[
                    "Space Steps (M)",
                    "Time Steps (N)",
                    "Explicit",
                    "Stability",
                    "Implicit",
                    "Crank-Nicolson"
                ]

            )


            table_placeholder.dataframe(
                convergence_df,
                use_container_width=True
            )


            progress.progress(
                (index+1)/total
            )
        # ==========================================
        # Finished Calculations
        # ==========================================

        end = time.time()

        runtime = end - start


        status.success(
            "Convergence analysis completed successfully."
        )


        st.success(
            f"Execution Time: {runtime:.2f} seconds"
        )


        # ==========================================
        # Summary Statistics
        # ==========================================

        st.subheader("Summary Statistics")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Final Explicit Price",
                f"{convergence_df['Explicit'].iloc[-1]:.6f}"
            )


        with col2:

            st.metric(
                "Final Implicit Price",
                f"{convergence_df['Implicit'].iloc[-1]:.6f}"
            )


        with col3:

            st.metric(
                "Final Crank-Nicolson Price",
                f"{convergence_df['Crank-Nicolson'].iloc[-1]:.6f}"
            )


        # ==========================================
        # Convergence Plot
        # ==========================================

        st.subheader(
            "Convergence Plot"
        )


        fig, ax = plt.subplots(figsize=(9,5))


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Explicit"],
            marker="o",
            linewidth=2,
            label="Explicit"
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Implicit"],
            marker="s",
            linewidth=2,
            label="Implicit"
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Crank-Nicolson"],
            marker="^",
            linewidth=2,
            label="Crank-Nicolson"
        )


        ax.set_xlabel(
            "Space Steps (M)"
        )


        ax.set_ylabel(
            "Option Price"
        )


        ax.set_title(
            "Convergence of Finite Difference Methods"
        )


        ax.grid(True)

        ax.legend()

        st.pyplot(fig)


        # ==========================================
        # Download Results
        # ==========================================

        csv = convergence_df.to_csv(
            index=False
        )


        st.download_button(

            label="Download Convergence Results (CSV)",

            data=csv,

            file_name="convergence_results.csv",

            mime="text/csv"

        )


        # ==========================================
        # Interpretation
        # ==========================================

        st.subheader(
            "Interpretation"
        )


        st.write(
        """
As the computational grid becomes finer, the numerical
solutions become more stable, indicating convergence.

The Explicit finite difference method is conditionally
stable. The stability column indicates whether the chosen
grid satisfies the stability condition.

The Implicit method remains numerically stable for all
grid sizes considered because it is an unconditionally
stable scheme.

The Crank–Nicolson method combines the advantages of the
Explicit and Implicit methods, generally producing highly
accurate and stable option prices.

The convergence results demonstrate that all three methods
approach a consistent numerical solution as the mesh is
refined.
"""
        )


        # ==========================================
        # Recommendations
        # ==========================================

        st.subheader(
            "Recommendation"
        )


        st.info(
        """
For this project:

• Quick Analysis is recommended for testing.

• Standard Analysis provides a good balance
  between computational speed and numerical
  accuracy.

• Detailed Analysis should be used only when
  a more refined convergence study is required.
"""
        )
