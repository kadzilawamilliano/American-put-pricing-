import numpy as np


def crank_nicolson_american_put(
    K,
    S0,
    T,
    r,
    sigma,
    M,
    N
):

    # ==========================================
    # Grid Setup
    # ==========================================

    S_max = 2 * K

    dS = S_max / M

    dt = T / N

    stock = np.linspace(
        0,
        S_max,
        M + 1
    )

    option = np.zeros(
        (M + 1, N + 1)
    )

    # ==========================================
    # Terminal Condition
    # ==========================================

    option[:, -1] = np.maximum(
        K - stock,
        0
    )

    # ==========================================
    # Boundary Conditions
    # ==========================================

    option[0, :] = K

    option[M, :] = 0

    # ==========================================
    # Coefficients
    # ==========================================

    j = np.arange(1, M)

    a = 0.25 * dt * (
        sigma**2 * j**2 - r * j
    )

    b = -0.5 * dt * (
        sigma**2 * j**2 + r
    )

    c = 0.25 * dt * (
        sigma**2 * j**2 + r * j
    )

    # ==========================================
    # Left Matrix
    # ==========================================

    A = np.zeros(
        (M - 1, M - 1)
    )

    np.fill_diagonal(
        A,
        1 - b
    )

    np.fill_diagonal(
        A[1:],
        -a[1:]
    )

    np.fill_diagonal(
        A[:, 1:],
        -c[:-1]
    )

    # ==========================================
    # Right Matrix
    # ==========================================

    B = np.zeros(
        (M - 1, M - 1)
    )

    np.fill_diagonal(
        B,
        1 + b
    )

    np.fill_diagonal(
        B[1:],
        a[1:]
    )

    np.fill_diagonal(
        B[:, 1:],
        c[:-1]
    )

    # ==========================================
    # Backward Time Marching
    # ==========================================

    for n in range(N - 1, -1, -1):

        rhs = B @ option[1:M, n + 1]

        rhs[0] += a[0] * (
            option[0, n] +
            option[0, n + 1]
        )

        rhs[-1] += c[-1] * (
            option[M, n] +
            option[M, n + 1]
        )

        option[1:M, n] = np.linalg.solve(
            A,
            rhs
        )

        option[:, n] = np.maximum(
            option[:, n],
            K - stock
        )

    # ==========================================
    # Interpolate Option Price
    # ==========================================

    price = np.interp(
        S0,
        stock,
        option[:, 0]
    )

    return (
        price,
        stock,
        option[:, 0]
    )
