import streamlit as st

def card(title, value):
    st.markdown(f"""
        <div style="padding:20px;border-radius:12px;background:#111827;color:white">
            <h3 align="center">{title}</h3>
            <h5>{value}</h5>
        </div>
    """, unsafe_allow_html=True)