import streamlit as st
import pandas as pd
from io import StringIO

st.header('PG&E Usage Formatter')
st.subheader('First, we will upload your file')

uploaded_file = st.file_uploader('Please select the usage csv from your local files')
if uploaded_file is not None:

  stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

  df = pd.read_csv(stringio, header=4, parse_dates= {"Date" : ["DATE","START TIME"]}, index_col=['Date'])
  df.drop(['END TIME'], axis='columns', inplace=True)
  df.COST = df.COST.str.replace('$', '', regex=False).astype('float16')

  st.subheader('Now we can view the contents')
  st.write('We are simply making sure that everything looks properly formatted before we aggregate the data')
  st.dataframe(df)

  st.subheader('Finally, we sum the usage and cost')
  st.write("We now aggregate the usage and costs fields using a simple sum. Keep in mind that the first of the month is shown even though this is the entire month's usage")
  usage = df.resample('MS').sum(numeric_only=True)
  usage.index = usage.index.date
  st.dataframe(usage.style.format(precision=2))

  st.download_button(
    label="Download data as CSV",
    data=usage.to_csv(index=True, float_format="%.2f", index_label='Date'),
    file_name='output.csv',
    mime='text/csv',
)