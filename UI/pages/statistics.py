import streamlit as st

st.title("Aggregate Post Generation Statistics")

# Dynamically show statistics in real-time
if "stats" in st.session_state:
    stats = st.session_state.stats
    st.write("### Summary of Statistics")
    st.metric("Total Regenerations (same keyword & post type)", stats["total_regenerations"])
    st.metric("Total Likes", stats["total_likes"])
    st.metric("Total Dislikes", stats["total_dislikes"])
else:
    st.write("No statistics available yet. Generate some posts first!")