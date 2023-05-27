import cv2
import pytesseract
from langdetect import detect
from googletrans import Translator
import streamlit as st
import base64

st.set_page_config(page_title="OCR Translate", page_icon=":book:")


def ocrTranslateProcess(imagePath, selectedLanguage, targetLang):
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imageContour = cv2.drawContours(image.copy(), contours, -1, (0, 0, 255), 2)
    text = pytesseract.image_to_string(threshold, lang=selectedLanguage)

    if text:
        sourceLang = detect(text)
        translator = Translator()

        try:
            translation = translator.translate(text, src=sourceLang, dest=targetLang)
            translationText = translation.text
            st.success("Metin başarıyla çevrildi.")
        except ValueError:
            translationText = ""
            st.error("Dil çevirisi başarısız oldu.")
    else:
        translationText = ""
        st.warning("Resimde metin bulunamadı.")
    return translationText, imageContour


def get_download_link(fileContent, fileName):
    encodedFile = base64.b64encode(fileContent).decode()
    href = f'<a href="data:file/txt;base64,{encodedFile}" download="{fileName}">Metni Dosya Olarak İndir</a>'
    return href


st.title("Dil Çevirici")
uploadedFile = st.file_uploader("Lütfen bir resim dosyası yükleyin", type=["png", "jpg", "jpeg"])

if uploadedFile is not None:
    imagePath = "uploaded_image.png"
    with open(imagePath, "wb") as file:
        file.write(uploadedFile.getbuffer())
    selectedLanguage = st.selectbox("Kaynak Dilini Seçin",
                                    ["eng", "tur", "de", "ar", "fr", "it", "es", "ru", "zh-cn", "ja", "ko"])
    targetLang = st.selectbox("Hedef Dilini Seçin",
                              ["eng", "tur", "de", "ar", "fr", "it", "es", "ru", "zh-cn", "ja", "ko"])

    try:
        showImage = st.empty()
        showText = st.empty()
        extractedText, imageContour = ocrTranslateProcess(imagePath, selectedLanguage, targetLang)
        if extractedText:
            showImage = st.selectbox("Analiz Edilen Resmi Göster/Gizle", options=["Gizle", "Göster"])
            if showImage == "Göster":
                st.image(imageContour, channels="BGR")
            showText = st.selectbox("Metni Göster/Gizle", options=["Gizle", "Göster"])
            if showText == "Göster":
                st.text(extractedText)
            if st.download_button("Metni Dosya Olarak İndir", data=extractedText, file_name="../metin.txt"):
                st.success("Dosya başarıyla indirildi.")
                st.balloons()
    except pytesseract.TesseractError:
        st.error("Hatalı dil seçimi yapıldı. Lütfen uygun bir dil seçimi yapın.")
    except:
        st.error("Çeviri işlemi sırasında bir hata oluştu. Lütfen tekrar deneyin.")
