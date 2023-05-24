import cv2
import pytesseract

# Görüntüyü yükle
image = cv2.imread("sw.jpg")

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
text = pytesseract.image_to_string(threshold, lang='tur')

# Metni dosyaya yazdır
with open("resimCevir.txt", "w", encoding="utf-8") as file:
    file.write(text)

# Metin bölgelerini göster
cv2.imshow("Metin Tespiti", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
