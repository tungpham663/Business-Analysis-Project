import streamlit as st
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Generation.generation import generation
from process_query import process_query

# Initialize session state
if "user_selected_post_type" not in st.session_state:
    st.session_state.user_selected_post_type = 1
if "user_generated_post" not in st.session_state:
    st.session_state.user_generated_post = ""
if "user_posts_generated" not in st.session_state:
    st.session_state.user_posts_generated = False
if "stats" not in st.session_state:
    st.session_state.stats = {"total_regenerations": 0, "total_likes": 0, "total_dislikes": 0}
if "last_keyword" not in st.session_state:
    st.session_state.last_keyword = None
if "last_post_type" not in st.session_state:
    st.session_state.last_post_type = None

def update_stats(stat_type):
    if stat_type in st.session_state.stats:
        st.session_state.stats[stat_type] += 1

# Title and input field
st.title("Post Suggestions for Blockchain Content Creators")
st.write("### Enter a keyword to generate a post for your blog, article, or video.")

# Keyword input
input = st.text_input("Enter a keyword:", "")
keyword, _, _ = process_query(input)
# Post type descriptions
post_types = {
    1: "News articles announcing fluctuations, shocking news, or positive news related to blockchain (exchange/crypto, token, DeFi, NFT).",
    2: "Analytical articles, forecasts, and insights about the current blockchain situation.",
    3: "Educational and knowledge-sharing articles, including tutorials and guides related to blockchain.",
    4: "Product and service introduction articles, showcasing new blockchain-related offerings.",
    5: "Interactive articles such as Q&A sessions, challenges, giveaways, polls, and surveys to engage the audience."
}

# Display a single box with descriptions of all post types
st.write("### Post Type Descriptions:")
st.markdown(f"""
    <div style="
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: transparent;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
        <b>1. News Articles:</b> {post_types[1]}<br><br>
        <b>2. Analytical Insights:</b> {post_types[2]}<br><br>
        <b>3. Educational Content:</b> {post_types[3]}<br><br>
        <b>4. Product/Service Promotion:</b> {post_types[4]}<br><br>
        <b>5. Interactive Content:</b> {post_types[5]}
    </div>
""", unsafe_allow_html=True)

# Display buttons in a single row using columns
st.write("### Select a Post Type:")
cols = st.columns(5)

for i, (post_id, description) in enumerate(post_types.items()):
    with cols[i]:
        if st.button(f"Post Type {post_id}", key=f"post_type_{post_id}"):
            st.session_state.user_selected_post_type = post_id

st.write("### Submit your choice:")

# Generate button
if st.button("Generate Post"):
    if keyword:
        with st.spinner("Generating post..."):
            # Check if keyword and post type are the same as before
            if (st.session_state.last_keyword == input
                and st.session_state.last_post_type == st.session_state.user_selected_post_type
            ):
                # Increment total regenerations if it's the same
                update_stats("total_regenerations")
            else:
                # Update last keyword and post type
                st.session_state.last_keyword = input
                st.session_state.last_post_type = st.session_state.user_selected_post_type

            st.session_state.user_generated_post = generation(
                st.session_state.user_selected_post_type, keyword
            )
            st.session_state.user_posts_generated = True
    else:
        st.warning("Please enter a keyword before generating a post!")

# Display generated post
if st.session_state.user_posts_generated:
    selected_description = post_types[st.session_state.user_selected_post_type]
    st.write(f"### Generated Post: Post Type {st.session_state.user_selected_post_type}")
    st.write(selected_description)
    st.write(st.session_state.user_generated_post)

     # Like/Dislike Buttons
    st.write("### Do you like this post?")
    if "user_feedback" not in st.session_state:
        st.session_state.user_feedback = None
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Like", key="like_button"):
            st.session_state.user_feedback= "liked"
            update_stats("total_likes")
            st.success("You liked the post!")

    with col2:
        if st.button("👎 Dislike", key="dislike_button"):
            st.session_state.user_feedback= "disliked"
            update_stats("total_dislikes")
            st.error("You disliked the post!")

    if st.session_state.user_feedback:
        st.write(f"Feedback recorded: {st.session_state.user_feedback}")