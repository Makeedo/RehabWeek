import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(1)

# Define sessions
sessions = list(range(1, 13))

# Function to simulate therapy data with red flags
def generate_red_flag_data(patient_id, base_steps, trend, erratic=False, fatigue_drop=False):
    data = []
    for session in sessions:
        step_count = base_steps + trend * session + np.random.randint(-20, 20)
        step_length = 0.45 + 0.01 * session + np.random.normal(0, 0.005)

        # Red Flag: unnatural drop
        if erratic and session in [5, 9]:
            step_count -= np.random.randint(100, 200)

        # Red Flag: fatigue-related drop in later sessions
        if fatigue_drop and session > 8:
            step_count -= np.random.randint(50, 100) + trend * session
            assist_level = max(0, 90 + np.random.randint(-3, 3))
            emg = round(0.2 - 0.01 * session + np.random.uniform(-0.005, 0.005), 3)
        else:
            assist_level = max(0, 90 - session * 5 + np.random.randint(-3, 3))
            emg = round(0.2 + 0.01 * session + np.random.uniform(-0.005, 0.005), 3)

        symmetry = 60 + session * 2 + np.random.randint(-5, 5)
        if fatigue_drop and session > 8:
            symmetry -= np.random.randint(10, 20)

        walking_speed = round(0.4 + 0.02 * session + np.random.uniform(-0.02, 0.02), 2)

        hip_rom = round(30 + 1.5 * session + np.random.normal(0, 1),2)
        knee_rom = round(40 + 1.8 * session + np.random.normal(0, 1),2)

        data.append({
            "Session": session,
            "Step Count": step_count,
            "Average Step Length (m)": step_length,
            "ROM hip (deg)": hip_rom,
            "ROM knee (deg)": knee_rom,
            "Assist Level (%)": assist_level,
            "Step Symmetry (%)": symmetry,
            "Walking Speed (m/s)": walking_speed,
            "EMG Activation (mV)": emg
        })
    df = pd.DataFrame(data)
    df.to_csv(f"Patient_{patient_id}.csv", index=False)

    print(f"CSV file 'Patient_{patient_id}.csv' generated successfully.")

# Generate data for three patients with different red flag patterns
generate_red_flag_data(1, 400, 30, erratic=True)
generate_red_flag_data(2, 350, 25, fatigue_drop=True)
generate_red_flag_data(3, 300, 15)  # Control patient

