# Color-Based Object Following Robot
### Real-Time Computer Vision and Embedded Robotics with NVIDIA Jetson Nano

A computer vision and robotics project that enables a mobile robot to detect, track, and follow a colored target using a live camera feed. Built with Python, OpenCV, and NVIDIA Jetson Nano, the system processes images in real time and translates the target's position into motor-control commands.

## Project Demo

[Watch the full demonstration]([YOUR_VIDEO_URL](https://drive.google.com/file/d/18oxON_ZiJPSMPRz9SVnipGjGD1LGhGDl/view?usp=sharing))

## Project Overview

Developed as part of a Computer Vision course project, this system combines image processing with embedded hardware control to create an object-following robot.

The robot captures video through a camera connected to the Jetson Nano, identifies a target based on its color, estimates its position within the frame, and adjusts its movement accordingly. The control logic enables the robot to turn left or right, move forward, or stop depending on the target's detected position and apparent size.

## How It Works

1. **Live video capture:** Captures frames from the connected camera using OpenCV.
2. **Color-based detection:** Converts each frame from BGR to HSV color space and applies adjustable color thresholds to isolate the target.
3. **Image processing:** Generates binary color masks, extracts object contours, and filters detections based on contour area.
4. **Target localization:** Identifies the largest qualifying contour and calculates its approximate center coordinates.
5. **Movement decisions:** Compares the target's horizontal position with the center region of the image to determine the required direction.
6. **Motor control:** Sends GPIO output signals from the Jetson Nano to control the robot's two motors, enabling forward movement, turning, or stopping.

## Technology Stack

- **Programming language:** Python
- **Computer vision:** OpenCV
- **Image processing:** HSV color thresholding, binary masking, contour detection, and bounding-box localization
- **Numerical processing:** NumPy
- **Embedded platform:** NVIDIA Jetson Nano
- **Hardware interface:** Jetson.GPIO
- **Input:** Live camera feed
- **Output:** Motor-control signals for a mobile robot

## Hardware Components

- NVIDIA Jetson Nano development board
- Camera compatible with the Jetson Nano
- Two DC motors
- Motor driver and mobile robot chassis
- Appropriate power supply and connecting hardware

*Note: The exact camera, motor-driver model, and chassis specifications are not documented in this repository.*

## Key Features

- Real-time, color-based target detection
- Adjustable HSV thresholds for target-color calibration
- Contour-based object localization
- Position-based movement decisions
- GPIO-based control of two motors
- Visual feedback through OpenCV display windows

## What I Learned

- Applying classical computer vision techniques to a real-world robotics problem.
- Processing live camera frames and extracting useful information from images.
- Translating visual information into movement decisions.
- Integrating Python-based image processing with embedded hardware and GPIO control.
- Working with image segmentation, contour analysis, and hardware-level motor control.

## Limitations and Potential Improvements

- Improve detection reliability under different lighting conditions and complex backgrounds.
- Add camera-based distance estimation or other sensing to improve following distance.
- Implement smoother motor control and more robust target-loss handling.
- Refactor the code into reusable modules and improve error handling.
- Evaluate performance across different target colors, distances, and environmental conditions.

## Repository Contents

- `Object-Following-Robot-Code.py` — Python implementation of the vision-processing and motor-control logic.

## Getting Started

This project was developed for the NVIDIA Jetson Nano hardware environment. Running it requires compatible camera access, GPIO connections, a motor driver, and the relevant Python libraries.

The code uses OpenCV, NumPy, and Jetson.GPIO. Hardware pin assignments and camera configuration must match the physical setup.

**Note:** This is an older academic project. The current code may require debugging or environment-specific adjustments before it can be run successfully.

## Project Context

Academic project | Computer Vision | 2021
