import cv2
import pytesseract
from nltk.corpus import wordnet
import streamlit as st

st.set_page_config(page_title="Word Analysis", page_icon=":book:")


def wordAnalysis(imagePath, selectedLanguage):
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

    # Algılanan metni yazdır
    text = pytesseract.image_to_string(threshold, lang=selectedLanguage)

    # Metni dosyaya yazdır
    with open("metin.txt", "w", encoding="utf-8") as file:
        file.write(text)

    # Metni kelimelere ayır ve anlamlarını yazdır
    words = text.split()
    result = []
    for index, word in enumerate(words, 1):
        synsets = wordnet.synsets(word, lang='eng')
        if synsets:
            synset = synsets[0]
            definition = synset.definition()
            result.append(f"{index}. {word}: {definition}")

    return text, result, image, contours


# Streamlit uygulaması
st.title("Metin Analizi ve Anlam Tespiti")
uploadedFile = st.file_uploader("Lütfen bir görüntü dosyası yükleyin.", type=["png", "jpg", "jpeg"])
selectedLanguage = st.selectbox("Dil Seçin", ["eng"])  # Kullanıcının dil seçebilmesi

if uploadedFile is not None:
    # Dosya yüklendiğinde analizi gerçekleştir
    imagePath = "uploaded_image.png"
    with open(imagePath, "wb") as file:
        file.write(uploadedFile.getvalue())

    text, result, image, contours = wordAnalysis(imagePath, selectedLanguage)

    showImage = st.selectbox("Resmi Göster/Gizle", options=["Gizle", "Göster"])
    if showImage == "Göster":
        # Load the image with contours
        imageContour = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)
        st.image(imageContour, channels="BGR")

    showText = st.selectbox("Metni Göster/Gizle", options=["Gizle", "Göster"])
    if showText == "Göster":
        st.text(result)

    if st.download_button("Anlamlar Dosyasını İndir", data="\n".join(result), file_name="anlamlar.txt"):
        st.success("Dosya başarıyla indirildi.")
        st.balloons()
