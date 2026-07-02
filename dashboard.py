
import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="BNPL Compliance Auditor & Loan Portal", layout="wide")

# Title and Header
st.title("🛡️ BNPL Compliance & Loan Portal")
st.markdown("### Real-time Regulatory Compliance Engine (FCA Aligned)")

# Sidebar for Navigation
menu = ["Dashboard", "Loan Application", "Audit Logs"]
choice = st.sidebar.selectbox("Navigation", menu)

# Load data (assuming data/synthetic_transactions.csv exists)
@st.cache_data
def load_data():
    return pd.read_csv('data/synthetic_transactions.csv')

df = load_data()

if choice == "Dashboard":
    st.subheader("System Performance & Regulatory Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("Compliance Rate", f"{round((df['is_compliant'].mean())*100, 2)}%")
    col3.metric("FCA Status", "Compliant", delta="Stable")
    
    st.write("### Regulatory Heatmap (Amount Distribution)")
    st.bar_chart(df['is_compliant'].value_counts())
    
elif choice == "Loan Application":
    st.subheader("Apply for a BNPL Loan")
    with st.form("loan_application_form"):
        customer_name = st.text_input("Customer Name")
        loan_amount = st.number_input("Requested Loan Amount (£)", min_value=100, max_value=200000, value=5000)
        submit_button = st.form_submit_button("Submit Application")
        
        if submit_button:
            with st.spinner('Verifying compliance with FCA regulations...'):
                # Simulate Chaincode Logic
                is_compliant = loan_amount <= 50000
                time.sleep(1.5) # Simulating network latency
                
                if is_compliant:
                    st.success(f"Loan Approved! Amount: £{loan_amount} is within FCA limits.")
                    st.balloons()
                else:
                    st.error(f"Loan Rejected! Amount: £{loan_amount} exceeds the FCA £50,000 threshold.")
                    st.warning("Automated entry logged to immutable ledger.")

elif choice == "Audit Logs":
    st.subheader("Immutable Audit Trail")
    st.write("This log represents the DLT ledger view.")
    st.dataframe(df.head(50))
    
    st.write("### Flagged Transactions (Regulatory Exceptions)")
    st.dataframe(df[df['is_compliant'] == 0].head(10))
