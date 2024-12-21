import streamlit as st
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Generation.generation import generation
from process_query import process_query
from get_input_data import get_input_data
from eval import eval

# Initialize session state
if "selected_post_type" not in st.session_state:
    st.session_state.selected_post_type = 1
if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""
if "posts_generated" not in st.session_state:
    st.session_state.posts_generated = False

# Title and input field
st.title("Post Suggestions for Blockchain Content Creators")
st.write("### Enter a keyword to generate a post for your blog, article, or video.")

# Keyword input
query = st.text_input("Enter a keyword:", "")
keywords, _, _ = process_query(query)
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
            st.session_state.selected_post_type = post_id

st.write("### Submit your choice:")

# Generate button
if st.button("Generate Post"):
    if keywords:
        with st.spinner("Generating post..."):
            st.session_state.generated_post = generation(
                st.session_state.selected_post_type, keywords
            )
            st.session_state.posts_generated = True
        paragraphs, relations = get_input_data(keywords)
        input_data = {"paragraphs": paragraphs, "relationships": relations}
        eval_result = eval(st.session_state.generated_post, query, input_data)
    else:
        st.warning("Please enter a keyword before generating a post!")


# Display generated post
if st.session_state.posts_generated:
    selected_description = post_types[st.session_state.selected_post_type]
    st.write(f"### Generated Post: Post Type {st.session_state.selected_post_type}")
    st.write(selected_description)
    st.write(st.session_state.generated_post)
    st.write("### Evaluation:")
    st.write(eval_result)