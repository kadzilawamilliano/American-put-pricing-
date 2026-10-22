import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



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
Convergence analysis studies how the numerical solution changes
as the computational grid becomes finer.

A stable finite difference method should approach a consistent
option price as the number of space and time steps increases.
""")


    if st.button("Run Convergence Analysis"):


        # Grid refinement levels

        grids = [
            (25,250),
            (50,500),
            (100,1000),
            (150,1500)
        ]


        results = []


        for M,N in grids:


            # ==================================
            # Explicit Stability Check
            # ==================================

            S_max = 2*K

            dS = S_max / M

            dt = T / N


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



            # ==================================
            # Run Explicit Method
            # ==================================

            explicit_price,_,_ = explicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )



            # ==================================
            # Run Implicit Method
            # ==================================

            implicit_price,_,_ = implicit_american_put(
                K,
                S0,
                T,
                r,
                sigma,
                M,
                N
            )



            # ==================================
            # Run Crank-Nicolson Method
            # ==================================

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
                    explicit_price,
                    explicit_status,
                    implicit_price,
                    cn_price
                ]
            )



        # ==================================
        # Convergence Table
        # ==================================

        convergence_df = pd.DataFrame(
            results,
            columns=[
                "Space Steps (M)",
                "Time Steps (N)",
                "Explicit Price",
                "Explicit Stability",
                "Implicit Price",
                "Crank-Nicolson Price"
            ]
        )


        st.subheader(
            "Convergence Results"
        )


        st.dataframe(
            convergence_df
        )



        # ==================================
        # Convergence Plot
        # ==================================

        fig,ax = plt.subplots(
            figsize=(8,5)
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Explicit Price"],
            marker="o",
            label="Explicit"
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Implicit Price"],
            marker="o",
            label="Implicit"
        )


        ax.plot(
            convergence_df["Space Steps (M)"],
            convergence_df["Crank-Nicolson Price"],
            marker="o",
            label="Crank-Nicolson"
        )



        ax.set_xlabel(
            "Number of Space Steps (M)"
        )


        ax.set_ylabel(
            "Option Price"
        )


        ax.set_title(
            "Finite Difference Method Convergence"
        )


        ax.legend()

        ax.grid(True)


        st.pyplot(fig)



        # ==================================
        # Stability Information
        # ==================================

        st.subheader(
            "Stability Analysis"
        )


        st.write("""
The Explicit finite difference method is conditionally stable.
Its stability depends on the relationship between the time step
and space step sizes.

If the stability condition is violated, the Explicit method may
produce inaccurate or oscillating results.

The Implicit method is unconditionally stable, while the
Crank-Nicolson method provides a balance between stability and
accuracy.
""")
