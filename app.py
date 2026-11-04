
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Smart Patient Monitoring",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Smart Patient Health Monitoring System")
st.write("Educational Patient Health Analytics Dashboard")

np.random.seed(42)
n = 100

df = pd.DataFrame({
    "Patient_ID": [f"P{i:03d}" for i in range(1, n + 1)],
    "Age": np.random.randint(18, 85, n),
    "Heart_Rate": np.random.randint(55, 121, n),
    "Systolic_BP": np.random.randint(90, 181, n),
    "Diastolic_BP": np.random.randint(60, 111, n),
    "SpO2": np.random.randint(88, 101, n),
    "Temperature": np.round(np.random.uniform(36, 39.5, n), 1)
})

df["Status"] = np.where(
    (df["Heart_Rate"] < 60) |
    (df["Heart_Rate"] > 100) |
    (df["Systolic_BP"] > 140) |
    (df["Diastolic_BP"] > 90) |
    (df["SpO2"] < 95) |
    (df["Temperature"] > 38),
    "Needs Review",
    "Within Set Limits"
)

st.subheader("Patient Overview")

c1, c2, c3 = st.columns(3)
c1.metric("Total Patients", len(df))
c2.metric("Needs Review", int((df["Status"] == "Needs Review").sum()))
c3.metric("Within Set Limits", int((df["Status"] == "Within Set Limits").sum()))

st.subheader("Patient Records")
st.dataframe(df, use_container_width=True)

st.subheader("Heart Rate Distribution")
fig = px.histogram(df, x="Heart_Rate")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Patient Search")
patient_id = st.text_input("Enter Patient ID (Example: P001)")

if patient_id:
    result = df[df["Patient_ID"] == patient_id.upper()]
    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("Patient ID not found")

st.download_button(
    "Download Patient Report",
    df.to_csv(index=False),
    "patient_report.csv",
    "text/csv"
)

st.caption("Educational prototype using synthetic data only. Not for clinical use.")
