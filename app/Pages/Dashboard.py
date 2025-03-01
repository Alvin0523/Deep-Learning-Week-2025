import streamlit as st
import altair as alt
import requests
import datetime
import pandas as pd

# ==========================================================================
# 1) CONFIG - Hardcoded token for demonstration
# ==========================================================================
ACCESS_TOKEN = " eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1EzNlEiLCJzdWIiOiJDR1hNODQiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcnNldCByaXJuIHJveHkgcm51dCBycHJvIHJzbGUgcmNmIHJhY3QgcnJlcyBybG9jIHJ3ZWkgcmhyIHJ0ZW0iLCJleHAiOjE3NDA4ODg4NzUsImlhdCI6MTc0MDg2MDA3NX0.4aSxoplznL1SnEPVBkDfP_DMUwxjOUoa4pwME4aS_RQ"

# ==========================================================================
# 2) FETCH FUNCTIONS
# ==========================================================================

def fetch_steps(access_token):
    url = "https://api.fitbit.com/1/user/-/activities/steps/date/today/7d.json"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("activities-steps", [])
    else:
        st.error("Error fetching steps data:")
        st.error(resp.text)
        return None

def fetch_heartrate_intraday(access_token):
    url = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error("Error fetching intraday heart rate data:")
        st.error(resp.text)
        return None

def fetch_sleep_data(access_token):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = today.strftime('%Y-%m-%d')
    url = f"https://api.fitbit.com/1.2/user/-/sleep/date/{start_str}/{end_str}.json"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error("Error fetching sleep data:")
        st.error(resp.text)
        return None

def parse_detailed_sleep(sleep_response):
    rows = []
    sleep_logs = sleep_response.get("sleep", [])
    for log in sleep_logs:
        date_of_sleep = log.get("dateOfSleep")
        levels = log.get("levels", {})
        data_entries = levels.get("data", [])
        for entry in data_entries:
            start_str = entry.get("dateTime")
            level = entry.get("level")
            duration_sec = entry.get("seconds", 0)
            start_time = pd.to_datetime(start_str)
            end_time = start_time + datetime.timedelta(seconds=duration_sec)
            rows.append({
                "dateOfSleep": date_of_sleep,
                "level": level,
                "start_time": start_time,
                "end_time": end_time,
                "duration_seconds": duration_sec
            })
    df = pd.DataFrame(rows)
    return df

def sleep_timeline_chart(df):
    chart = alt.Chart(df).mark_bar().encode(
        x='start_time',
        x2='end_time',
        y=alt.Y('dateOfSleep:N', title='Date of Sleep'),
        color=alt.Color('level:N', legend=alt.Legend(title='Stage')),
        tooltip=['dateOfSleep', 'level', 'start_time', 'end_time', 'duration_seconds']
    ).properties(
        width=800,
        height=200
    )
    return chart

def fetch_skin_temperature(access_token):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = today.strftime('%Y-%m-%d')
    url = f"https://api.fitbit.com/1/user/-/temp/skin/date/{start_str}/{end_str}.json"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error("Error fetching skin temperature data:")
        st.error(resp.text)
        return None

def fetch_activity_summary(access_token):
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    url = f"https://api.fitbit.com/1/user/-/activities/date/{today_str}.json"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error("Error fetching activity summary:")
        st.error(resp.text)
        return None

# ==========================================================================
# 2.5) HELPER: DISPLAY ACTIVITY SUMMARY
# ==========================================================================

def display_activity_summary(activity_data):
    """
    Parse out top-level fields and distances from activity_data["summary"].
    """
    summary = activity_data.get("summary", {})
    
    # Display key fields
    st.write("**Steps:**", summary.get("steps"))
    st.write("**Calories Out:**", summary.get("caloriesOut"))
    st.write("**Activity Calories:**", summary.get("activityCalories"))
    st.write("**Sedentary Minutes:**", summary.get("sedentaryMinutes"))
    st.write("**Lightly Active Minutes:**", summary.get("lightlyActiveMinutes"))
    st.write("**Fairly Active Minutes:**", summary.get("fairlyActiveMinutes"))
    st.write("**Very Active Minutes:**", summary.get("veryActiveMinutes"))
    
    # Distances array
    distances = summary.get("distances", [])
    if distances:
        df_distances = pd.DataFrame(distances)
        st.write("**Distances (Various Activity Types):**")
        st.dataframe(df_distances)
        # Optional total distance
        total_distance = sum(d.get("distance", 0) for d in distances)
        st.write("**Total Distance:**", total_distance)
    else:
        st.write("No distance data found.")

