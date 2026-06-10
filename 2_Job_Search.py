import streamlit as st
st.set_page_config(page_title="Job Search", page_icon="")
st.title(" Job Search")
q = st.text_input("Search jobs for:", "Python developer")
loc = st.text_input("Location:", "Remote")
if st.button("Search"): st.success(f"Searching jobs for {q} in {loc} (demo)")
