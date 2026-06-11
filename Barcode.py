import cv2
from pyzbar import pyzbar
from datetime import datetime

print("📱 Simple Barcode & QR Scanner")
print("Press 'q' to quit\n")

cap = cv2.VideoCapture(0)  # 0 = default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Cannot access camera")
        break

    # Detect barcodes/QR codes
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        # Get the data
        data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        
        # Draw rectangle and text on screen
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, data, (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Print to console (only once per unique scan)
        print(f"✅ Scanned [{barcode_type}]: {data} | {datetime.now().strftime('%H:%M:%S')}")

    # Show the video feed
    cv2.imshow("Barcode & QR Scanner - Press Q to Quit", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()