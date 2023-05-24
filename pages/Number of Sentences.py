import cv2
import pytesseract
import streamlit as st
import re

st.set_page_config(page_title="Number of Sentences", page_icon=":book:")


def numberOfSentences(imagePath, selectedLanguage):
    # Görüntüyü yükle
    image = cv2.imread(imagePath)

    # Görüntüyü gri tonlamaya dönüştür
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Görüntüyü eşikle (binarize et)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Konturları bul
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Konturları metin bölgeleri olarak işaretle
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    try:
        # Algılanan metni yazdır
        text = pytesseract.image_to_string(threshold, lang=selectedLanguage)
    except pytesseract.TesseractError as e:
        raise Exception("Lütfen geçerli bir dil seçtiğinizden emin olun.") from e

    # Nokta ile biten cümleleri bul
    pattern = re.compile(r'[^.!?]*[.!?] ')
    matches = pattern.findall(text)
    dotEndedSentences = [match.strip() for match in matches]

    # Metni dosyaya yazdır
    output_text = ""
    for i, sentence in enumerate(dotEndedSentences, 1):
        output_text += f"{i}. cümle: {sentence}\n"

    return output_text, image


st.title("Resimden Metin Çıkarıcı")

uploadedFile = st.file_uploader("Lütfen bir resim dosyası yükleyin", type=["png", "jpg", "jpeg"])
selectedLanguage = None

if uploadedFile is not None:

    # Resmi yükle
    imagePath = "uploaded_image.png"
    with open(imagePath, "wb") as file:
        file.write(uploadedFile.getbuffer())

    selectedLanguage = st.selectbox("Kullanılan Dil Seçiniz",
                                    ["eng", "tur", "de", "ar", "fr", "it", "es", "ru", "zh-cn", "ja", "ko"])

if selectedLanguage is not None:
    try:
        # Metni çıkar ve göster
        extractedText, imageContours = numberOfSentences(imagePath, selectedLanguage)

        showImage = st.selectbox("Analiz Edilen Resmi Göster/Gizle", options=["Gizle", "Göster"])
        if showImage == "Göster":
            st.image(imageContours, channels="BGR")

        showText = st.selectbox("Metni Göster/Gizle", options=["Gizle", "Göster"])
        if showText == "Göster":
            st.text(extractedText)

        if st.download_button("Metni Dosya Olarak İndir", data=extractedText, file_name="metin.txt"):
            st.success("Dosya başarıyla indirildi.")
            st.balloons()

    except Exception as e:
        st.error(str(e))
