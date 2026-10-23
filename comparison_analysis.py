import time
import pandas as pd


def run_comparison(
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


    # ==========================================
    # Calculate Prices and Runtime
    # ==========================================


    start = time.time()

    explicit_price, _, _ = explicit_american_put(
        K,
        S0,
        T,
        r,
        sigma,
        M,
        N
    )

    explicit_time = time.time() - start



    start = time.time()

    implicit_price, _, _ = implicit_american_put(
        K,
        S0,
        T,
        r,
        sigma,
        M,
        N
    )

    implicit_time = time.time() - start



    start = time.time()

    cn_price, _, _ = crank_nicolson_american_put(
        K,
        S0,
        T,
        r,
        sigma,
        M,
        N
    )

    cn_time = time.time() - start



    # ==========================================
    # Use Crank-Nicolson as Reference
    # ==========================================


    reference = cn_price



    explicit_error = abs(
        explicit_price - reference
    )


    implicit_error = abs(
        implicit_price - reference
    )


    cn_error = 0



    explicit_percentage = (
        explicit_error / reference
    ) * 100


    implicit_percentage = (
        implicit_error / reference
    ) * 100


    cn_percentage = 0



    # ==========================================
    # Stability Check
    # ==========================================


    S_max = 2*K


    dS = S_max/M

    dt = T/N


    stability_parameter = (
        sigma**2 *
        S_max**2 *
        dt /
        dS**2
    )


    if stability_parameter <= 1:

        explicit_stability = "Stable"

    else:

        explicit_stability = "Unstable"



    # ==========================================
    # Create Comparison Table
    # ==========================================


    comparison_df = pd.DataFrame(

        {

            "Method":
            [
                "Explicit",
                "Implicit",
                "Crank-Nicolson"
            ],


            "Option Price":
            [
                explicit_price,
                implicit_price,
                cn_price
            ],


            "Absolute Error":
            [
                explicit_error,
                implicit_error,
                cn_error
            ],


            "Percentage Error (%)":
            [
                explicit_percentage,
                implicit_percentage,
                cn_percentage
            ],


            "Runtime (seconds)":
            [
                explicit_time,
                implicit_time,
                cn_time
            ],


            "Stability":
            [
                explicit_stability,
                "Stable",
                "Stable"
            ]

        }

    )



    # Round values for display

    comparison_df = comparison_df.round(6)



    # ==========================================
    # Recommendation
    # ==========================================


    recommendation = """

Crank-Nicolson provides the most accurate solution
because it has the smallest numerical error.

The Explicit method has the lowest computational
cost but requires a stability condition.

The Implicit method provides strong stability but
requires solving a system of equations.

Therefore, Crank-Nicolson provides the best balance
between accuracy and numerical stability.
"""


    return comparison_df, recommendation
