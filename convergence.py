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
    M,
    N,
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

    analysis_level = st.selectbox(
        "Select Analysis Level",
        [
            "Quick",
            "Standard",
            "Detailed"
        ]
    )


    # User selected maximum grid

    max_M = int(M)

    max_N = int(N)


    # Limit convergence computation

    max_M = min(max_M,120)

    max_N = min(max_N,600)



    if analysis_level == "Quick":

        grids = [

            (
                max(10,max_M//4),
                max(50,max_N//4)
            ),

            (
                max(20,max_M//2),
                max(100,max_N//2)
            ),

            (
                max_M,
                max_N
            )

        ]


    elif analysis_level == "Standard":

        grids = [

            (
                max(10,max_M//4),
                max(50,max_N//4)
            ),

            (
                max(20,max_M//2),
                max(100,max_N//2)
            ),

            (
                max(30,(3*max_M)//4),
                max(150,(3*max_N)//4)
            ),

            (
                max_M,
                max_N
            )

        ]


    else:

        grids = [

            (
                max(10,max_M//5),
                max(40,max_N//5)
            ),

            (
                max(20,(2*max_M)//5),
                max(80,(2*max_N)//5)
            ),

            (
                max(30,(3*max_M)//5),
                max(120,(3*max_N)//5)
            ),

            (
                max(40,(4*max_M)//5),
                max(160,(4*max_N)//5)
            ),

            (
                max_M,
                max_N
            )

        ]



    st.info(
f"""
Analysis Level: {analysis_level}

Maximum Grid:

Space Steps (M): {max_M}

Time Steps (N): {max_N}

The convergence study automatically creates
progressively finer grids.
"""
    )


    st.subheader("Grid Levels")


    grid_df = pd.DataFrame(
        grids,
        columns=[
            "Space Steps (M)",
            "Time Steps (N)"
        ]
    )


    st.dataframe(
        grid_df,
        use_container_width=True
    )



    if st.button("Run Convergence Analysis"):


        start = time.time()


        progress = st.progress(0)

        status = st.empty()

        table_placeholder = st.empty()


        results = []


        total = len(grids)



        for index,(M_grid,N_grid) in enumerate(grids):


            status.write(
                f"""
Running grid {index+1}/{total}

M = {M_grid}

N = {N_grid}
"""
            )


            # ==================================
            # Stability Check
            # ==================================

            S_max = 2*K

            dS = S_max/M_grid

            dt = T/N_grid


            stability_parameter = (
                sigma**2 *
                S_max**2 *
                dt /
                dS**2
            )


            if stability_parameter <= 1:

                explicit_status = "Stable"

            else:

                explicit_status = "Unstable"



            # ==================================
            # Explicit
            # ==================================

            explicit_price,_,_ = explicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M_grid,
                N_grid
            )


            # ==================================
            # Implicit
            # ==================================

            implicit_price,_,_ = implicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M_grid,
                N_grid
            )


            # ==================================
            # Crank Nicolson
            # ==================================

            cn_price,_,_ = crank_nicolson_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M_grid,
                N_grid
            )
                        # ==================================
            # Store Results
            # ==================================

            results.append(
                [
                    M_grid,
                    N_grid,
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


            # Update table while running

            table_placeholder.dataframe(
                convergence_df,
                use_container_width=True
            )
                        # Save convergence results for PDF export

            st.session_state["convergence_results"] = convergence_df


            progress.progress(
                (index+1)/total
            )


        # ==================================
        # Completion
        # ==================================

        end = time.time()

        runtime = end-start


        status.success(
            "Convergence analysis completed successfully."
        )


        st.success(
            f"Execution Time: {runtime:.2f} seconds"
        )



        # ==================================
        # Summary
        # ==================================

        st.subheader(
            "Final Grid Results"
        )


        col1,col2,col3 = st.columns(3)


        with col1:

            st.metric(
                "Explicit",
                f"{convergence_df['Explicit'].iloc[-1]:.6f}"
            )


        with col2:

            st.metric(
                "Implicit",
                f"{convergence_df['Implicit'].iloc[-1]:.6f}"
            )


        with col3:

            st.metric(
                "Crank-Nicolson",
                f"{convergence_df['Crank-Nicolson'].iloc[-1]:.6f}"
            )



        # ==================================
        # Convergence Plot
        # ==================================

        st.subheader(
            "Convergence Plot"
        )


        fig,ax = plt.subplots(
            figsize=(9,5)
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Explicit"],
            marker="o",
            label="Explicit"
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Implicit"],
            marker="s",
            label="Implicit"
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Crank-Nicolson"],
            marker="^",
            label="Crank-Nicolson"
        )


        ax.set_xlabel(
            "Space Steps (M)"
        )


        ax.set_ylabel(
            "Option Price"
        )


        ax.set_title(
            "Finite Difference Method Convergence"
        )


        ax.grid(True)

        ax.legend()


        st.pyplot(fig)
                st.pyplot(fig)


        # Save convergence plot for PDF report

        fig.savefig(
            "convergence_plot.png",
            bbox_inches="tight"
        )


        # ==================================
        # Download CSV
        # ==================================

        csv = convergence_df.to_csv(
            index=False
        )



        # ==================================
        # Download CSV
        # ==================================

        csv = convergence_df.to_csv(
            index=False
        )


        st.download_button(

            label="Download Convergence Results",

            data=csv,

            file_name="convergence_results.csv",

            mime="text/csv"

        )



        # ==================================
        # Interpretation
        # ==================================

        st.subheader(
            "Interpretation"
        )


        st.write(
        """
As the number of grid points increases, the numerical
solutions approach a stable value, demonstrating convergence.

The Explicit finite difference method is conditionally stable,
therefore the stability condition is checked for every grid.

The Implicit method is unconditionally stable because it solves
a system of equations at each time step.

The Crank-Nicolson method combines Explicit and Implicit schemes,
providing improved accuracy and stability.

For this project, the Standard analysis level provides a good
balance between computational efficiency and convergence
demonstration.
"""
        )
