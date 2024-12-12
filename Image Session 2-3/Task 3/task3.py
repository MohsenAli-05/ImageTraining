import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def make_fig_gray(images, titles, plots, size):
    fig = plt.figure(figsize=size)
    for i in range(len(images)):
        fig.add_subplot(plots[0], plots[1], i+1)
        plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.axis('off')
    plt.show()

img = cv.imread('Task 3/images/cards 1.jpg')
img_copy = img.copy()

# Convert to grayscale and apply Canny edge detection
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
canny = cv.Canny(gray, 20, 100)

contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) #External to show only the outer controls

min_contour_area = 1500  #The threshold for contours, to filter them by area
filtered_contours = [contour for contour in contours if cv.contourArea(contour) > min_contour_area]

cv.drawContours(img_copy, filtered_contours, -1, (255, 0, 0), 3)

print(f"Total contours: {len(contours)}")
print(f"Filtered contours: {len(filtered_contours)}")

images = [canny, img_copy]
titles = ["Canny Edges", "Filtered Contours"]
plots = [1, 2]
size = (30, 10)
make_fig_gray(images, titles, plots, size)

#A list to store combined mask and masked pairs, to show them all together in
combined_images = [] #one window

for contour in filtered_contours:
    mask = np.zeros(img.shape[:2], np.uint8)

    cv.drawContours(mask, [contour], -1, 255, -1)

    masked = cv.bitwise_and(img, img, mask=mask)
    # Convert mask to 3 channels for consistent stacking with masked image
    mask_color = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

    combined = np.hstack((mask_color, masked))
    combined_images.append(combined)

# Chunk the images into groups of 3, to show them all in teh same window
chunk_size = 3
chunks = [combined_images[i:i + chunk_size] for i in range(0, len(combined_images), chunk_size)]

#Display each chunk
current_chunk = 0

while True:
    if chunks:
        #Stack the current chunk vertically
        display_chunk = np.vstack(chunks[current_chunk])

        #Create a resizable OpenCV window
        cv.namedWindow("Contours Scrollable", cv.WINDOW_NORMAL)
        cv.resizeWindow("Contours Scrollable", 800, 800)

        #Display the current chunk
        cv.imshow("Contours Scrollable", display_chunk)

        
        key = cv.waitKey(0) & 0xFF

        if key == 27:  # escape to exit
            break
        elif key == ord('n'):  #'n' for next chunk
            current_chunk = (current_chunk + 1) % len(chunks)
        elif key == ord('p'):  #'p' for previous chunk
            current_chunk = (current_chunk - 1) % len(chunks)
    else:
        print("No contours to display!")
        break

cv.destroyAllWindows()

#After exiting, go to the next image, the cards 2

img = cv.imread('Task 3/images/cards 2.jpg')
img_copy = img.copy()

#Preprocessing the image until I was able to detect the cards properly
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray, (5, 5), 0)

canny = cv.Canny(blurred, 40, 180)
canny = cv.GaussianBlur(canny, (3, 3), 0)

contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

min_contour_area = 8000
filtered_contours = [contour for contour in contours if cv.contourArea(contour) > min_contour_area]

cv.drawContours(img_copy, contours, -1, (255, 0, 0), 3)

print(f"Total contours: {len(contours)}")
print(f"Filtered contours: {len(filtered_contours)}")

images = [canny, img_copy]
titles = ["Canny Edges", "Filtered Contours"]
plots = [1, 2]
size = (30, 10)
make_fig_gray(images, titles, plots, size)

combined_images = []

for contour in filtered_contours:

    mask = np.zeros(img.shape[:2], np.uint8)

    cv.drawContours(mask, [contour], -1, 255, -1)

    masked = cv.bitwise_and(img, img, mask=mask)

    mask_color = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

    combined = np.hstack((mask_color, masked))

    combined_images.append(combined)

# Chunk the images into groups of 3, to display them together
chunk_size = 3
chunks = [combined_images[i:i + chunk_size] for i in range(0, len(combined_images), chunk_size)]

# Display each chunk
current_chunk = 0

while True:
    if chunks:
        # Stack the current chunk vertically
        display_chunk = np.vstack(chunks[current_chunk])

        # Create a resizable OpenCV window
        cv.namedWindow("Contours Scrollable", cv.WINDOW_NORMAL)
        cv.resizeWindow("Contours Scrollable", 800, 800)

        # Display the current chunk
        cv.imshow("Contours Scrollable", display_chunk)

        # Wait for user input
        key = cv.waitKey(0) & 0xFF

        if key == 27:  # ESC key to exit
            break
        elif key == ord('n'):  # 'n' for next chunk
            current_chunk = (current_chunk + 1) % len(chunks)
        elif key == ord('p'):  # 'p' for previous chunk
            current_chunk = (current_chunk - 1) % len(chunks)
    else:
        print("No contours to display!")
        break

cv.destroyAllWindows()
