import cv2
import numpy as np
import os

def process_static_image():
    """Process static image - show only blue channel"""
    print("\n=== STEP 2: Process Static Image ===")
    
    current_dir = os.getcwd()
    possible_names = ['image.jpg', 'image.jpeg', 'variant-4.jpg', 'variant-4.jpeg']
    
    img = None
    for name in possible_names:
        if os.path.exists(name):
            img = cv2.imread(name)
            if img is not None:
                break
    
    if img is None:
        print("Error: Cannot find image file!")
        return False
    
    blue = img.copy()
    blue[:, :, 1] = 0  
    blue[:, :, 2] = 0  
    
    cv2.imshow('Original Image', img)
    cv2.imshow('Blue Channel Only', blue)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def track_marker():
    """Track custom marker and check if in right half of screen"""
    print("\n=== STEP 3: Camera Tracking ===")
    print("Press 'q' to quit")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width == 0 or height == 0:
        width, height = 640, 480
    mid_x = width // 2
    
    print(f"Camera resolution: {width} x {height}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        blue = frame.copy()
        blue[:, :, 1] = 0
        blue[:, :, 2] = 0
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bin =cv2.threshold(gray, 100, 250, cv2.THRESH_BINARY)
        
        # Detect lines using Hough Transform to find the marker shape
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 50, param1=60, param2=40, minRadius=100, maxRadius=120)
      
        if circles is not None and len(circles):
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0,0, 255), 2)
            # lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
            #                         minLineLength=50, maxLineGap=10)
            
            # marker_detected = False
            # marker_center = None
            
            # if lines is not None:
            #     # Look for intersecting lines that form the cross shape
            #     vertical_lines = []
            #     horizontal_lines = []
                
            #     for line in lines:
            #         x1, y1, x2, y2 = line[0]
            #         angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
                    
            #         if angle < 20 or angle > 160:
            #             horizontal_lines.append(line[0])
            #         elif 70 < angle < 110:
            #             vertical_lines.append(line[0])
                
            #     if len(vertical_lines) > 0 and len(horizontal_lines) > 0:
            #         marker_detected = True
                    
            #         vx_center = np.mean([(x1 + x2) // 2 for x1, y1, x2, y2 in vertical_lines])
            #         hy_center = np.mean([(y1 + y2) // 2 for x1, y1, x2, y2 in horizontal_lines])
            #         marker_center = (int(vx_center), int(hy_center))
                    
            #         cv2.circle(frame, marker_center, 10, (0, 0, 255), 2)
                    
            #         if marker_center[0] > mid_x:
            #             status = "IN RIGHT HALF"
            #             color = (0, 255, 0)
            #         else:
            #             status = "IN LEFT HALF"
            #             color = (0, 0, 255)
                    
            #         cv2.putText(blue, status, (mid_x + 20, 100), 
            #                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # cv2.line(frame, (mid_x, 0), (mid_x, height), (255, 255, 255), 2)
            # cv2.putText(frame, "LEFT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            # cv2.putText(frame, "RIGHT", (mid_x + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # if marker_detected:
            #     cv2.putText(frame, "MARKER DETECTED", (10, 60), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Tracking - Blue Channel', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("=" * 40)
    print("LAB 8 - VARIANT 4")
    print("=" * 40)
    
    while True:
        print("\nMenu:")
        print("1. Process static image")
        print("2. Start camera tracking")
        print("3. Exit")
        
        choice = input("Choose (1-3): ")
        
        if choice == '1':
            process_static_image()
        elif choice == '2':
            track_marker()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted")
