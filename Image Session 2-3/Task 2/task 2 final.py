import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def display_image(image, title='original', colored=None):
    plt.figure(figsize=(10, 10))
    if colored:
        plt.imshow(image[:,:,::-1]) # converting from bgr to rgb
    else:
        plt.imshow(image, cmap='gray')
    plt.axis("off")
    plt.title(title)
    plt.show()

img1 = cv.imread("Task 2/images/Ronaldo.jpg") 
img1 = cv.resize(img1, (0, 0), fx=0.5, fy=0.5)
img1_copy = img1.copy()

gray1 = cv.cvtColor(img1_copy, cv.COLOR_BGR2GRAY)
blur1 = cv.GaussianBlur(gray1, (9, 9), 2)

edges1 = cv.Canny(blur1, 56, 75)

circles1 = cv.HoughCircles(
        edges1,
        method=cv.HOUGH_GRADIENT,
        dp=1,
        minDist=30,
        param1=100, 
        param2=31,  
        minRadius=55,
        maxRadius=86
    )


img2 = cv.imread("Task 2/images/brown-eyes.jpg") 
img2 = cv.resize(img2, (0, 0), fx=0.5, fy=0.5)
img2_copy = img2.copy()

gray2 = cv.cvtColor(img2_copy, cv.COLOR_BGR2GRAY)
blur2 = cv.GaussianBlur(gray2, (9, 9), 2)

edges2 = cv.Canny(blur2, 50, 150)

circles2 = cv.HoughCircles(
        edges2,
        method=cv.HOUGH_GRADIENT,
        dp=1,
        minDist=30,
        param1=100, 
        param2=21,  
        minRadius=0,
        maxRadius=63
    )

if circles1 is not None:
        circles1 = np.uint16(np.around(circles1))
        for circle in circles1[0, :]:
            center = (circle[0], circle[1]) 
            radius = circle[2]              
            cv.circle(img1_copy, center, radius, (0, 255, 0), 2)
            cv.circle(img1_copy, center, 3, (255, 0, 0), 3)

if circles2 is not None:
        circles2 = np.uint16(np.around(circles2))
        for circle in circles2[0, :]:
            center = (circle[0], circle[1]) 
            radius = circle[2]              
            cv.circle(img2_copy, center, radius, (0, 255, 0), 2)
            cv.circle(img2_copy, center, 3, (255, 0, 0), 3)

display_image(img1_copy, colored=1)
display_image(img2_copy, colored=1)



