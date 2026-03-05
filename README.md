📚 Touchless Virtual Library

A Gesture Controlled Reading Interface using Computer Vision

This project demonstrates a touchless digital reading interface where users can interact with books using hand gestures and head movements instead of a keyboard or mouse.

The system uses MediaPipe and OpenCV to detect hand and face landmarks in real time and convert them into actions like selecting books, zooming text, highlighting lines, and flipping pages.

⸻

🧠 Key Features

🖐 Hand Gesture Navigation

MediaPipe detects 21 hand landmarks and tracks the index finger to act as a virtual cursor.

📖 Hover Based Book Selection

Users can hover the cursor over a book cover for a short duration to open the book.

🔍 Pinch Gesture Zoom

Zoom functionality is implemented by calculating the distance between thumb and index finger.

✨ Dynamic Text Highlighting

When the cursor moves over text lines, the system highlights the corresponding line for better readability.

↔ Edge Based Page Navigation

Moving the cursor to the left or right edge of the screen flips pages.

🧠 Head Tilt Navigation

Using MediaPipe FaceMesh, head tilt is detected to trigger page navigation.

🔊 Interactive Feedback

A page flip sound is played during page transitions to simulate a realistic reading experience.

⸻

🛠 Technologies Used
	•	Python
	•	OpenCV
	•	MediaPipe
	•	NumPy

 📂 Project Structure
 Touchless-Virtual-Library
│
├── project.py                # Main program file
├── requirements.txt          # Required Python libraries
├── README.md                 # Project documentation
│
├── page.wav                  # Page flip sound effect
│
├── pride.jpg                 # Book cover image
├── prideandprejudice.txt     # Book text
│
├── dracula.jpg
├── Dracula.txt
│
├── alice.jpg
├── aliceinwonderland.txt
│
├── sherlock.jpg
├── sherlockholmes.txt
│
├── Frank.jpg
├── Frankenstein.txt

▶ How to Run the Project

1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run the program
python project.py

The webcam will start and the gesture-controlled interface will launch.

💡 What I Learned
	•	Real-time computer vision pipelines
	•	Hand landmark based gesture recognition
	•	Gesture-based human-computer interaction
	•	Building interactive UI systems without traditional input devices

⸻

🔗 Author

Aleena Wilson
Data Science Trainee | Python | Computer Vision

  
