import cv2 as cv
import numpy as np

img_path = 'images/bunny.jpeg'
image = cv.imread(img_path)

lower_bound = None
upper_bound = None

def get_hsv_bounds(event, x, y, flags, param):
    global lower_bound, upper_bound, hsv_image

    if event == cv.EVENT_LBUTTONDOWN:
        pixel_hsv = hsv_image[y, x]
        lower_bound = np.array([max(0, pixel_hsv[0] - 10), max(0, pixel_hsv[1] - 40), max(0, pixel_hsv[2] - 40)])
        #since the pixel 20px away could be of a completely different colof if you chose a pixel on the edge,
        #I +- 10 from the hue value of the selected pixel and +- 40 from the saturation and value
        #I used the min and max functions to make sure the values are within the range for hsv
        upper_bound = np.array([min(179, pixel_hsv[0] + 10), min(255, pixel_hsv[1] + 40), min(255, pixel_hsv[2] + 40)])

        print("Lower Bound:", lower_bound)
        print("Upper Bound:", upper_bound)
        print("press 'c' to reset mask\n\n")

hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

cv.namedWindow("Image")
cv.setMouseCallback("Image", get_hsv_bounds)

while True:
    if lower_bound is not None and upper_bound is not None:
        mask = cv.inRange(hsv_image, lower_bound, upper_bound)

        mask_results = cv.bitwise_and(image, image, mask=mask)

        cv.imshow("Mask", mask)
        cv.imshow("Result", mask_results)

    else:
        cv.imshow("Mask", np.zeros_like(image[:, :, 0]))
        cv.imshow("Result", np.zeros_like(image))

    cv.imshow("Image", image)

    key = cv.waitKey(1)
    if key == 27:  
        break
    if key == ord('c'): #pressing c will reset mask
        lower_bound = None
        upper_bound = None

cv.destroyAllWindows()  
