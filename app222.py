import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from crank_nicolson import crank_nicolson_american_put


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Benchmark Convergence",
    layout="wide"
)

st.title("Benchmark Convergence Analysis")

st.write("""
This application determines a suitable numerical benchmark for the
American put option by solving the problem using the Crank–Nicolson
finite difference method on increasingly finer grids.

The benchmark is selected automatically once the option price
converges within the chosen tolerance.
""")


# =====================================================
# Option Parameters
# =====================================================

st.sidebar.header("Option Parameters")

K = st.sidebar.number_input(
    "Strike Price (K)",
    value=100.0
)

S0 = st.sidebar.number_input(
    "Initial Stock Price (S0)",
    value=100.0
)

T = st.sidebar.number_input(
    "Time to Maturity (T)",
    value=1.0
)

r = st.sidebar.number_input(
    "Risk-Free Rate",
    value=0.05,
    format="%.4f"
)

sigma = st.sidebar.number_input(
    "Volatility",
    value=0.20,
    format="%.4f"
)


# =====================================================
# Convergence Settings
# =====================================================

st.sidebar.header("Convergence Settings")

max_M = st.sidebar.selectbox(
    "Maximum Space Steps (M)",
    [100,200,300,400,500],
    index=1
)

step = st.sidebar.selectbox(
    "Grid Increment",
    [25,50],
    index=0
)

ratio = st.sidebar.number_input(
    "N / M Ratio",
    value=10
)

tolerance = st.sidebar.number_input(
    "Convergence Tolerance",
    value=1e-6,
    format="%.1e"
)


# =====================================================
# Generate Grid Sizes
# =====================================================

grid_sizes = []

for M in range(step, max_M + step, step):

    N = int(M * ratio)

    grid_sizes.append((M, N))


# =====================================================
# Run Analysis
# =====================================================

if st.button("Run Benchmark Convergence"):

    results = []

    progress = st.progress(0)

    previous_price = None

    benchmark_price = None
    benchmark_M = None
    benchmark_N = None

    converged = False

    for i, (M, N) in enumerate(grid_sizes):

        price, _, _ = crank_nicolson_american_put(
            K,
            S0,
            T,
            r,
            sigma,
            M,
            N
        )

        if previous_price is None:

            difference = None

        else:

            difference = abs(price - previous_price)

            if (not converged) and (difference < tolerance):

                benchmark_price = price
                benchmark_M = M
                benchmark_N = N

                converged = True

        results.append({

            "M": M,
            "N": N,
            "Option Price": price,
            "Difference": difference

        })

        previous_price = price

        progress.progress((i + 1) / len(grid_sizes))


    # =====================================================
    # Results Table
    # =====================================================

    df = pd.DataFrame(results)

    st.subheader("Convergence Results")

    st.dataframe(
        df,
        use_container_width=True
    )


    # =====================================================
    # Plot
    # =====================================================

    fig, ax = plt.subplots(figsize=(8,5))

    ax.plot(
        df["M"],
        df["Option Price"],
        marker="o"
    )

    ax.set_xlabel("Space Steps (M)")

    ax.set_ylabel("Option Price")

    ax.set_title("Crank–Nicolson Convergence")

    ax.grid(True)

    st.pyplot(fig)


    # =====================================================
    # Benchmark Selection
    # =====================================================

    if converged:

        st.success(f"""
Benchmark successfully identified.

Reference Option Price : {benchmark_price:.8f}

Grid Used

M = {benchmark_M}

N = {benchmark_N}

Tolerance = {tolerance:.1e}
""")

    else:

        st.warning("""
The option value did not converge within the chosen tolerance.

Consider:

• Increasing the maximum grid size.

• Increasing the N/M ratio.

• Relaxing the convergence tolerance.
""")


    # =====================================================
    # Download Results
    # =====================================================

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Convergence Results",
        csv,
        file_name="benchmark_convergence.csv",
        mime="text/csv"
    )
