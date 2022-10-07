import html
import sys
from json2txttree import json2txttree
import requests
import streamlit as st
import time
import streamlit.components.v1 as components


if 'executed' not in st.session_state: st.session_state['executed'] = False

st.set_page_config(
    page_title='APIs',
    layout='wide'
)


def reset_params():
    st.session_state['executed'] = False
    st.experimental_rerun()


endpoint = st.text_input("Enter your endpoint:", value="http://openlibrary.org/search.json?q=some query")

col1, col2, _, _, _, _ = st.columns(6)
with col1:
    if st.button("Get Response!") or st.session_state['executed']:
        st.session_state['executed'] = True
if st.session_state['executed']:
    with col2:
        if st.button("Reset Results!"):
            reset_params()

if st.session_state['executed']:
    if not endpoint:
        st.error("You need to give an endpoint!")
    else:
        start = time.time()
        get_response = requests.get(endpoint)
        end = time.time()

        status_code = get_response.status_code
        st.write(f"Status Code: {status_code}")
        st.write(f"Total time : %.2f second" % (end - start))
        st.write(f"Size of the object returned: {sys.getsizeof(get_response.content)} bytes")
        if status_code == 200:
            content_type = get_response.headers['Content-Type'].split(';')[0]

            st.write(f"Content Type : {get_response.headers['Content-Type']}")

            if 'json' in content_type:
                json_data = get_response.json()
                try:
                    count = json_data['numFound']
                    if count == 0:
                        st.error("This JSON is NULL")
                        st.write(json_data)
                except Exception as e:
                    pass

                try:
                    structure = json2txttree(json_data)
                    st.write("#### Structure of JSON Data:")
                    st.text(structure)
                    if st.button("Show JSON Data (Not recommended if you're running out of memory!)") and st.session_state['executed']:
                        st.write(json_data)
                except Exception as e:
                    st.error("Can not parse to a tree")
                    st.write("Retrieved Data : ")
                    st.write(json_data)
            else:
                st.write("#### Preview for HTML page -->")
                components.html(html.unescape(get_response.text), width=1200, height=1200)

