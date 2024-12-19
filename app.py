import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from process_query import process_query
from generation import gen_1, gen_2, gen_3, gen_4, gen_5

# Parallel generation function
def generate_all(keywords):
    results = {}
    with ThreadPoolExecutor() as executor:
        futures = {
            "News Articles": executor.submit(gen_1, keywords),
            "Analytical Insights": executor.submit(gen_2, keywords),
            "Educational Content": executor.submit(gen_3, keywords),
            "Product/Service Promotion": executor.submit(gen_4, keywords),
            "Interactive Content": executor.submit(gen_5, keywords),
        }
        for key, future in futures.items():
            results[key] = future.result()
    return results

# Streamlit Interface
st.title("Post Suggestions for Blockchain Content Creators")
st.write("### Enter a query to generate posts for your blog, article, or video.")

# State to manage generated results
if "posts_generated" not in st.session_state:
    st.session_state.posts_generated = False
if "results" not in st.session_state:
    st.session_state.results = {}
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# Form for query input
with st.form(key="query_form"):
    query = st.text_input("Enter a query:", "")
    submit_button = st.form_submit_button("Generate Posts")

# Categories with descriptions
categories = {
    "News Articles": "News articles announcing fluctuations, shocking news, or positive news related to blockchain.",
    "Analytical Insights": "Analytical articles, forecasts, and insights about the blockchain situation.",
    "Educational Content": "Blockchain knowledge-sharing articles and tutorials.",
    "Product/Service Promotion": "Product and service introduction articles.",
    "Interactive Content": "Interactive articles, Q&A, Challenges, Giveaways, Polls, Surveys."
}


cols = st.columns(5)
buttons = list(categories.keys())  # Keys for selection
descriptions = list(categories.values())  # Values for display

# Display buttons but disable them if posts are not generated
for i, col in enumerate(cols):
    disabled_state = not st.session_state.posts_generated  # Disable if posts not generated
    if col.button(descriptions[i], disabled=disabled_state):
        st.session_state.selected_category = buttons[i]

# Post generation logic
if submit_button:
    if query:
        st.write("### Generating posts... Please wait.")
        # Process query and generate posts
        entities, phase, cate = process_query(query)
        with st.spinner("Generating posts..."):
            st.session_state.results = generate_all(entities)
            st.session_state.posts_generated = True
    else:
        st.warning("Please enter a query before submitting!")

# Display the selected post after generation
if st.session_state.posts_generated:
    if st.session_state.selected_category:
        st.write(f"### {st.session_state.selected_category}")
        st.write(st.session_state.results[st.session_state.selected_category])
    else:
        st.info("Please select a category to display its generated post.")
else:
    st.info("Submit a query to generate posts.")
