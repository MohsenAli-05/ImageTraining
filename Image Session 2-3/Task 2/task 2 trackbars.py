import cv2 as cv
import numpy as np

def create_trackbars():  # Function to create adjustable trackbars
    cv.namedWindow("Trackbars")             #I used the trackbars to test for various values and then choose and record the
    cv.resizeWindow("Trackbars", 640, 400)  #most suitable ones and use them. Images of using the trackbars can be found
                                            #in the folder test_images
    cv.createTrackbar("Min Radius", "Trackbars", 50, 500, lambda x: None)
    cv.createTrackbar("Max Radius", "Trackbars", 100, 500, lambda x: None)
    cv.createTrackbar("Canny Th1", "Trackbars", 50, 255, lambda x: None)
    cv.createTrackbar("Canny Th2", "Trackbars", 150, 255, lambda x: None)
    cv.createTrackbar("Hough Param2", "Trackbars", 30, 200, lambda x: None)
    

img = cv.imread("Task 2/images/Ronaldo.jpg") 
img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)  #resize if necessary
original_img = img.copy()

create_trackbars()

while True:
    #Reset the working copy of the image every iterations to delete old circles and draw new ones
    img_copy = original_img.copy()

    #Get values from trackbars
    min_radius = cv.getTrackbarPos("Min Radius", "Trackbars")
    max_radius = cv.getTrackbarPos("Max Radius", "Trackbars")
    canny_th1 = cv.getTrackbarPos("Canny Th1", "Trackbars")
    canny_th2 = cv.getTrackbarPos("Canny Th2", "Trackbars")
    hough_param2 = cv.getTrackbarPos("Hough Param2", "Trackbars")

    gray = cv.cvtColor(img_copy, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 2)

    # Edge detection with Canny
    edges = cv.Canny(blur, canny_th1, canny_th2)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #not necessary, i was testing with it
    contour_img = img.copy()
    cv.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

    # Detect circles using HoughCircles, some values are fixed while others are gotten from the tracbars
    circles = cv.HoughCircles(
        edges,
        method=cv.HOUGH_GRADIENT,
        dp=1,
        minDist=30, #Fixed min dist between points
        param1=100,  #Fixed threshold for edge detection in HoughCircles
        param2=hough_param2,  # Sensitivity of circle detection, gotten from the trackbars
        minRadius=min_radius,
        maxRadius=max_radius
    )

    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1]) 
            radius = circle[2]              
            cv.circle(img_copy, center, radius, (0, 255, 0), 2)
            cv.circle(img_copy, center, 3, (255, 0, 0), 3)

    # Display results
    cv.imshow("Contours", contour_img)
    cv.imshow("Edges", edges)
    cv.imshow("Detected Circles", img_copy)

    # Exit on pressing 'ESC'
    key = cv.waitKey(1) & 0xFF
    if key == ord('p'): #when you want to save the values, press p and the values will get printed
        print(f"Minimum radius: {min_radius}\n")
        print(f"Maximum radius: {max_radius}\n")
        print(f"Canny Threshold 1: {canny_th1}\n")
        print(f"Canny Threshold 2: {canny_th2}\n")
        print(f"Hought Parameter 2: {hough_param2}\n")
    if key == 27:
        break

cv.destroyAllWindows()
