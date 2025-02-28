import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.utils import clean_data, generate_alerts
from app.optimisation import find_optimal_batch



# --- Load Data ---
@st.cache_data
def load_data():
    try:
        # Skip rows until the main data table starts
        df = pd.read_csv("data/calibration_data.csv", skiprows=10, header=None) #set header to none.
        #Remove all rows with all null values.
        df = df.dropna(how = "all")

        # Set the correct column names.
        df.columns = ['Div', 'Description', 'Brand', 'Tag', 'Model', 'Serial', 'Range', 'Tolerance',
                      'Unnamed_9', 'Unnamed_10', 'In_Use', 'Actual_Calibration_Interval',
                      'Last_Calibration', 'Calibration_Due', 'Remaining_Months', 'Calibration_Type',
                      'Calibration_Report_Number', 'Calibrator', 'PIC', 'Action', 'Unnamed_20']

        # Convert date columns to datetime objects
        df['Last_Calibration'] = pd.to_datetime(df['Last_Calibration'], format='%d-%b-%y', errors='coerce')
        df['Calibration_Due'] = pd.to_datetime(df['Calibration_Due'], format='%d-%b-%y', errors='coerce')

        # Drop rows where 'Last Calibration' or 'Calibration Due' are NaN. These rows are not tool data.
        df = df.dropna(subset=['Last_Calibration', 'Calibration_Due'])

        return df
    except FileNotFoundError:
        st.error("Calibration data file not found.")
        return None

df = load_data()

if df is not None:
    # --- Data Processing ---
    df = clean_data(df)
    df['days_until_calibration'] = (df['Calibration_Due'] - pd.to_datetime('today')).dt.days

    # --- Streamlit App ---
    st.title("Bosch Tool Calibration Dashboard")

    # --- Alerts ---
    st.subheader("Tools Due for Calibration Soon")
    due_tools = generate_alerts(df, 30) # 30 days threshold
    if not due_tools.empty:
        st.warning("The following tools are due for calibration within 30 days:")
        st.dataframe(due_tools)
    else:
        st.info("No tools are due for calibration within 30 days.")

    # --- Visualizations ---
    st.subheader("Calibration Schedule")
    fig, ax = plt.subplots()
    sns.histplot(df['days_until_calibration'].dropna(), ax=ax) #drop nan values, that cause errors with the plot.
    st.pyplot(fig)

    # --- Optimal Calibration Batch ---
    st.subheader("Optimal Calibration Batch")
    optimal_batch = find_optimal_batch(df, 5) # Example: batch size of 5
    if not optimal_batch.empty:
        st.dataframe(optimal_batch)
    else:
        st.info("No tools found for optimal batching.")

    # --- Interactive Filters ---
    st.subheader("Data Filtering")
    min_days = int(df['days_until_calibration'].dropna().min())
    max_days = int(df['days_until_calibration'].dropna().max())
    days_filter = st.slider("Filter by Days Until Calibration", min_days, max_days, (min_days, max_days))
    filtered_df = df[(df['days_until_calibration'] >= days_filter[0]) & (df['days_until_calibration'] <= days_filter[1])]
    st.dataframe(filtered_df)

    # --- Additional Visualizations (Example: Tool Usage) ---
    if 'Usage Hours' in df.columns:
        st.subheader("Tool Usage")
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=df, x='Last Calibration', y='Usage Hours', hue='Description', ax=ax2)
        st.pyplot(fig2)

else:
    st.stop() # Stops the app if the data is not loaded.






# EXTRA
# import streamlit as st

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# st.title("💬 Chatbot")
# st.caption("🚀 A Streamlit chatbot powered by OpenAI")
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     client = OpenAI(api_key=openai_api_key)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)