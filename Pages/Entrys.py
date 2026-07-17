import streamlit as st
import pandas as pd

st.title("Newest Entrys")
ndata = pd.read_csv("database.csv")
ndata["timestamp"] = pd.to_datetime(ndata["timestamp"])
ndata = ndata.drop_duplicates(subset="text", keep="last")
ndata = ndata.sort_values("kg", ascending=False).reset_index(drop=True)
edittable_t = st.data_editor(ndata, num_rows="dynamic", use_container_width=True, hide_index=True)
