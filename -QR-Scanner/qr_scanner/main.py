import cv2
import sys
from qr_utils import detect_codes, display_results

opened_urls = set()

def start_camera(camera_index=0):

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit(1)
    return cap



def main():
    import webbrowser
    cap = start_camera()
    print("Press 'q' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame from camera.")
            break
        codes = detect_codes(frame)

        for code in codes:
            data = code['data']
            if data.startswith('http://') or data.startswith('https://'):
                if data not in opened_urls:
                    opened_urls.add(data)
                    print(f"Opening URL: {data}")
                    webbrowser.open(data)

        frame = display_results(frame, codes)
        cv2.imshow('QR & Barcode Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Unexpected error: {e}")
        cv2.destroyAllWindows()
        sys.exit(1)
