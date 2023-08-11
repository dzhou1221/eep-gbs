import streamlit as st
import time
from common.utils.authentication import check_password

def main():
  with st.spinner('Wait for it...'):
    time.sleep(2)
  st.success("welcome page two")
  st.balloons()
      
if __name__ == '__main__':
  if check_password():
    main()