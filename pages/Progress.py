import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Charts")

if "logged_in_user" in st.session_state:
    user_n = st.session_state["logged_in_user"]
    st.write(f"showing Progress for: **{user_n}**")
    if user_n == "emanuele" or user_n == "emin" or user_n == "altin" or user_n == "armin":
        st.write(f"***Oha {user_n} du bist in der letzten zeit ja viel stärker geworden. Weiter so :) - Dein Enes***")
else:
    st.warning("Please go to the main page and type in your user name")


connect = st.connection("gsheets", type=GSheetsConnection)
rawdata = connect.read(ttl=0)


if rawdata is not None and not rawdata.empty:

    rawdata["timestamp"] = pd.to_datetime(rawdata["timestamp"])
    rawdata = rawdata.sort_values("timestamp", ascending = True)
    rawdata["text"] = rawdata["text"].str.strip()
    rawdata["kg"] = pd.to_numeric(rawdata["kg"])
    user_data = rawdata[rawdata["name"] == user_n]
    if not user_data.empty:

        options = user_data["text"].unique().tolist()
        list = ["All exercises"] + options
        select = st.selectbox("Wich excercise do you want to review?", list)

        if select == "All exercises":
            chartdata = user_data.pivot_table(index="timestamp", columns="text", values="kg", aggfunc="max")
            chartdata = chartdata.ffill()
            st.line_chart(data=chartdata)
        else:
            fdata = user_data[user_data["text"] == select]
            #st.dataframe(fdata)
            chartdata = fdata.set_index("timestamp")["kg"]
            st.line_chart(data=chartdata)

else:
    st.write("Go to the Gym to view progress")