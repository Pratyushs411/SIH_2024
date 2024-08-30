import cv2
import os
import numpy as np
import tensorflow as tf
from darkflow.net.build import TFNet

# Define the YOLO model options
options = {
    'model': './cfg/yolo.cfg',  # Path to the YOLO configuration file
    'load': './bin/yolov2.weights',  # Path to the YOLO weights file
    'threshold': 0.3,  # Minimum confidence threshold for detection
}

# Initialize the TFNet object
tfnet = TFNet(options)

# Define input and output paths
inputPath = os.getcwd() + "/test_images/"
outputPath = os.getcwd() + "/output_images/"


def detectVehicles(filename):
    global tfnet, inputPath, outputPath

    # Read the image
    img = cv2.imread(inputPath + filename, cv2.IMREAD_COLOR)

    # Perform object detection
    result = tfnet.return_predict(img)

    # Loop through the detected objects
    for vehicle in result:
        label = vehicle['label']  # Extract the object label
        if (
            label == "car"
            or label == "bus"
            or label == "bike"
            or label == "truck"
            or label == "rickshaw"
        ):  # Check if the object is a vehicle
            # Draw bounding box and label
            top_left = (vehicle['topleft']['x'], vehicle['topleft']['y'])
            bottom_right = (vehicle['bottomright']['x'], vehicle['bottomright']['y'])
            img = cv2.rectangle(
                img, top_left, bottom_right, (0, 255, 0), 3
            )  # Draw a green bounding box
            img = cv2.putText(
                img,
                label,
                top_left,
                cv2.FONT_HERSHEY_COMPLEX,
                0.5,
                (0, 0, 0),
                1,
            )  # Add the label text

    # Save the output image
    outputFilename = outputPath + "output_" + filename
    cv2.imwrite(outputFilename, img)
    print('Output image stored at:', outputFilename)


# Process all images in the input directory
for filename in os.listdir(inputPath):
    if (
        filename.endswith(".png")
        or filename.endswith(".jpg")
        or filename.endswith(".jpeg")
    ):
        detectVehicles(filename)

print("Done!")