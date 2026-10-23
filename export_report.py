import streamlit as st
import pandas as pd
from reportlab.platypus import Image
import os
import inspect

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Preformatted
)

from reportlab.lib.styles import getSampleStyleSheet



# =====================================================
# Generate Academic PDF Report
# =====================================================


def generate_pdf(
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


    buffer = BytesIO()


    doc = SimpleDocTemplate(
        buffer,
        title="American Put Option Pricing Using Finite Difference Methods"
    )


    styles = getSampleStyleSheet()


    content = []



    # =====================================================
    # Title
    # =====================================================


    content.append(
        Paragraph(
            "American Put Option Pricing Using Finite Difference Methods",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    content.append(
        Paragraph(
            "Developer: Milliano Benjamin Kadzilawa",
            styles["Normal"]
        )
    )


    content.append(
        Spacer(1,30)
    )



    # =====================================================
    # Introduction
    # =====================================================


    content.append(
        Paragraph(
            "1. Introduction",
            styles["Heading2"]
        )
    )


    content.append(
        Paragraph(
        """
American options allow the holder the right to exercise the option
before maturity. Unlike European options, American options generally
do not have closed-form solutions; therefore numerical methods are
required.

This project applies three finite difference methods for pricing an
American put option:
Explicit, Implicit and Crank-Nicolson methods.
""",
        styles["Normal"]
        )
    )



    # =====================================================
    # Mathematical Model
    # =====================================================


    content.append(
        Paragraph(
            "2. Mathematical Model",
            styles["Heading2"]
        )
    )


    content.append(
        Paragraph(
        """
The option price satisfies the Black-Scholes partial differential
equation:

∂V/∂t + 0.5σ²S²(∂²V/∂S²) + rS(∂V/∂S) - rV = 0

The terminal payoff condition is:

V(S,T)=max(K-S,0)

The American early exercise constraint is:

V(S,t)=max(V(S,t),K-S)
""",
        styles["Normal"]
        )
    )



    # =====================================================
    # Parameters
    # =====================================================


    content.append(
        Paragraph(
            "3. Model Parameters",
            styles["Heading2"]
        )
    )


    parameters = [
        ["Parameter","Value"],
        ["Strike Price (K)",str(K)],
        ["Initial Stock Price (S0)",str(S0)],
        ["Maturity (T)",str(T)],
        ["Risk Free Rate",str(r)],
        ["Volatility",str(sigma)],
        ["Space Steps (M)",str(M)],
        ["Time Steps (N)",str(N)]
    ]


    table = Table(parameters)


    table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None)
            ]
        )
    )


    content.append(table)

    content.append(
        Spacer(1,20)
    )



    # =====================================================
    # Results
    # =====================================================


    explicit_price,_,_ = explicit_american_put(
        K,S0,T,r,sigma,M,N
    )


    implicit_price,_,_ = implicit_american_put(
        K,S0,T,r,sigma,M,N
    )


    cn_price,_,_ = crank_nicolson_american_put(
        K,S0,T,r,sigma,M,N
    )


    content.append(
        Paragraph(
            "4. Numerical Results",
            styles["Heading2"]
        )
    )


    results = [
        ["Method","Option Price"],
        ["Explicit",f"{explicit_price:.6f}"],
        ["Implicit",f"{implicit_price:.6f}"],
        ["Crank-Nicolson",f"{cn_price:.6f}"]
    ]


    result_table = Table(results)


    result_table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None)
            ]
        )
    )


    content.append(result_table)
   # ==========================================
