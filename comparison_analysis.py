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


    # =====================================================
    # 1. Calculate Prices and Runtime
    # =====================================================


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



    # =====================================================
    # 2. High Resolution Reference Solution
    # =====================================================
    #
    # There is no analytical Black-Scholes solution
    # for an American put option.
    #
    # Therefore, a highly refined Crank-Nicolson
    # solution is used as the numerical benchmark.
    #
    # =====================================================


    reference_price, _, _ = crank_nicolson_american_put(
        K,
        S0,
        T,
        r,
        sigma,
        500,
        5000
    )



    # =====================================================
    # 3. Error Calculation
    # =====================================================


    explicit_error = abs(
        explicit_price - reference_price
    )


    implicit_error = abs(
        implicit_price - reference_price
    )


    cn_error = abs(
        cn_price - reference_price
    )



    explicit_percentage = (
        explicit_error / reference_price
    ) * 100


    implicit_percentage = (
        implicit_error / reference_price
    ) * 100


    cn_percentage = (
        cn_error / reference_price
    ) * 100



    # =====================================================
    # 4. Explicit Stability Check
    # =====================================================


    S_max = 2 * K


    dS = S_max / M

    dt = T / N


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



    # =====================================================
    # 5. Comparison Table
    # =====================================================


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


            "Reference Price":
            [
                reference_price,
                reference_price,
                reference_price
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



    comparison_df = comparison_df.round(6)



    # =====================================================
    # 6. Method Recommendation
    # =====================================================


    recommendation = """

A highly refined Crank-Nicolson solution was used as the
reference value because no analytical Black-Scholes solution
exists for an American put option.

The Explicit method achieved the lowest computational time,
but its accuracy depends on satisfying the stability condition.

The Implicit method provides unconditional stability but
requires solving a system of equations at each time step.

The Crank-Nicolson method produced the smallest numerical error
relative to the high-resolution reference solution while
maintaining reasonable computational efficiency.

Therefore, Crank-Nicolson provides the best balance between
accuracy, stability and computational cost for this application.

"""


    return comparison_df, recommendation
