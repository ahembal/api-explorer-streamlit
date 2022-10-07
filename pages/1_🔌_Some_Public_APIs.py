from pathlib import Path
from streamlit import cache
import pandas as pd
import streamlit as st

# we set page configs only once
st.set_page_config(
    page_title='APIs',
    layout='wide'
)


# Cache this function to get data faster
@cache
def read_md_file(md_file):
    return Path(md_file).read_text()


# To be able to browse freely, print list of links
if st.checkbox("Show APIs Links"):
    md_file = read_md_file("data/links.txt")
    st.markdown(md_file, unsafe_allow_html=True)

# Get table of APIs
books_df = pd.read_csv(Path('data/books.csv'))
books_df['line'] = books_df['API'] + ' | ' + books_df['Description']
set_of_auth = list(set(list(books_df['Auth'])))
set_of_https = list(set(list(books_df['HTTPS'])))
set_of_cors = list(set(list(books_df['CORS'])))
filtered_df = books_df

st.write("## Books Public APIs Comparison")
col1, col2, col3, _, _, _ = st.columns(6)
with col1:
    choices_auth = st.multiselect("Filter Auth:", options=set_of_auth)
    if not choices_auth:
        indexes_auth = []
    else:
        indexes_auth = filtered_df['Auth'].isin(choices_auth)
with col2:
    choices_https = st.multiselect("Filter HTTPS:", options=set_of_https)
    if not choices_https:
        indexes_https = []
    else:
        indexes_https = filtered_df['HTTPS'].isin(choices_https)
with col3:
    choices_cors = st.multiselect("Filter CORS:", options=set_of_cors)
    if not choices_cors:
        indexes_cors = []
    else:
        indexes_cors = filtered_df['CORS'].isin(choices_cors)

if st.button("Apply Filters"):
    indexes = []
    try:
        list_of_indexes = [indexes_cors, indexes_auth, indexes_https]
        full_indexes = [i for i in list_of_indexes if len(i) == 23]
        indexes = full_indexes[0]
        for i in full_indexes:
            indexes = i & indexes
        indexes = list(indexes)
    except Exception as e:
        pass
    if indexes:
        filtered_df = filtered_df[indexes]
    else:
        filtered_df = books_df
        st.error("Please choose at least one filter!")

st.dataframe(filtered_df[['API','Description', 'Auth', 'HTTPS', 'CORS']])

# st.write("### Here you can explore some of public APIs")
# selected_api = st.selectbox("Select API to try:", options=books_df['line'])
#
# splitted = [i.strip() for i in selected_api.split('|')]
# api, desc = splitted[0], splitted[1]
# st.write(api)
# st.write(desc)
# selected_row = books_df[books_df['API'].isin([api]) & books_df['Description'].isin([desc])].drop(['line', 'API', 'Description'], axis=1)
# st.dataframe(selected_row)

# list_of_available_endpoints = get_endpoints(api, desc)
