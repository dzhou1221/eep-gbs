import requests
import streamlit as st
from common.utils.authentication import check_password


def main():
  st.title("New CISID")
  st.divider()
  with st.form("Entrance"):
    st.caption(
        "This form should be completed whenever a new billing record (CISID) is needed, e.g. new customer legal entity or account requiring self billing"
    )
    col11, col12 = st.columns(2)
    with col11:
      overall_status = st.text_input(
          "Overall status", "Incomplete - Please check HSBCNetID"
      )

    with col12:
      new_cisid = st.number_input(
          "# new CISIDs",
          min_value=1,
          max_value=25,
          help="Determines the number of rows (CISIDs to create). Max 25",
      )
    st.form_submit_button("Submit")

  with st.container():
    st.header("Section 1 - Tariff & Invoice Preferences")
    with st.form("Section 1-1"):
      col21, col22 = st.columns(2)
      with col21:
        st.selectbox("Country", ("United Kingdom", "Poland", "Mexico"))
        st.text_input("Proposed Tariff Code")
        st.selectbox("Frequency", ("Monthly", "Quarterly"))
        st.selectbox(
            "Template",
            (
                "1 - Invoice only",
                "2 - Invoice and Account-based View",
                "Invoice and Product-based View",
                "Invoice, Account-based View and Product-Based View",
            ),
        )
        st.selectbox("test", "hello")
      with col22:
        st.selectbox(
            "Delivery Method 1",
            (
                "Paper via Post(B)",
                "PDF via HSBCNet (C)",
                "PDF via HSBCNet(C) & Paper via Post (B)",
            ),
        )
        st.selectbox(
            "Delivery Method 2",
            (
                "Paper via Post(B)",
                "PDF via HSBCNet (C)",
                "PDF via HSBCNet(C) & Paper via Post (B)",
            ),
        )
        st.selectbox(
            "Delivery Method 3",
            (
                "Paper via Post(B)",
                "PDF via HSBCNet (C)",
                "PDF via HSBCNet(C) & Paper via Post (B)",
            ),
        )
        # st.selectbox("Delivery Method 4", ("Paper via Post(B)", "PDF via HSBCNet (C)", "PDF via HSBCNet(C) & Paper via Post (B)"))
        values = requests.get(
            "https://we97oci982.execute-api.eu-west-2.amazonaws.com/route"
        )
        st.selectbox("Delivery Method xxxx", values)
      st.form_submit_button("Confirm")

    with st.form("Section 1-2"):
      col31, col32 = st.columns(2)
      with col31:
        st.text_input("HSBCNetId")
        st.text_input("Email Address")
        st.selectbox("HSBCNet TWIST Enabled?", ("Yes", "No"))
        st.selectbox("HSBCNet CAD Enabled?", ("Yes", "No"))
      with col32:
        st.text_input("Additional Email Address 1")
        st.text_input("Additional Email Address 2")
        st.text_input("Additional Email Address 3")
        st.text_input("Additional Email Address 4")
      st.form_submit_button("Submit")

  with st.container():
    st.header("Section 2 - CISID")


if __name__ == "__main__":
  if check_password():
    main()
