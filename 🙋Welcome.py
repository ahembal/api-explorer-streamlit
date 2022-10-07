import streamlit as st

st.set_page_config(
    page_title='Tester Client',
    layout='wide'
)


st.title("Welcome to API Explorer")

st.markdown("This page is designed to have a quick understanding of APIs. You can explore some "
            "[OPEN APIs](https://github.com/public-apis/public-apis) or you can test your custom endpoint.")
st.markdown("Choose what ever you want from the sidebar.")