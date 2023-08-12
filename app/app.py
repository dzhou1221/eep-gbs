import streamlit as st
from common.utils.authentication import check_password

if check_password():
  st.set_page_config(
      page_title="Hello",
      page_icon="👋",
  )

  st.write("# Welcome to Streamlit! 👋")

  st.sidebar.success("Select a demo above.")
