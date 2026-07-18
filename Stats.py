import pandas as pd
import streamlit as st
import datetime
from streamlit_gsheets import GSheetsConnection
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

st.title("Your Personal Gym Tracker")

user_n = st.text_input("Enter your name:", "").strip().lower()

if user_n:
    st.session_state["logged_in_user"] = user_n
    connect = st.connection("gsheets", type=GSheetsConnection)
    rawdata = connect.read(ttl=0)
    if user_n == "emanuele" or user_n == "emin" or user_n == "altin" or user_n == "armin":
        st.write(f"***Stark {user_n} Welche Maschine Hast du jz wieder auseinander genommen? :) - Dein Enes***")

    if rawdata is None or rawdata.empty:
        rawdata = pd.DataFrame(columns=["name", "timestamp", "text", "kg"])
    

    u1 = st.selectbox("Exersices",
                  ("Preacher curls", "Shrugs", "Chest Press", "Shoulder Press", "Lat Pulldown", 
                  "Triceps Pushdown", "Wrist Curls", "Row", "Leg Press", "Leg Extension", "Butterflys",
                  )
                  )
    if u1 != "":
        kg = st.number_input(f"How much Kg at {u1}?", step = 2.5)

    save = st.button("Save")
    if save:
        if kg <= 0:
          st.error("Invalid Value")
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Create a clean DataFrame for the new gym entry
            new_entry = pd.DataFrame([{
                "name": user_n,
                "timestamp": timestamp,
                "text": u1,
                "kg": kg
            }])
            
            # Safely append to the CSV without destroying the headers
            st.success("erfolgreich gespeichert")
            updated_df = pd.concat([rawdata, new_entry], ignore_index=True)
            connect.update(data=updated_df)
            st.rerun()
else:
    st.error("Please enter you name!")
    










