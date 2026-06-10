import cv2
import mediapipe as mp

print("🚀 Starting Simple Face Detection...")
print("Press 'q' to quit.")

# Initialize
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open webcam. Make sure camera is not in use.")
    exit()

print("✅ Camera started! Look at the camera.")

with mp_face_detection.FaceDetection(
    model_selection=1, 
    min_detection_confidence=0.5
) as face_detection:

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to get frame")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)
            
            cv2.putText(frame, f"Faces: {len(results.detections)}", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        cv2.imshow("Face Detection (Press Q to Quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("👋 Stopped.")