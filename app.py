import streamlit as st
import pandas as pd

# Load data as strings
data = pd.read_csv("data.csv", dtype=str)
history = pd.read_csv("history.csv")

st.set_page_config(page_title="Smart Call Assistant", layout="centered")



st.title(" Smart Call Identifier")

st.write("Enter a phone number to check if it's spam or a job-related call.")

# Input
number = st.text_input("Incoming Phone Number:")

if number:
    number = number.strip()

    result = data[data["phone"] == number]

    if not result.empty:
        row = result.iloc[0]

        if row["type"] == "job":
            st.success(f" {row['company']} is calling!")
            st.info(" Based on your saved job applications")

        elif row["type"] == "spam":
            st.error(" High probability of spam")
            st.caption("Detected using known spam database")

    else:
        # Simple spam detection rules
        if number.startswith("800") or number.startswith("888") or len(number) > 11:
            st.error(" Likely Spam Caller (pattern detected)")
        else:
            st.warning(" Unknown Number (no spam patterns detected)")






st.subheader(" Add a Company You Applied To")

new_phone = st.text_input("Enter Company Phone Number:")
new_company = st.text_input("Enter Company Name:")

if st.button("Add Company"):
    if new_phone and new_company:
        new_row = pd.DataFrame([[new_phone, new_company, "job"]],
                               columns=["phone", "company", "type"])
        
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv("data.csv", index=False)

        st.success(f" {new_company} added successfully!")
    else:
        st.warning("Please fill both fields.")

st.markdown("---")
st.subheader(" Call History")

st.dataframe(history)

st.markdown("###  Call Statistics")

if not history.empty:
    counts = history["result"].value_counts()

    st.write("Total Calls:", len(history))
    st.write("Spam Calls:", counts.get("spam", 0))
    st.write("Job Calls:", counts.get("job", 0))
    st.write("Unknown Calls:", counts.get("unknown", 0))
