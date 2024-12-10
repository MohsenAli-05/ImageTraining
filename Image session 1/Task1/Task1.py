import cv2 as cv
import keyboard

drawing = False
x1, y1 = -1, -1
cropped_image = None

def draw_rectangle(event,x,y,flags,param):
    global x1, y1, color, temp_image, image, drawing, r
    if r:
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            x1, y1 = x,y #save the current mouse coords
            temp_image = image.copy()
        elif event == cv.EVENT_MOUSEMOVE: #show the rect as it's being drawn
            if drawing:
                image=temp_image.copy() #on a copy of the image to not save on the actual image
                cv.rectangle(image, (x1, y1), (x, y), (255,0,255), 3)
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False
            cv.rectangle(image, (x1,y1), (x,y), (255,0,255), 3) #startsPts, endPts, drawColor, thickness (use -ve to fill)   

def crop_and_save(event, x, y, flags, param):
    global drawing, x1, y1, cropped_image, image, cropImgCounter
    if crop:
        if event == cv.EVENT_LBUTTONDOWN: 
            drawing = True
            x1, y1 = x, y 
     
        elif event == cv.EVENT_MOUSEMOVE: 
            if drawing:
                temp_image = image.copy() 
                cv.rectangle(temp_image, (x1, y1), (x, y), (0,0,255), 3)
                cv.imshow("Image", temp_image)
     
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False
            xStart, xEnd = min(x1, x), max(x1, x)
            yStart, yEnd = min(y1, y), max(y1, y)
            cropped_image = image[yStart:yEnd, xStart:xEnd]
     
            if cropped_image.size > 0:
                cv.imshow("Cropped Image", cropped_image)
     
                while True:
                    key = cv.waitKey(1) & 0xFF
                    if key == 13:  # press enter to save
                        cv.imwrite(f"Task1/cropped_images/cropped-image-{cropImgCounter}.png", cropped_image)
                        print(f"Cropped image saved as 'cropped-image-{cropImgCounter}'.")
                        cv.destroyWindow("Cropped Image")
                        cropImgCounter +=1
                        break
                    elif key == ord('q'):  # press q to cancel
                        print("Cropping canceled. Image not saved.")
                        cv.destroyWindow("Cropped Image")
                        break

    
crop = False
r=0
cropImgCounter = 0
image_path='images/bunny.jpeg'
image=cv.imread(image_path)

print("Click 'r' to draw a rectangle and 'c' to crop" )

while True:
    cv.imshow('Image',image)

    key = cv.waitKey(1) &0xFF
    if key == 27:
        break
    if key == ord('c'):
        if crop == False:
            print("Select an area, click enter to save and 'q' to cancel")
            crop = True
            cv.setMouseCallback("Image",crop_and_save)
        elif crop:
            crop = False
            cv.destroyWindow("Cropped Image")
    
    if key == ord('r'):
        if r == False:
            print("Use mouse to drawe rectangles")
            r = True
            cv.setMouseCallback("Image", draw_rectangle)
        elif r:
            r = False
    


cv.destroyAllWindows()

