import streamlit as st
import pandas as pd
import requests
import datetime

# ===== Hardcoded Access Token =====
# Replace with your actual valid Fitbit access token (with required scopes).
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1EzNlEiLCJzdWIiOiJDR1hNODQiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcnNldCByaXJuIHJveHkgcm51dCBycHJvIHJzbGUgcmNmIHJhY3QgcnJlcyBybG9jIHJ3ZWkgcmhyIHJ0ZW0iLCJleHAiOjE3NDA4ODU1MjAsImlhdCI6MTc0MDg1NjcyMH0.r3lKKFuB25Dnkr0zpEy6LHb_c5p8kvklWf9y5e84D6w"

# ===== Helper Functions (No OAuth exchange) =====

def fetch_fitbit_steps(access_token):
    """Fetch steps data for the last 7 days."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.fitbit.com/1/user/-/activities/steps/date/today/7d.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("activities-steps", [])
    else:
        st.error("Error fetching Fitbit steps data:")
        st.error(response.text)
        st.stop()

def fetch_fitbit_heart_rate_summary(access_token):
    """
    Fetch daily heart rate summaries for the last 7 days,
    including resting heart rate if available.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.fitbit.com/1/user/-/activities/heart/date/today/7d.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        heart_data = data.get("activities-heart", [])
        summary = []
        for day in heart_data:
            date_str = day.get("dateTime")
            value = day.get("value", {})
            rhr = value.get("restingHeartRate")  # Might be None if not available
            summary.append({"dateTime": date_str, "restingHeartRate": rhr})
        return summary
    else:
        st.error("Error fetching Fitbit heart rate data:")
        st.error(response.text)
        st.stop()

def fetch_fitbit_sleep_summary(access_token):
    """
    Fetch sleep logs for the last 7 days by specifying exact start/end dates.
    """
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = today.strftime('%Y-%m-%d')

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.fitbit.com/1.2/user/-/sleep/date/{start_str}/{end_str}.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("sleep", [])
    else:
        st.error("Error fetching Fitbit sleep data:")
        st.error(response.text)
        st.stop()

def fetch_fitbit_skin_temp(access_token):
    """
    Fetch skin temperature data for the last 7 days.
    Requires 'temperature' scope and a device that measures skin temp.
    """
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = today.strftime('%Y-%m-%d')

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.fitbit.com/1/user/-/temp/skin/date/{start_str}/{end_str}.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("tempSkin", [])
    else:
        st.error("Error fetching Fitbit skin temperature data:")
        st.error(response.text)
        st.stop()

# ===== Streamlit App =====
st.title("Fitbit Data Dashboard (Hardcoded Token)")

# Check if the hardcoded token is non-empty
if not ACCESS_TOKEN or ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
    st.warning("Please update ACCESS_TOKEN with a valid Fitbit token.")
    st.stop()

# ----- LAYOUT: We'll show Steps, Heart Rate, and Skin Temp side by side, then Sleep below. -----
col1, col2, col3 = st.columns(3)

# ----- STEPS DATA -----
with col1:
    st.subheader("Steps (Last 7 Days)")
    steps_data = fetch_fitbit_steps(ACCESS_TOKEN)
    if steps_data:
        steps_df = pd.DataFrame(steps_data)
        steps_df["dateTime"] = pd.to_datetime(steps_df["dateTime"])
        steps_df["value"] = pd.to_numeric(steps_df["value"])
        steps_df.sort_values("dateTime", inplace=True)
        st.line_chart(steps_df.rename(columns={"dateTime": "index"}).set_index("index")["value"])
    else:
        st.write("No steps data found.")

# ----- HEART RATE (RHR) DATA -----
with col2:
    st.subheader("Resting Heart Rate (Last 7 Days)")
    hr_summary = fetch_fitbit_heart_rate_summary(ACCESS_TOKEN)
    if hr_summary:
        hr_df = pd.DataFrame(hr_summary)
        hr_df["dateTime"] = pd.to_datetime(hr_df["dateTime"])
        hr_df.sort_values("dateTime", inplace=True)
        # Filter out any days where restingHeartRate is None
        hr_df = hr_df.dropna(subset=["restingHeartRate"])
        if not hr_df.empty:
            st.line_chart(hr_df.rename(columns={"dateTime": "index"}).set_index("index")["restingHeartRate"])
        else:
            st.write("No resting heart rate data found (possibly none recorded).")
    else:
        st.write("No heart rate data found.")

# ----- SKIN TEMPERATURE DATA -----
with col3:
    st.subheader("Skin Temperature (Last 7 Days)")
    skin_temp_data = fetch_fitbit_skin_temp(ACCESS_TOKEN)
    if skin_temp_data:
        temp_summary = []
        for entry in skin_temp_data:
            date_str = entry.get("dateTime")
            value = entry.get("value", {})
            temp_val = value.get("temperature")  # might be None
            units = value.get("units", "C")      # default to Celsius
            temp_summary.append({
                "dateTime": date_str,
                "temperature": temp_val,
                "units": units
            })

        temp_df = pd.DataFrame(temp_summary)
        temp_df["dateTime"] = pd.to_datetime(temp_df["dateTime"])
        temp_df.sort_values("dateTime", inplace=True)
        temp_df.dropna(subset=["temperature"], inplace=True)

        if not temp_df.empty:
            st.line_chart(temp_df.rename(columns={"dateTime": "index"}).set_index("index")["temperature"])
            st.caption(f"Units: {temp_df['units'].iloc[0] if not temp_df.empty else 'C'}")
        else:
            st.write("No skin temperature data found (possibly none recorded).")
    else:
        st.write("No skin temperature data found.")

# ----- SLEEP DATA (Below the three columns) -----
st.subheader("Sleep Logs (Last 7 Days)")
sleep_logs = fetch_fitbit_sleep_summary(ACCESS_TOKEN)
if sleep_logs:
    # We'll aggregate total minutes asleep by date
    summary = {}
    for log in sleep_logs:
        date_str = log.get("dateOfSleep")
        minutes_asleep = log.get("minutesAsleep", 0)
        if date_str in summary:
            summary[date_str] += minutes_asleep
        else:
            summary[date_str] = minutes_asleep

    # Convert to DataFrame
    sleep_df = pd.DataFrame(
        [{"dateTime": k, "minutesAsleep": v} for k, v in summary.items()]
    )
    sleep_df["dateTime"] = pd.to_datetime(sleep_df["dateTime"])
    sleep_df.sort_values("dateTime", inplace=True)

    st.bar_chart(sleep_df.rename(columns={"dateTime": "index"}).set_index("index")["minutesAsleep"])
    st.write("Total Minutes Asleep by Date:")
    st.dataframe(sleep_df)
else:
    st.write("No sleep data found.")
