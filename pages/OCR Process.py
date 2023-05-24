import cv2
import pytesseract
import streamlit as st

st.set_page_config(page_title="OCR Process", page_icon=":book:")


def ocrProcess(imagePath, selectedLanguage):
    # Load the image
    image = cv2.imread(imagePath)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarize the image (apply threshold)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Perform OCR on the image
    text = pytesseract.image_to_string(threshold, lang=selectedLanguage)

    return text, contours


st.title("Resimden Metin Çıkarıcı")

uploadedFile = st.file_uploader("Lütfen bir resim dosyası yükleyin", type=["png", "jpg", "jpeg"])

if uploadedFile is not None:
    # Upload the image
    imagePath = "uploaded_image.png"
    with open(imagePath, "wb") as file:
        file.write(uploadedFile.getbuffer())

    # Extract text and contours
    st.header("Metin Dosyası")

    selectedLanguage = st.selectbox("Kaynak Dilini Seçin",
                                    ["eng", "tur", "de", "ar", "fr", "it", "es", "ru", "zh-cn", "ja", "ko"])
    extractedText, contours = ocrProcess(imagePath, selectedLanguage)

    show_image = st.selectbox("Resmi Göster/Gizle", options=["Gizle", "Göster"])
    if show_image == "Göster":
        # Load the image with contours
        imageContour = cv2.drawContours(cv2.imread(imagePath), contours, -1, (0, 255, 0), 2)

        st.image(imageContour, channels="BGR")

    showText = st.selectbox("Metni Göster/Gizle", options=["Gizle", "Göster"])
    if showText == "Göster":
        st.text(extractedText)

    if st.download_button("Metni Dosya Olarak İndir", data=extractedText, file_name="../metin.txt"):
        st.success("Dosya başarıyla indirildi.")
        st.balloons()
