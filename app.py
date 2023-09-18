import streamlit as st
import pandas as pd
import os


file = None

with st.sidebar:
    st.image('https://plus.unsplash.com/premium_photo-1661878265739-da90bc1af051?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2586&q=80')
    radio = st.radio('', [
        'Upload', 'Explore', 'Download'
    ])

if os.path.exists('source.csv'):
    data = pd.read_csv('source.csv', index_col=None)
if radio=='Upload':
    st.title('Upload your dataset for exploring...')
    file = st.file_uploader('upload CSV file here')
    if file:
        data = pd.read_csv(file, index_col=None)
        data.to_csv('source.csv', index=None)
        st.dataframe(data)

###################### Explore Option ######################
if radio=='Explore':
    if data is not None:
        explore_radio = st.radio('These are the options you can use to explore your dataset...', [
            'Show categorical Columns',
            'Show Numerical Columns',
            'Missing Values',
            'Remove Missing Values',
            'Remove unwanted columns'
        ])
        if explore_radio=='Show categorical Columns':
            cat_col = [i for i in data.columns if data[i].dtype=='object']
            st.write(cat_col)
        if explore_radio=='Show Numerical Columns':
            num_col = [i for i in data.columns if data[i].dtype=='float64' or data[i].dtype=='int']
            st.write(num_col)
        if explore_radio=='Missing Values':
            st.write(data.isnull().sum().reset_index().rename(columns={'index': 'Features', 0: 'MissingCount'}))
        if explore_radio=='Remove Missing Values':
            if st.button('Sure want to delete missing values?'):
                data = data.dropna(axis=0)
                data.to_csv('source.csv', index=None)
        if explore_radio=='Remove unwanted columns':
            col_del = st.multiselect('Choose columns to be deleted from the data',
                                     list(data.columns))
            st.write(col_del)
            if st.button(f'remove {col_del} ?'):
                data=data.drop(col_del, axis=1)
                data.to_csv('source.csv', index=None)
        st.dataframe(data)
    else:
        st.write('please go to Upload and upload your csv and come back :)')
###################### End Explore  ######################

st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

if radio=='Download':
    csv = convert_df(data)
    st.download_button("Press to Download",
                    csv,
                    "file.csv",
                    "text/csv",
                    key='download-csv')
        