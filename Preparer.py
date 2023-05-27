import streamlit as st
import time

st.set_page_config(page_title="Preparer", page_icon=":book:")

nameAndSurname = st.empty()
subject1 = st.empty()
subject2 = st.empty()
subject3 = st.empty()
subject4 = st.empty()

nameAndSurname.markdown(
    "<h1 style='font-size: 40px; color: #333; margin-bottom: 30px; text-align: center;'>Muhammed Demirel</h1>",
    unsafe_allow_html=True)
time.sleep(1)
subject1.markdown(
    "<h1 style='font-size: 30px; color: #333; margin-bottom: 20px; text-align: center;'>Görüntü İşleme </h1>",
    unsafe_allow_html=True)
time.sleep(1)
subject2.markdown(
    "<h1 style='font-size: 25px; color: #555; margin-bottom: 20px; text-align: center;'>OpenCV ile Optik Karakter Tanıma (OCR)</h1>",
    unsafe_allow_html=True)
time.sleep(1)
subject3.markdown("<h1 style='font-size: 25px; color: #333; margin-bottom: 30px; text-align: center;'>ve</h1>",
                  unsafe_allow_html=True)
time.sleep(1)
subject4.markdown(
    "<h1 style='font-size: 30px; color: #555; margin-bottom: 20px; text-align: center;'>Dil Analizi Uygulaması</h1>",
    unsafe_allow_html=True)
