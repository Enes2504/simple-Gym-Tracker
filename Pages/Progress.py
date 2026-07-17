import streamlit as st
import pandas as pd

st.title("Charts")

st.write("Charts about your Progress")
ndata = pd.read_csv("database.csv")
ndata["timestamp"] = pd.to_datetime(ndata["timestamp"])
ndata = ndata.sort_values("timestamp", ascending = True)

ndata["text"] = ndata["text"].str.strip()
ndata["kg"] = pd.to_numeric(ndata["kg"])

if not ndata.empty:

    options = ndata["text"].unique().tolist()
    list = ["All exercises"] + options
    select = st.selectbox("Wich excercise do you want to review?", list)

    if select == "All exercises":
        chartdata = ndata.pivot_table(index="timestamp", columns="text", values="kg", aggfunc="max")
        chartdata = chartdata.ffill()
        st.line_chart(chartdata)
    else:
        fdata = ndata[ndata["text"] == select]
        #st.dataframe(fdata)
        chartdata = fdata.set_index("timestamp")["kg"]
        st.line_chart(chartdata)

else:
    st.write("Go to the Gym to view progress")