import cv2
import numpy as np
import numpy as np
import pandas as pd
import tkinter as tk

def color_detection_via_image():
    # Path to the image
    img_path = "./image.jpg"

    # Reading the image with OpenCV
    img = cv2.imread(img_path)
    img_original = img.copy()  # Store a copy of the original image

    # Declaring global variables (are used later on)
    clicked = False
    r = g = b = xpos = ypos = 0

    # Reading CSV file with pandas and giving names to each column
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('./colors.csv', names=index, header=None)

    # Function to calculate minimum distance from all colors and get the most matching color
    def getColorName(R, G, B):
        minimum = 10000
        for i in range(len(csv)):
            d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
            if d <= minimum:
                minimum = d
                cname = csv.loc[i, "color_name"]
        return cname

    # Function to get x, y coordinates of mouse double click
    def draw_function(event, x, y, flags, param):
        nonlocal b, g, r, xpos, ypos, clicked
        if event == cv2.EVENT_LBUTTONDBLCLK:
            clicked = True
            xpos = x
            ypos = y
            b, g, r = img[y, x]
            b = int(b)
            g = int(g)
            r = int(r)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)

    while True:
        if clicked:
            # Restore the original image
            img = img_original.copy()

            # Draw the rectangle with the selected color
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

            # Create the text string to display (Color name and RGB values) and convert it to uppercase
            text = getColorName(r, g, b).upper() + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

            # Change font style and size here
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 1.2
            thickness = 1

            # For very light colors we will display text in black color
            color = (255, 255, 255)
            if r + g + b >= 600:
                color = (0, 0, 0)

            # Draw the text multiple times to simulate a bold effect
            for i in range(1, 5):
                cv2.putText(img, text, (50 + i, 50 + i), font, font_scale, color, thickness, cv2.LINE_AA)

            clicked = False

        # Display the image
        cv2.imshow("image", img)

        # Break the loop when the user hits the 'esc' key or closes the window
        if cv2.waitKey(20) & 0xFF == 27:
            break
        if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

def color_detection_via_camera():
    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        exit()

    # Set font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_thickness = 2

    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        cx = int(width / 2)
        cy = int(height / 2)

        # Pick pixel value
        pixel_center = hsv_frame[cy, cx]

        # Define color ranges in HSV
        color_ranges = {
            'red': ([0, 70, 50], [10, 255, 255]),
            'green': ([40, 70, 50], [80, 255, 255]),
            'blue': ([100, 70, 50], [130, 255, 255]),
            'yellow': ([20, 70, 50], [40, 255, 255]),
            'orange': ([10, 70, 50], [20, 255, 255]),
            'black': ([0, 0, 0], [180, 255, 30]),
            'white': ([0, 0, 200], [180, 30, 255]),
            'pink': ([140, 70, 50], [170, 255, 255]),
        }

        detected_color = None
        for color_name, (lower, upper) in color_ranges.items():
            lower = np.array(lower)
            upper = np.array(upper)
            mask = cv2.inRange(hsv_frame, lower, upper)
            if mask[cy, cx] == 255:  # Check if the center pixel is within the color range
                detected_color = color_name
                break

        # Draw a black circle at the center of the frame
        cv2.circle(frame, (cx, cy), 5, (0, 0, 0), 3)

        # Draw the detected color text at the top center of the frame
        text_size = cv2.getTextSize(detected_color, font, font_scale, font_thickness)[0]
        text_x = int((width - text_size[0]) / 2)
        cv2.putText(frame, detected_color, (text_x, 50), font, font_scale, (255, 255, 255), font_thickness)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    pass

def open_image():
    # Call color detection function with the specified image path
    color_detection_via_image()

def main():
    root = tk.Tk()
    root.title("Color Detection Options")

    # Set the window size and position
    window_width = 500
    window_height = 250  # Adjust the height as needed
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    # Change background color of the window
    root.config(bg="lightblue")

    # Add label for title
    label_title = tk.Label(root, text="Choose Your Colour Detection Method From Below -", bg="lightblue")
    label_title.pack(pady=15)

    # Create buttons with custom colors and padding
    button_camera = tk.Button(root, text="Via Camera", command=color_detection_via_camera, bg="lightgreen", fg="black", padx=12, pady=6)
    button_camera.pack(pady=(0, 15))  # Add some padding between buttons

    button_image = tk.Button(root, text="Via Image", command=open_image, bg="lightgreen", fg="black", padx=12, pady=6)
    button_image.pack(pady=(0, 15))  # Add some padding between buttons

    # Close the window when clicking the "x" button
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()

if __name__ == "__main__":
    main()

