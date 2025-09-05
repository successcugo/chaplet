import streamlit as st

# Mapping WAEC grades to scores
grade_mapping = {
    "A1": 95,
    "B2": 85,
    "B3": 75,
    "C4": 65,
    "C5": 55,
    "C6": 45,
    "D7": 0,
    "AR": None,  # Awaiting Result
}

st.title("FUTO Post-UTME Aggregate Calculator")

# Input for JAMB score
jamb_score = st.number_input("Enter your JAMB score:", min_value=0, max_value=400, step=1)

# O'level subject grades
st.subheader("Select your O'level grades for 4 relevant subjects")
st.write("Note: This is English language and the four other subjects from your JAMB combination but their grades in your O'level result.")

olevel_grades = []
ar_selected = False

for i in range(1, 5):
    grade = st.selectbox(
        f"O'level Subject Grade {i}",
        options=list(grade_mapping.keys()),
        key=f"grade_{i}"
    )
    if grade == "AR":
        ar_selected = True
    else:
        olevel_grades.append(grade_mapping[grade])

# Submit button
if st.button("Calculate Aggregate"):
    if jamb_score == 0:
        st.warning("⚠️ Please enter your JAMB score.")
    elif ar_selected:
        st.warning("⚠️ You selected 'Awaiting Result (AR)'. Please wait for your O'level results before calculating your aggregate.")
    else:
        jamb_component = jamb_score * 0.15
        olevel_component = sum(olevel_grades) * 0.1
        aggregate = jamb_component + olevel_component
        
        st.success(f"✅ Your FUTO aggregate score is: **{aggregate:.2f}**")
