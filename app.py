import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import time

# Function to simulate data streaming
def simulate_data_stream(df, delay=1):
    while True:
        current_length = min(st.session_state.index + 1, len(df))
        st.session_state.index = current_length  # Update the index in the session state
        yield df.iloc[:current_length]
        time.sleep(delay)

# Read the CSV file into a DataFrame
file_path = "HomeC_sampled.csv"  # Update to your file path
df = pd.read_csv(file_path)

# Convert the 'time' column to a more readable date format
df['date'] = pd.to_datetime(df['time'], unit='s')
df.sort_values('date', inplace=True)

# Streamlit Page Configurations
st.set_page_config(page_title="Energy Consumption Analysis", layout="wide")

# Initialize session state variables
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'simulate' not in st.session_state:
    st.session_state.simulate = False

# Title of the application
st.title("Home Energy Consumption Analysis")

st.markdown("""
This application provides an analysis of home energy consumption and the relationship between energy usage and weather conditions.
""")

# Sidebar
if st.sidebar.button('Start/Stop Simulation'):
    st.session_state.simulate = not st.session_state.simulate  # Toggle the simulation state

# Real-time Energy Consumption Visualization
st.header("Real-time Energy Consumption Visualization")
st.markdown("This chart simulates real-time data updates for energy consumption.")
real_time_chart_placeholder = st.empty()

# Select a single energy type for real-time simulation
energy_column = 'use [kW]'  # The energy usage column you want to display in real-time

# Check if simulation should be running
if st.session_state.simulate:
    for subset_df in simulate_data_stream(df):
        fig = px.line(subset_df, x='date', y=energy_column, labels={'x': 'Date', 'y': 'Energy Use [kW]'}, title="Real-time Energy Consumption")
        real_time_chart_placeholder.plotly_chart(fig, use_container_width=True)


# Select columns containing '[kW]'
energy_columns = [col for col in df.columns if '[kW]' in col]
# Group by date and calculate the average
df['date'] = df['date'].dt.date
avg_consumption_per_day = df.groupby('date')[energy_columns].mean()

# Visualization for Objective 1
for column in energy_columns:
    fig = px.line(avg_consumption_per_day, x=avg_consumption_per_day.index, y=column, labels={'x': 'Date', 'y': 'Average kW'}, title=f'Average Daily {column.replace(" [kW]", "")}')
    st.plotly_chart(fig)

# Objective 2: Correlation Analysis Between Weather and Energy Usage
st.header("Correlation Analysis Between Weather and Energy Usage")
st.markdown("""
The following section showcases the correlation between various weather variables and the overall energy usage (in kW) in the home.
""")

weather_columns = ['temperature', 'humidity', 'visibility', 'windSpeed', 'precipIntensity', 'dewPoint']
energy_column = 'use [kW]'  # The energy usage column

# Calculate correlations
correlations = {col: df[energy_column].corr(df[col]) for col in weather_columns}

# Convert the correlations to a DataFrame for visualization
correlation_df = pd.DataFrame(list(correlations.items()), columns=['Weather Variable', 'Correlation'])

# Displaying the correlation values
st.dataframe(correlation_df)

# Plotting the correlations
st.subheader("Correlation Plot")
fig = px.bar(correlation_df, x='Weather Variable', y='Correlation', color='Correlation', labels={'Correlation': 'Correlation with Energy Usage'}, title="Correlation between Weather Variables and Energy Usage")
st.plotly_chart(fig)
