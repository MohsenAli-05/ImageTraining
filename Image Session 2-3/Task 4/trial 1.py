import cv2 as cv
import numpy as np


img = cv.imread("Task 4/Images/original.png")

if img is None:
    print("Error: Image not found.")

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

blurred = cv.GaussianBlur(img_gray, (5, 5), 0)

edges = cv.Canny(blurred, 25, 60)

circles = cv.HoughCircles(
        edges,
        method=cv.HOUGH_GRADIENT,
        dp=1,
        minDist=30, 
        param1=100,
        param2=23, 
        minRadius=0,
        maxRadius=100
    )

if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        center = (circle[0], circle[1]) 
        radius = circle[2]              
        cv.circle(img, center, radius, (255, 0, 0), 2)
        cv.putText(img, "Circle", (center[0] - 15, center[1] - 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)


contours, _ = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

for contour in contours:
    peri = cv.arcLength(contour, True) 
    #calculates the perimeter of the contour, and the true parameter ensures that it's a closed shape
    approx = cv.approxPolyDP(contour, 0.04 * peri, True)
    #Approximates the contour into a polygon with less vertices, the second parameter is the approximation accuracy (4%)
    #and the True means that the contour has to be a closed shape. It does that i order to get straight lines to count
    #and then identify the shape based on

    #Identify shape based on the number of vertices
    if len(approx) == 3:
        shape = "Triangle"
        color = (0, 0, 255)
    elif len(approx) == 4:
        #Check if it's a square (aspect ratio close to 1)
        x, y, w, h = cv.boundingRect(approx)
        aspect_ratio = w / float(h)
        if 0.9 <= aspect_ratio <= 1.1:
            shape = "Square"
            color = (0, 255, 0) 
        else:
            continue
    else:
        # Check for 'X' using intersections
        hull = cv.convexHull(contour) #compute the convex hull -> the smallest polygon to enclose all points
        hull_area = cv.contourArea(hull)
        contour_area = cv.contourArea(contour)
        solidity = contour_area / hull_area if hull_area > 0 else 0
        # solidty tells us how much the shape deviates from being a perfect convex shape. 
        # A solidity close to 1 means the shape is convex, and a value less than 1 suggests concave regions. 
        # An "X" shape, for example, will have lower solidity because it’s not convex.

        if solidity < 0.7 and solidity > 0.025:  #Solidity threshold for 'X'
            shape = "X"
            color = (0, 255, 255)
        else:
            continue


    cv.drawContours(img, [contour], -1, color, 2)
    x, y, w, h = cv.boundingRect(approx)
    cv.putText(img, shape, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Display the result
cv.imshow("edges", edges)
cv.imshow("Detected Shapes", img)
cv.waitKey(0)
cv.destroyAllWindows()

