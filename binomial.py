import numpy as np


def american_put_binomial(
    K,
    S0,
    T,
    r,
    sigma,
    steps
):

    dt = T / steps

    u = np.exp(sigma * np.sqrt(dt))

    d = 1 / u

    p = (
        np.exp(r * dt) - d
    ) / (
        u - d
    )

    discount = np.exp(-r * dt)


    # -------------------------
    # Stock prices at maturity
    # -------------------------

    stock = np.array(

        [
            S0 * (u ** j) * (d ** (steps - j))
            for j in range(steps + 1)
        ]

    )


    # -------------------------
    # Payoff
    # -------------------------

    option = np.maximum(
        K - stock,
        0
    )


    # -------------------------
    # Backward induction
    # -------------------------

    for i in range(
        steps - 1,
        -1,
        -1
    ):

        stock = stock[:-1] / d

        continuation = discount * (

            p * option[1:]

            +

            (1 - p) * option[:-1]

        )

        exercise = np.maximum(
            K - stock,
            0
        )

        option = np.maximum(
            continuation,
            exercise
        )

    return option[0]
