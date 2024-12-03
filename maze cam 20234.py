import cv2
import numpy as np

rl = (0, 0, 60)
rm = (65, 40, 255)
yl = (0, 80, 125)
ym = (85, 255, 255)
gl = (0, 65, 0)
gm = (95, 255, 140)

def create_trackbars():
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 640, 240)

    cv2.createTrackbar("R min", "Trackbars", 0, 255, lambda x: None)
    cv2.createTrackbar("R max", "Trackbars", 255, 255, lambda x: None)
    cv2.createTrackbar("G min", "Trackbars", 0, 255, lambda x: None)
    cv2.createTrackbar("G max", "Trackbars", 255, 255, lambda x: None)
    cv2.createTrackbar("B min", "Trackbars", 0, 255, lambda x: None)
    cv2.createTrackbar("B max", "Trackbars", 255, 255, lambda x: None)
    cv2.createTrackbar("Black min", "Trackbars", 0, 255, lambda x: None)
    cv2.createTrackbar("Black max", "Trackbars", 30, 255, lambda x: None)

def colors_detection(img):
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hmin = cv2.getTrackbarPos("R min", "Trackbars")
    hmax = cv2.getTrackbarPos("R max", "Trackbars")
    smin = cv2.getTrackbarPos("G min", "Trackbars")
    smax = cv2.getTrackbarPos("G max", "Trackbars")
    vmin = cv2.getTrackbarPos("B min", "Trackbars")
    vmax = cv2.getTrackbarPos("B max", "Trackbars")
    black_min = cv2.getTrackbarPos("Black min", "Trackbars")
    black_max = cv2.getTrackbarPos("Black max", "Trackbars")

    lower = np.array([vmin, smin, hmin])
    upper = np.array([vmax, smax, hmax])
    mask = cv2.inRange(img,lower,upper)
    maskr = cv2.inRange(img, rl, rm)
    masky = cv2.inRange(img, yl, ym)
    maskg = cv2.inRange(img, gl, gm)

    imgfinal = cv2.bitwise_and(img,img,mask=mask)
    imgr = cv2.bitwise_and(img, img, mask=maskr)
    imgy = cv2.bitwise_and(img, img, mask=masky)
    imgg = cv2.bitwise_and(img, img, mask=maskg)

    averager = cv2.mean(imgr)[0]
    averagey = cv2.mean(imgy)[0]
    averageg = cv2.mean(imgg)[0]

    if averager < 0.4:
        print("Not Red")
    else:
        print("Red")
        color_present = "red"

    if averagey < 0.4:
        print("Not Yellow")
    else:
        print("Yellow")
        color_present = "yellow"

    if averageg < 0.4:
        print("Not Green")
    else:
        print("Green")
        color_present = "green"

    cv2.imshow("og", img)
    #cv2.imshow("hsv", imghsv)
    cv2.imshow("mask", mask)
    cv2.imshow("Result", imgfinal)

    return color_present

def get_mean_color(img):

    mean_color = np.mean(img, axis = (0,1))
    return mean_color

def letter_detection(img):
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayscale_img, 127, 255, cv2.THRESH_BINARY)

    letter = cv2.bitwise_not(blackAndWhiteImage)

    cnts = cv2.findContours(letter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        letter = letter[y:y + h, x:x + w]

    h, w = letter.shape
    letter_type = "N"

    third = h // 3
    top = letter[:third, :]
    middle = letter[third:third * 2, :]
    bottom = letter[third * 2:, :]

    cnts = cv2.findContours(top, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    c1 = (len(cnts))

    cnts = cv2.findContours(middle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    c2 = (len(cnts))

    cnts = cv2.findContours(bottom, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    c3 = (len(cnts))

    if c1 == 1 and c3 == 1:
        # print("S victim")
        letter_type = "S"
    elif c1 == 2 and c2 == 1 and c3 == 2:
        # print("H victim")
        letter_type = "H"

    elif c1 == 2 and c2 == 2 and c3 == 1:
        # print("U victim")
        letter_type = "U"

    return letter_type


path = cv2.VideoCapture(0)
# path = "D:\\Maze 24\\Screenshot 2023-12-14 220434.png"
create_trackbars()

while True:
    # success, img = path.read()
    img = cv2.imread("geeksforgeeks.png", cv2.IMREAD_COLOR)

    colors_detection(img)
    cv2.waitKey(1)



# print(letter_type)

# cv2.imshow("img", letter)

# cv2.waitKey(10000)
# cv2.destroyAllWindows()