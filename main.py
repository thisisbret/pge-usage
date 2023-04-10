import streamlit as st
import pandas as pd
from io import StringIO

with st.sidebar:
  st.image('./assets/Logo-Final-2.png')
  st.write("Welcome to our PG&E usage and cost tool. Simply upload your client's usage csv "
           "this will resample the data into monthly figures.")
  header_index = st.number_input('Header Index', 0, 10, 4, 1)

st.subheader("First, let's upload your file")

uploaded_file = st.file_uploader('Please select the usage csv from your local files')
if uploaded_file is not None:

  stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

  df = pd.read_csv(
    stringio,
    header=header_index, 
    parse_dates= {"Date" : ["DATE","START TIME"]},
    index_col=['Date']
  )

  df.drop(['END TIME'], axis='columns', inplace=True)
  df.USAGE = df.USAGE.astype('float16')
  df.COST = df.COST.str.replace('$', '', regex=False).astype('float16')

  st.write("Now that the file is loaded, you can view it to make sure everything ",
           "appears normal. The header index in the sidebar allows you to ",
           "adjust where the header row appears in the raw data file if there's an error.")
  
  with st.expander('Expand to view the raw data.', False):
    st.dataframe(df)

  st.write("We now aggregate the usage and costs fields using a simple sum. "
           "Keep in mind that the first of the month is shown even though this "
           "is the entire month's usage.")
  
  usage = df.resample('MS').sum(numeric_only=True)
  usage.index = usage.index.date
  with st.expander('Expand to view the aggregated usage data.', False):
    st.dataframe(usage.style.format(precision=2))

  st.write("Lastly, you can save the data locally.")

  st.download_button(
    label="Download data as CSV",
    data=usage.to_csv(index=True, float_format="%.2f", index_label='Date'),
    file_name='output.csv',
    mime='text/csv',
  )