# Convergence Analysis
# ==========================================
    # ==========================================
    # Convergence Analysis
    # ==========================================

    content.append(
        Paragraph(
            "5. Convergence Analysis",
            styles["Heading2"]
        )
    )


    if "convergence_results" in st.session_state:


        convergence_df = st.session_state[
            "convergence_results"
        ]


        convergence_data = [
            list(convergence_df.columns)
        ]


        for row in convergence_df.values.tolist():

            convergence_data.append(
                [str(x) for x in row]
            )


        convergence_table = Table(
            convergence_data
        )


        convergence_table.setStyle(
            TableStyle(
                [
                    ("GRID",(0,0),(-1,-1),0.5,None)
                ]
            )
        )


        content.append(
            convergence_table
        )


    else:

        content.append(
            Paragraph(
                """
Convergence analysis was not executed.
Run the convergence analysis before
generating the report.
""",
                styles["Normal"]
            )
        )



    # ==========================================
    # Convergence Plot
    # ==========================================

    content.append(
        Spacer(1,20)
    )


    content.append(
        Paragraph(
            "Convergence Plot",
            styles["Heading3"]
        )
    )


    if os.path.exists("convergence_plot.png"):


        img = Image(
            "convergence_plot.png",
            width=400,
            height=250
        )


        content.append(
            img
        )


    else:


        content.append(
            Paragraph(
                """
Convergence plot was not available.
Run convergence analysis before
generating the report.
""",
                styles["Normal"]
            )
        )
  

    # =====================================================
    # Analysis
    # =====================================================
    # =====================================================
    # Method Comparison Analysis
    # =====================================================
    # =====================================================
    # Method Comparison Analysis
    # =====================================================

    content.append(
        Paragraph(
            "6. Method Comparison Analysis",
            styles["Heading2"]
        )
    )


    if "comparison_results" in st.session_state:

        comparison_df = st.session_state["comparison_results"]

        comparison_data = [list(comparison_df.columns)]

        for row in comparison_df.values.tolist():
            comparison_data.append([str(x) for x in row])

        comparison_table = Table(comparison_data)

        comparison_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, None)
                ]
            )
        )

        content.append(comparison_table)

        content.append(
            Spacer(1,20)
        )

        # ==========================================
        # Recommendation
        # ==========================================

        content.append(
            Paragraph(
                "Method Selection Recommendation",
                styles["Heading3"]
            )
        )

        recommendation = st.session_state["comparison_recommendation"]

        content.append(
            Paragraph(
                recommendation.replace("\n","<br/>"),
                styles["Normal"]
            )
        )

        # ==========================================
        # Accuracy Plot
        # ==========================================

        content.append(
            Spacer(1,20)
        )

        content.append(
            Paragraph(
                "Accuracy Comparison",
                styles["Heading3"]
            )
        )

        if os.path.exists("accuracy_comparison.png"):

            img = Image(
                "accuracy_comparison.png",
                width=400,
                height=250
            )

            content.append(img)

        else:

            content.append(
                Paragraph(
                    "Accuracy comparison plot was not available.",
                    styles["Normal"]
                )
            )

        # ==========================================
        # Runtime Plot
        # ==========================================

        content.append(
            Spacer(1,20)
        )

        content.append(
            Paragraph(
                "Computational Efficiency",
                styles["Heading3"]
            )
        )

        if os.path.exists("runtime_comparison.png"):

            img = Image(
                "runtime_comparison.png",
                width=400,
                height=250
            )

            content.append(img)

        else:

            content.append(
                Paragraph(
                    "Runtime comparison plot was not available.",
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                """
Method comparison was not executed.
Run the comparison analysis before generating the report.
""",
                styles["Normal"]
            )
            )

    
    
            

    # =====================================================
    # Appendix - Source Code
    # =====================================================
    content.append(
    PageBreak()
    )
    

    content.append(
        Paragraph(
            "Appendix: Numerical Method Source Code",
            styles["Heading2"]
        )
    )


    methods = [
        (
            "Explicit Finite Difference Method",
            explicit_american_put
        ),

        (
            "Implicit Finite Difference Method",
            implicit_american_put
        ),

        (
            "Crank-Nicolson Method",
            crank_nicolson_american_put
        )
    ]



    for title, method in methods:


        content.append(
            Paragraph(
                title,
                styles["Heading3"]
            )
        )


        code = inspect.getsource(method)


        content.append(
            Preformatted(
                code,
                styles["Code"]
            )
        )


        content.append(
            Spacer(1,20)
        )



    doc.build(content)


    buffer.seek(0)


    return buffer

        
# =====================================================
# Export Tab
# =====================================================


def export_report_tab(
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


    st.header(
        "Generate Academic Report"
    )


    st.write(
    """
Generate a PDF report suitable for submission.
The report contains the mathematical formulation,
results and numerical method appendix.
"""
    )


    if st.button("Generate Report"):


        pdf = generate_pdf(
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


        st.download_button(
            "Download PDF",
            pdf,
            file_name="American_Put_FDM_Report.pdf",
            mime="application/pdf"
        )
