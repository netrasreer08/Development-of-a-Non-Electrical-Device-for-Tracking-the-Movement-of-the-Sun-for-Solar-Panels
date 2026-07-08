import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

st.title("Solar Panel Sun Tracking System")
theme = st.selectbox(
    "Select Dashboard Theme",
    ["Dark Mode", "Light Mode"]
)

st.write(f"Current Theme:, {theme}")
if theme == "Light Mode":
    st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: black;
    }

    button {
        background-color: #f0f0f0 !important;
        color: black !important;
    }

    .stSelectbox, .stButton, .stTextInput, .stNumberInput {
        color: black !important;
    }

    </style>
    """, unsafe_allow_html=True)
st.header("Project Description")
st.info(
    "Solar energy is renewable, clean, and reduces carbon emissions."
)
if st.button("Complete Simulation"):
    st.balloons()
st.subheader("System Architecture")

st.code("""
Sun Position Data
       ↓
Python Processing
       ↓
Efficiency Calculation
       ↓
Graph Generation
       ↓
Dashboard Output
""")
st.subheader("Project Objectives")

st.write("""
1. Simulate solar tracking.
2. Compare fixed and tracking panels.
3. Calculate efficiency.
4. Improve solar energy utilization.
""")
st.write("""
This project simulates a solar tracking system.
The panel follows the sun throughout the day,
improving efficiency compared to a fixed panel.
""")

current_time = datetime.now().strftime("%H:%M:%S")
st.write("Current Time:", current_time)
current_hour = datetime.now().hour

if 6 <= current_hour <= 18:
    st.success("☀️ Day Time - Solar Generation Active")
else:
    st.error("🌙 Night Time - No Solar Generation")
today = date.today()
st.write("Date:", today)
df = pd.read_csv("solar_data.csv")
selected_time = st.selectbox(
    "Select Time",
    df["Time"]
)
if selected_time < 12:
    st.write("🌅 Sun Position: East")
elif selected_time == 12:
    st.write("☀️ Sun Position: Overhead")
else:
    st.write("🌇 Sun Position: West")
weather = st.selectbox(
    "Weather Condition",
    ["Sunny", "Cloudy", "Rainy"]
)

if weather == "Sunny":
    weather_efficiency = 100
elif weather == "Cloudy":
    weather_efficiency = 70
else:
    weather_efficiency = 40

st.write(
    "Weather Based Efficiency:",
    weather_efficiency,
    "%"
)

row = df[df["Time"] == selected_time]

st.write(
    "Sun Angle:",
    row["Sun_Angle"].values[0],
    "degrees"
)
if selected_time < 12:
    st.success("Morning - Sun in East")

elif selected_time == 12:
    st.success("Noon - Maximum Sunlight")

else:
    st.success("Evening - Sun in West")
fixed_angle = 90

df["Tracking_Panel_Angle"] = df["Sun_Angle"]

df["Fixed_Efficiency"] = (
    100 - abs(df["Sun_Angle"] - fixed_angle) * 100 / 180
)

df["Tracking_Efficiency"] = 100
df["Energy_Generated"] = (
    df["Tracking_Efficiency"] * 10
)
st.subheader("Solar Data")
st.dataframe(df)
st.subheader("Statistics")

st.write("Total Records:", len(df))
st.write("Maximum Sun Angle:", df["Sun_Angle"].max())
st.write("Minimum Sun Angle:", df["Sun_Angle"].min())
fixed_avg = df["Fixed_Efficiency"].mean()
tracking_avg = df["Tracking_Efficiency"].mean()

st.subheader("Power Generation Calculator")

panel_area = st.number_input(
    "Panel Area (m²)",
    value=10
)

power = panel_area * tracking_avg * 0.1

st.write(
    "Estimated Power Generation:",
    round(power, 2),
    "Watts"
)
st.subheader("Monthly Energy Estimation")

monthly_energy = power * 30

st.write(
    "Estimated Monthly Energy:",
    round(monthly_energy,2),
    "Watts"
)
energy = power

co2_saved = energy * 0.0007
st.subheader("Future Prediction")

future_energy = power * 1.05

st.write(
    "Tomorrow Estimated Energy:",
    round(future_energy,2),
    "Watts"
)
st.subheader("Environmental Impact")

st.write(
    "Estimated CO₂ Saved:",
    round(co2_saved,2),
    "kg"
)
st.subheader("Cost Savings Estimation")
st.subheader("Battery Storage")

battery = st.slider(
    "Battery Charge (%)",
    0,
    100,
    75
)

st.write(
    "Current Battery Level:",
    battery,
    "%"
)
electricity_rate = st.number_input(
    "Electricity Rate (₹ per unit)",
    value=8
)

daily_savings = power * electricity_rate / 1000

st.write(
    "Estimated Daily Savings: ₹",
    round(daily_savings, 2)
)
best_time = df.loc[
    df["Fixed_Efficiency"].idxmax(),
    "Time"
]

st.success(
    f"Maximum Fixed Panel Efficiency occurs at {best_time}:00 Hours"
)
st.subheader("Efficiency Bar Chart")

st.bar_chart(
    df[
        [
            "Fixed_Efficiency",
            "Tracking_Efficiency"
        ]
    ]
)
fixed_avg = df["Fixed_Efficiency"].mean()
tracking_avg = df["Tracking_Efficiency"].mean()

fig2, ax2 = plt.subplots()

ax2.pie(
    [fixed_avg, tracking_avg],
    labels=["Fixed", "Tracking"],
    autopct="%1.1f%%"
)

ax2.set_title("Efficiency Distribution")

st.pyplot(fig2)
fixed_avg = df["Fixed_Efficiency"].mean()
tracking_avg = df["Tracking_Efficiency"].mean()
st.metric(
    label="Tracking Efficiency",
    value=f"{tracking_avg:.2f}%"
)
st.subheader("Solar Panel Health")

if tracking_avg >= 90:
    st.success("Panel Health: Excellent")
elif tracking_avg >= 70:
    st.warning("Panel Health: Good")
else:
    st.error("Panel Health: Poor")
st.subheader("Efficiency Level")

st.progress(int(tracking_avg))
if tracking_avg > 90:
    st.success("Solar System Performance: Excellent")

elif tracking_avg > 70:
    st.warning("Solar System Performance: Good")

else:
    st.error("Solar System Performance: Poor")
st.write("Fixed Panel Efficiency:", round(fixed_avg, 2), "%")
st.write("Tracking Panel Efficiency:", round(tracking_avg, 2), "%")

fig, ax = plt.subplots()

ax.plot(df["Time"], df["Fixed_Efficiency"], marker="o", label="Fixed Panel")
ax.plot(df["Time"], df["Tracking_Efficiency"], marker="o", label="Tracking Panel")

ax.set_title("Efficiency Comparison")
ax.set_xlabel("Time")
ax.set_ylabel("Efficiency (%)")
ax.legend()
ax.grid(True)

st.pyplot(fig)
csv = df.to_csv(index=False)

st.download_button(
    "Download Report",
    csv,
    "solar_report.csv",
    "text/csv"
)
st.subheader("Project Summary")
st.subheader("Solar Tips")

st.info(
    "Keep solar panels clean to improve efficiency."
)
st.subheader("Project Score")

score = 100

st.progress(score)

st.write(
    "System Performance Score:",
    score,
    "/100"
)
st.write(f"""
Fixed Panel Efficiency : {fixed_avg:.2f} %

Tracking Panel Efficiency : {tracking_avg:.2f} %

The tracking system provides better efficiency
than the fixed solar panel.
""")
st.subheader("Conclusion")

st.write("""
The solar tracking panel maintains alignment with the sun,
resulting in higher efficiency compared to a fixed solar panel.
This simulation demonstrates the benefits of solar tracking systems.
""")
st.subheader("Project Information")

st.write("Project: Solar Panel Sun Tracking System")
st.write("Department: Computer Science Engineering")
st.write("Technology: Python, Pandas, Matplotlib, Streamlit")
st.subheader("System Status")

st.success("✓ Solar Tracking Active")
st.success("✓ Efficiency Calculation Completed")
st.success("✓ Power Generation Calculated")
st.success("✓ Environmental Impact Calculated")
if st.button("Generate Completion Certificate"):
    st.success(
        "Solar Tracking Simulation Completed Successfully!"
    )
    st.balloons()