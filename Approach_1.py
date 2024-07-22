# -*- coding: utf-8 -*-
"""
Created on Fri May 24 12:41:42 2024

@author: amitc
"""
import cv2
import numpy as np
import sys

video_path = 'C:/Users/amitc/Downloads/Post_Doc_IIT_Madras/'
video_name = 'Postdoc Task.mp4'

all_centers = []
center_colors = []

def is_point_in_polygon(point, vertices):
    x, y = point
    n = len(vertices)
    inside = False
    p1x, p1y = vertices[0]
    for i in range(1, n + 1):
        p2x, p2y = vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def calculate_distance(coords1, coords2):
    x1, y1, _, _ = coords1
    x2, y2, _, _ = coords2
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def detect_and_draw(frame, frame_coords, lower_color, upper_color, fixed_width, fixed_height, frame_color):
    global all_centers, center_colors
    
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Threshold the HSV image to get only colors in specified range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Perform morphological operations to remove small blobs
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize variables to store current bounding box coordinates
    current_bbox_coords = None
    current_center = None

    # Draw bounding box for the largest contour within frame coordinates
    for contour in contours:
        # Calculate centroid of contour
        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # Check if centroid is within the specified frame coordinates
            if is_point_in_polygon((cx, cy), frame_coords):
                x = cx - fixed_width // 2
                y = cy - fixed_height // 2
                current_bbox_coords = (x, y, x + fixed_width, y + fixed_height)
                current_center = (cx, cy)
                
                if len(all_centers) == 0 or calculate_distance(current_bbox_coords, (*all_centers[-1], 0, 0)) < 1050:
                    # Draw the bounding box
                    cv2.rectangle(frame, (x, y), (x + fixed_width, y + fixed_height), frame_color, 2)
                    
                    # Calculate the center of the rectangle
                    center_x = x + fixed_width // 2
                    center_y = y + fixed_height // 2
                    
                    # Add the current center to the list of all centers
                    all_centers.append((center_x, center_y))
                    center_colors.append(frame_color)  # Save the color used for this center
                
                break  

    # Draw all previous centers with their respective colors
    dot_radius = 3  # Radius of the dot
    for center, color in zip(all_centers, center_colors):
        cv2.circle(frame, center, dot_radius, color, -1)

    return frame


frame_coords = [(113, 144), (849, 131), (855, 838), (128, 836)]

# Open the video file
cap = cv2.VideoCapture(video_path + video_name)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()

# Get video frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_path + 'output.avi', fourcc, 20.0, (frame_width, frame_height))

# Read until the end of the video
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if ret:
        # Detect blue color and draw bounding box
        fixed_width, fixed_height = 80, 80
        frame_color_1 = (255, 0, 0)
        frame_color_2 = (0, 0, 255)


        lower_blue = np.array([110, 30, 50])
        upper_blue = np.array([120, 255, 120])
    
    
        lower_red = np.array([14, 29, 74])
        upper_red = np.array([41, 69, 171])
        

        frame_with_box = detect_and_draw(frame, frame_coords, lower_blue, upper_blue, fixed_width, fixed_height, frame_color_1)
        frame_with_box = detect_and_draw(frame, frame_coords, lower_red, upper_red, fixed_width, fixed_height, frame_color_2)

        # Display the frame
        frame_with_box_resized = cv2.resize(frame_with_box, (800, 600))  # width, height
        cv2.imshow('Frame', frame_with_box_resized)

        # Write frame to output video
        out.write(frame_with_box)

        # Press 'q' on keyboard to exit the loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Save positional information
np.save(video_path + 'positional_info.npy', np.array(all_centers))

# Release the VideoWriter object along with VideoCapture and other cleanups
cap.release()
out.release()
cv2.destroyAllWindows()
