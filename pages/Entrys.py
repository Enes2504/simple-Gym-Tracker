import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
st.title("Newest Entrys")


if "logged_in_user" in st.session_state:
    user_n = st.session_state["logged_in_user"]
    st.write(f"Showing Progress for: **{user_n}**")
    if user_n == "emanuele" or user_n == "emin" or user_n == "altin" or user_n == "armin":
        st.write(f"***Ey {user_n} du bist ein Löwe mach weiter und gib nicht auf :) - Dein Enes***")
else:
    st.warning("Please go to the main page and type in your user name")
    st.stop() # Stops the script right here so it doesn't crash below!

# 2. Connect and read the live cloud data (added parentheses!)
connect = st.connection("gsheets", type=GSheetsConnection)
rawdata = connect.read(ttl=0)


# 3. Check if the cloud database actually has data
if rawdata is not None and not rawdata.empty:
    user_data = rawdata[rawdata["name"] == user_n]
else:
    user_data = pd.DataFrame(columns=["name", "timestamp", "text", "kg"])

if not user_data.empty:

    ordered_data = user_data.sort_values("timestamp", ascending=True)
    newest_per_exercise = ordered_data.drop_duplicates(subset="text", keep="last")
    final_display = newest_per_exercise.sort_values("kg", ascending=False)
    
    edited_df = st.data_editor(
        final_display[["timestamp", "text", "kg"]], 
        num_rows="dynamic", 
        disabled=["timestamp", "text", "kg"], 
        use_container_width=True,
        hide_index=True
    )
    if len(edited_df) < len(final_display):
        # Find the exact cloud row index that was just deleted from the screen
        deleted_indices = final_display.index.difference(edited_df.index)
        
        # Drop it from the master cloud sheet
        rawdata = rawdata.drop(deleted_indices)
        
        # Convert timestamps back to clean strings so the Google Sheet stays tidy
        rawdata["timestamp"] = pd.to_datetime(rawdata["timestamp"]).dt.strftime("%Y-%m-%d")
        
        # Upload the clean dataset back to the cloud
        connect.update(data=rawdata)
        
        # Instantly reload the page so the chart updates automatically
        st.rerun()
else:
    st.warning("You haven't saved any workouts yet!")