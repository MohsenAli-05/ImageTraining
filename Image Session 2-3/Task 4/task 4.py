import cv2 as cv
import numpy as np

image_files = [
    "original.png",
    "frame1.png",
    "frame2.png",
    "frame3.png",
    "real.jpg",
    "real2.jpg",
    "real3.jpg",
    "real4.png"
]

choice = int(input("Choose an image (0-7): ")) #choose an image from the array
img_path = f"Task 4\\Images\\{image_files[choice]}"
img = cv.imread(img_path)

if img is None:
    raise ValueError("Error: Image not found.")

# Resize the image for faster processing
scale_percent = 50  # Scale image to 50% of its original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
img_resized = cv.resize(img, dim)
img_contours = img_resized.copy()

img_gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(img_gray, (3, 3), 0)
edges = cv.Canny(blurred, 25, 60)

# Morphological operations to improve edge detection, just to close the edge of the shapes since
kernel = np.ones((3, 3), np.uint8)  #some shapes weren't being detected
edges_cleaned = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

# Detect circles
circles = cv.HoughCircles(
    edges_cleaned,
    method=cv.HOUGH_GRADIENT,
    dp=1,
    minDist=30,
    param1=100,
    param2=23,
    minRadius=0,
    maxRadius=40
)

# Draw detected circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        center = (circle[0], circle[1])
        radius = circle[2]
        cv.circle(img_resized, center, radius, (255, 0, 0), 2)
        cv.putText(img_resized, "Circle", (center[0] - 10, center[1] - 25), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

# Find contours using cv.RETR_TREE for hierarchical information
contours, hierarchy = cv.findContours(edges_cleaned, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Filter contours and identify shapes
min_contour_area = 100  # Minimum area of contours to keep

for contour in contours:
    area = cv.contourArea(contour)
    
    if area > min_contour_area:

        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.03 * peri, True)

        # Check circularity for circles, because circles were being double detected as Xs
        x, y, w, h = cv.boundingRect(contour)
        aspect_ratio = w / float(h)
        circularity = (4 * np.pi * area) / (peri ** 2) if peri > 0 else 0
        is_circle = 0.85 <= circularity <= 1.15 and aspect_ratio >= 0.9 and aspect_ratio <= 1.1

        # Identify shapes based on number of vertices
        if len(approx) == 3:
            shape = "Triangle"
            color = (0, 0, 255)
        elif len(approx) == 4 and 0.9 <= aspect_ratio <= 1.1:
            shape = "Square"
            color = (0, 255, 0)
        elif len(approx) >= 8 and not is_circle:
            shape = "X"
            color = (0, 255, 255)
        else:
            continue

        # Draw contours and label detected shapes
        cv.drawContours(img_resized, [contour], -1, color, 2)
        cv.putText(img_resized, shape, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

cv.imshow("Detected Shapes", img_resized)
cv.waitKey(0)
cv.destroyAllWindows()
