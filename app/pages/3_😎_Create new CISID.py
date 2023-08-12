import time

import pandas as pd
import streamlit as st
import folium
from geopy.geocoders import Nominatim
from common.utils.authentication import check_password

def add_account():
  if 'my_lst' not in st.session_state:
      st.session_state['my_lst'] = []
  with st.expander("Add Account"):
      with st.form("GBS account"):
        account_id = st.text_input("Account ID")
        add_button = st.form_submit_button("Add")
        if add_button:
            if len(account_id) > 0:
                st.session_state['my_lst'] += [account_id]
                st.write( st.session_state['my_lst'] )
            else:
                st.warning("Enter text")
def main():
  st.title("Create a new CISID")
  st.divider()
  with st.container():
    with st.form("form 1"):
      col11, col12 = st.columns(2)
      with col11:
        # "Enter the Customer to be invoiced"
        lead_customer = st.text_input(
            label="Lead Customer", 
            max_chars=None,
            type="default",
            help="Enter the Customer to be invoiced"
        )
      # if not lead_customer:
      #   st.error("Lead Customer is required!")
      #   raise Exception("Lead Customer is required!")
      with col12:
        lead_cin = st.number_input(
            "Lead CIN",
            min_value=1,
            max_value=25,
            help="CIN, if more than one CIN is included only include the primary CIN",
        )
      
      col2, _ = st.columns([2,2])
      rm_name = col2.text_input(
          label="RM Name", 
          max_chars=None,
          type="default",
      )
      col31, col32 = st.columns(2)
      with col31:
        # "Enter the Customer to be invoiced"
        debit_account_number = st.text_input(
            "Debit Account Number",
            max_chars=None,
            type="default",
        )

      with col32:
        debit_account_currency = st.selectbox(
          label = "Debit Account Currency",
          options = ["GBP","USD","CAD","CNY","JPY"],
          index = 0
        )
      st.subheader("Delivery Details")
      hsbcnet_id=st.text_input(
        label="HSBCnet ID",
        help="Input the HSBCnet ID to deliver statements to. Must be full HSBCnet ID starating with country code (e.g. GB,US,CA FR)"
      )
      
      customer_email = st.text_input(
        label="Customer Email Address",
        help="Populate only if email delivery is required"
      )
      invoice_template = st.selectbox(
        label = "Invoice Template",
        options = ["Invoice and Product View Statement(1)", "Invoice and Product View Statement(2)"],
        index = 0
      )
      st.form_submit_button("Save")
    
    with st.form("Address Details"):
      st.caption("Mandatory, please fill in all cases")
      uk_address_flag = st.checkbox("UK Address?")
      post_code = st.text_input("Post Code")
      find_address = st.form_submit_button("Find My Address")
      if find_address:
        geolocator = Nominatim(timeout=10, user_agent="PDS")
        location = geolocator.geocode(post_code)
        derived_city, derived_county, derived_country, _, _ = [x.strip() for x in location.address.split(",")]
        street = st.text_input("Street")
        city = st.text_input("City", value=derived_city)
        county = st.text_input("County", value=derived_county)
        country = st.text_input("Country", value=derived_country)
        st.map(pd.DataFrame(data={'lat':[location.latitude], 'lon':[location.longitude]}))
        
    tariff_group = st.selectbox(
          label = "Tariff Group",
          options = ["BBSTD", "OTHERS"],
          index = 0
        )
    if tariff_group == "OTHERS":
      tariff_group = st.text_input(label="input an existing group tariff")
    customer_tax_region = st.selectbox(
          label = "Customer Tax Region",
          options = ["UK", "France"],
          index = 0
        )

    segment = st.selectbox(
          label = "Segement",
          options = ["UCORP", "UBBRM-BBRM","UBBSM-BBSM", "UNPO-Charities"],
          index = 0
        )

    # account_id = []
    # with st.form("GBS account 1"):
    #   account_id = st.text_input("Account ID")
    #   st.caption("GBS Account ID to be Added")
    #   st.warning("please only input 1 Account ID perrow")
    #   add_button = st.form_submit_button("Add Account ID")
    
    # if add_button:
    #   account_id.extend(account_id)
    #   if account_id:
    #     st.text(account_id)
    add_account()
if __name__ == "__main__":
  # if check_password():
  main()
