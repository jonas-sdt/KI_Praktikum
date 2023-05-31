import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage.util import img_as_ubyte



# Laden des Bildes
img = cv2.imread("img_path")
cv2.imshow("anfangs bild", img)
cv2.waitKey(0)

# Definieren der Koordinaten des Ausschnitts
x, y, w, h = 17, 77, 528, 403       # x und y Koordinaten vom Eckpunkt oben links des Bildes + width + height (durch Paint leicht bestimmbar)

# Ausschneiden des Bildes
cropped_img = img[y:y+h, x:x+w]
cv2.imshow("Cropped Image", cropped_img)
cv2.waitKey(0)

#Dieser Block wird nur verwendet falls das Bild um ca 1-5° verdreht ist. (muss ich durch Testbilder mal schauen wies am ende ist)
# Bestimmung der Drehmatrix
#rows, cols = img.shape[:2]
#theta = 1 # 1 Grad
#M = cv2.getRotationMatrix2D((cols/2, rows/2), theta, 1)
#rotated_img = cv2.warpAffine(img, M, (cols, rows))

# Bild Rotieren um 180°
rota = cv2.rotate(cropped_img, cv2.ROTATE_180)
cv2.imshow("rotiertes bild", rota)
cv2.waitKey(0)

# Konvertieren des Bildes in Graustufen
gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
cv2.imshow("greyscaled bild", gray)
cv2.waitKey(0)

# Bild blurren
blur_img = cv2.GaussianBlur(gray, (5, 5), 0)

# Anwenden der Schwellwertfunktion
ret, thresh_img = cv2.threshold(blur_img, 115, 255, cv2.THRESH_BINARY)

cv2.imshow("Threshold Image", thresh_img)
cv2.waitKey(0)

# Definieren des Dilatationskernels
kernel = np.ones((3, 3), np.uint8)

# Anwenden der Dilatation
image = cv2.dilate(thresh_img, kernel, iterations=1)
cv2.imshow("dialation", image)
cv2.waitKey(0)

# Anwenden der Skeletierung
skeleton = skeletonize(image)

final = img_as_ubyte(skeleton) #Bild von skimage Format in cv2 Format umwandeln
cv2.imshow("image", final)
cv2.waitKey(0)

arr = np.where(final == 255, 1, final)   #ändert im array 255 Werte auf 1
np.savetxt("final.txt", arr, fmt='%d')   #speichert das array in einer Textdatei (damit kann man sich das Array genauer anschauen
