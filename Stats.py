import pandas as pd
import streamlit as st
import datetime

st.title("Your Personal Gym Tracker")

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
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Create a clean DataFrame for the new gym entry
        new_entry = pd.DataFrame([{
            "timestamp": timestamp,
            "text": u1,
            "kg": kg
        }])
            
            # Safely append to the CSV without destroying the headers
        new_entry.to_csv("database.csv", mode="a", index=False, header=False)
            
        st.success("erfolgreich gespeichert")









