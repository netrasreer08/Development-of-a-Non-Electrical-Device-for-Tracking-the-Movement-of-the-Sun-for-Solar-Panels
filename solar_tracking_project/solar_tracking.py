import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("solar_data.csv")

print("Dataset:")
print(df)

# Fixed panel angle
fixed_angle = 90

# Tracking panel follows sun
df["Tracking_Panel_Angle"] = df["Sun_Angle"]
print("\nSolar Tracking System")
print("----------------------")
print("The panel automatically follows the sun.")

# Calculate efficiencies
df["Fixed_Efficiency"] = (
    100 - abs(df["Sun_Angle"] - fixed_angle) * 100 / 180
)

df["Tracking_Efficiency"] = (
    100 - abs(df["Sun_Angle"] - df["Tracking_Panel_Angle"]) * 100 / 180
)

# Display results
print("\nResults:")
print(df)

# Average efficiency
fixed_avg = df["Fixed_Efficiency"].mean()
tracking_avg = df["Tracking_Efficiency"].mean()

print("\nAverage Efficiency")
print("Fixed Panel :", round(fixed_avg, 2), "%")
print("Tracking Panel :", round(tracking_avg, 2), "%")

# Graph
plt.figure(figsize=(8,5))

plt.plot(
    df["Time"],
    df["Fixed_Efficiency"],
    marker='o',
    label="Fixed Panel"
)

plt.plot(
    df["Time"],
    df["Tracking_Efficiency"],
    marker='o',
    label="Tracking Panel"
)

plt.title("Solar Panel Efficiency Comparison")
plt.xlabel("Time")
plt.ylabel("Efficiency (%)")
plt.legend()
plt.grid(True)

plt.show()