# Touchless Virtual Library

Touchless Virtual Library is a computer vision–based digital reading system that allows users to interact with books using only hand gestures and head movements. The main goal of this project is to create a natural, touch-free interaction system without using a keyboard or mouse.

The system is developed using Python, OpenCV, and MediaPipe. OpenCV is used for real-time video capture, UI rendering, and frame processing. MediaPipe is used for detecting hand landmarks (21 points) and face mesh landmarks (468 points). NumPy is used for mathematical calculations such as distance measurement and angle computation.

The application works in real time using a continuous frame processing loop. Each frame from the webcam is captured, converted from BGR to RGB for MediaPipe compatibility, processed for hand and face detection, and then updated on the interface instantly.

Main Functionalities:

• Hand-Controlled Cursor  
The index fingertip position is tracked to create a smooth virtual cursor. Exponential smoothing is applied to reduce jitter and make movement stable.

• Book Selection (Hover + Hold)  
When the cursor hovers over a book cover, a highlight appears. If the cursor remains there for a few frames, the book opens. This prevents accidental selection.

• Reading Mode  
Once a book is selected, the system loads text from a file, cleans unwanted characters, splits the content into word-based pages, and displays it dynamically.

• Pinch to Zoom  
The distance between the thumb tip and index fingertip is calculated using the Euclidean distance formula. When the distance falls below a threshold, the text size increases. A control mechanism prevents repeated triggering.

• Head Tilt Page Navigation  
The system calculates the angle between the left and right eye landmarks using arctan2. If the tilt exceeds a threshold angle, the page changes accordingly.

• Edge-Based Page Flip  
Moving the cursor to the extreme left or right side of the screen triggers page navigation. Cooldown timers are used to prevent multiple rapid page flips.

• Fist Gesture for Back Navigation  
When all fingers are detected as closed, the system returns to the main menu.

• Sound Feedback  
A page-flipping sound is played asynchronously during navigation to improve user experience without blocking execution.

This project demonstrates how computer vision and gesture recognition can be integrated to build intuitive, real-time human-computer interaction systems. It explores practical applications of landmark detection, gesture logic, UI rendering, and state-based system design.
