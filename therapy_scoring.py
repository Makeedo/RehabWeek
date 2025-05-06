import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

st.title("Exoskeleton Therapy Progress Dashboard")

@st.cache_data
def load_data():
    url = "exoskeleton_therapy_sample_data.csv"
    return pd.read_csv(url)

df = load_data()

# Show raw data
with st.expander("Show raw dataset"):
    st.dataframe(df)

# Select one or more metrics
metrics = [col for col in df.columns if col != "Session"]
selected_metrics = st.multiselect("Select metrics to visualize:", metrics, default=[metrics[0]])

# Plot selected metrics over sessions
st.subheader("Selected Metrics Over Time")
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))
for metric in selected_metrics:
    sns.lineplot(data=df, x="Session", y=metric, marker="o", label=metric, ax=ax)
ax.set_xlabel("Session")
ax.set_ylabel("Value")
ax.legend()
st.pyplot(fig)

# Session comparison with radar chart
st.subheader("Compare Two Sessions (Radar Chart)")
session_options = df["Session"].tolist()
session1 = st.selectbox("Select Session 1", session_options, index=0)
session2 = st.selectbox("Select Session 2", session_options, index=len(session_options)-1)

def radar_chart(data, session1, session2, metrics):

    s1_data = data[data["Session"] == session1][metrics].values.flatten()
    s2_data = data[data["Session"] == session2][metrics].values.flatten()

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=s1_data, theta=metrics, fill='toself', name=f"Session {session1}"))
    fig.add_trace(go.Scatterpolar(r=s2_data, theta=metrics, fill='toself', name=f"Session {session2}"))

    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    return fig

radar_metrics = st.multiselect("Metrics for Radar Chart", metrics, default=metrics[:5])
if radar_metrics:
    radar_fig = radar_chart(df, session1, session2, radar_metrics)
    st.plotly_chart(radar_fig, use_container_width=True)

# Correlation matrix
st.subheader("Correlation Between Metrics")
corr_matrix = df[metrics].corr()
fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax_corr)
st.pyplot(fig_corr)

# Improvement summary
st.subheader("Improvement Summary")
improvements = {}
for metric in metrics:
    first = df[metric].iloc[0]
    last = df[metric].iloc[-1]
    improvement = ((last - first) / first) * 100
    improvements[metric] = round(improvement, 2)
improvement_df = pd.DataFrame(list(improvements.items()), columns=["Metric", "Percent Improvement"])
st.dataframe(improvement_df.sort_values(by="Percent Improvement", ascending=False))