# ==========================================================================
# 3) STREAMLIT APP
# ==========================================================================
def main():
    st.title("Fitbit Data Dashboard")

    if not ACCESS_TOKEN or ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        st.warning("Please update the ACCESS_TOKEN with a valid Fitbit token.")
        return

    # -----------------------
    # ROW 1: Steps + Heart Rate
    # -----------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Steps (Last 7 Days)")
        steps_data = fetch_steps(ACCESS_TOKEN)
        if steps_data and len(steps_data) > 0:
            df = pd.DataFrame(steps_data)
            df["dateTime"] = pd.to_datetime(df["dateTime"])
            df["value"] = pd.to_numeric(df["value"])
            df.sort_values("dateTime", inplace=True)
            st.line_chart(df.set_index("dateTime")["value"])
        else:
            st.write("No steps data found or empty response.")

    with col2:
        st.subheader("Heart Rate (Intraday, Today)")
        hr_data = fetch_heartrate_intraday(ACCESS_TOKEN)
        if hr_data and "activities-heart-intraday" in hr_data:
            intraday = hr_data["activities-heart-intraday"]
            dataset = intraday.get("dataset", [])
            if dataset and len(dataset) > 0:
                df_hr = pd.DataFrame(dataset)
                st.line_chart(df_hr.set_index("time")["value"])
            else:
                st.write("No intraday HR data found.")
        else:
            st.write("No intraday HR data or invalid response structure.")

    # -----------------------
    # ROW 2: Sleep Summary + Detailed Timeline
    # -----------------------
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Sleep Logs (Last 7 Days)")
        sleep_resp = fetch_sleep_data(ACCESS_TOKEN)
        parsed_df = None
        if sleep_resp and "sleep" in sleep_resp:
            sleep_list = sleep_resp["sleep"]
            if sleep_list and len(sleep_list) > 0:
                summary_dict = {}
                for log in sleep_list:
                    date_str = log.get("dateOfSleep")
                    minutes = log.get("minutesAsleep", 0)
                    summary_dict[date_str] = summary_dict.get(date_str, 0) + minutes

                df_sleep = pd.DataFrame(
                    [{"date": k, "minutesAsleep": v} for k, v in summary_dict.items()]
                )
                df_sleep["date"] = pd.to_datetime(df_sleep["date"])
                df_sleep.sort_values("date", inplace=True)
                st.bar_chart(df_sleep.set_index("date")["minutesAsleep"])

                # parse detailed
                parsed_df = parse_detailed_sleep(sleep_resp)
            else:
                st.write("No sleep logs found.")
        else:
            st.write("No sleep data or invalid response.")

    with col4:
        st.subheader("Detailed Sleep Timeline")
        if parsed_df is not None and not parsed_df.empty:
            st.dataframe(parsed_df)
            parsed_df.sort_values("start_time", inplace=True)
            timeline = sleep_timeline_chart(parsed_df)
            st.altair_chart(timeline, use_container_width=True)
        else:
            st.write("No detailed segments found for timeline.")

    # -----------------------
    # ROW 3: Skin Temp + Activity Summary
    # -----------------------
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Skin Temperature (Last 7 Days)")
        skin_temp = fetch_skin_temperature(ACCESS_TOKEN)
        if skin_temp and "tempSkin" in skin_temp:
            temp_list = skin_temp["tempSkin"]
            if temp_list and len(temp_list) > 0:
                rows = []
                for entry in temp_list:
                    date_str = entry.get("dateTime")
                    val = entry.get("value", {})
                    temp_val = val.get("temperature")
                    units = val.get("units", "C")
                    rows.append({"date": date_str, "temp": temp_val, "units": units})
                df_temp = pd.DataFrame(rows)
                df_temp["date"] = pd.to_datetime(df_temp["date"])
                df_temp.sort_values("date", inplace=True)
                df_temp = df_temp.dropna(subset=["temp"])
                if not df_temp.empty:
                    st.line_chart(df_temp.set_index("date")["temp"])
                    st.write("Units:", df_temp["units"].iloc[0])
                else:
                    st.write("Skin temperature data is empty or invalid.")
            else:
                st.write("No skin temperature logs found.")
        else:
            st.write("No skin temperature data or invalid response.")

    with col6:
        st.subheader("Activity Summary (Today)")
        activity_data = fetch_activity_summary(ACCESS_TOKEN)
        if activity_data and "summary" in activity_data:
            # Instead of just dumping summary, parse it
            display_activity_summary(activity_data)
       
        else:
            st.write("No activity summary or invalid response.")


# ==========================================================================
# 4) RUN THE APP
# ==========================================================================
if __name__ == "__main__":
    main()
