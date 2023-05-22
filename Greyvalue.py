import cv2
#Dieser Code zeigt das Bild an und durch Mausklick lassen sich die Greyvalues auslesen.
#Dies wird genutzt um den höchsten Helligkeitswert des Hintergrunds auszulesen für die Threshhold function

# Bild Laden
image = cv2.imread('Img_Path', 0)  # Load the image in grayscale


# Definieren der Koordinaten des Ausschnitts
x, y, w, h = 36, 1, 604, 410

# Ausschneiden des Bildes
cropped_img = image[y:y+h, x:x+w]

# Bild Rotieren (180°)
img = cv2.rotate(cropped_img, cv2.ROTATE_180)

# Create a window and bind mouse events to it
cv2.namedWindow('image')

# Mouse callback function
def get_pixel_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_value = img[y, x]  # Get the grayscale value at the cursor's coordinates
        print(f"Grayscale value at ({x}, {y}): {pixel_value}")

# Set the callback function for mouse events
cv2.setMouseCallback('image', get_pixel_value)

while True:
    # Display the image
    cv2.imshow('image', img)

    # Wait for the ESC key to exit the program
    if cv2.waitKey(1) == 27:
        break

# Close all windows
cv2.destroyAllWindows()