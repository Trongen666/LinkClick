import cv2
import numpy as np
import os
from datetime import datetime

class SimpleFaceMatcher:
    def __init__(self, save_dir="saved_faces"):
        """Initialize the face matcher with a directory to save face images"""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.save_dir = save_dir
        
        # Create directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # SIFT for feature detection and matching
        self.sift = cv2.SIFT_create()
        
        # FLANN parameters for feature matching
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    def save_face(self, image, username):
        """Save a face from an image"""
        if isinstance(image, str):  # If path is provided
            img = cv2.imread(image)
        elif isinstance(image, np.ndarray):  # If image is provided
            img = image.copy()
        else:
            raise ValueError("Image must be a path or numpy array")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            print("No face detected")
            return False
        
        # Take the first face
        x, y, w, h = faces[0]
        
        # Extract face region with some margin
        face_img = img[y-20:y+h+20, x-20:x+w+20]
        
        # Save to file
        filename = os.path.join(self.save_dir, f"{username}.jpg")
        cv2.imwrite(filename, face_img)
        
        print(f"Face saved to {filename}")
        return True
    
    def match_faces(self, saved_username, threshold=10):
        """Match live camera feed with a saved face"""
        # Load the saved face
        saved_face_path = os.path.join(self.save_dir, f"{saved_username}.jpg")
        
        if not os.path.exists(saved_face_path):
            print(f"No saved face for {saved_username}")
            return False
        
        saved_face = cv2.imread(saved_face_path)
        saved_face_gray = cv2.cvtColor(saved_face, cv2.COLOR_BGR2GRAY)
        
        # Compute keypoints and descriptors for saved face
        saved_kp, saved_des = self.sift.detectAndCompute(saved_face_gray, None)
        
        # Open camera
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Could not open camera")
            return False
        
        match_result = False
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Create a copy for display
                display_frame = frame.copy()
                
                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                best_match_score = 0
                
                for (x, y, w, h) in faces:
                    # Draw rectangle around face
                    cv2.rectangle(display_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    # Extract face region
                    face_region = gray[y:y+h, x:x+w]
                    
                    # Compute keypoints and descriptors
                    kp, des = self.sift.detectAndCompute(face_region, None)
                    
                    if kp and saved_kp and des is not None and saved_des is not None:
                        # Match descriptors
                        matches = self.flann.knnMatch(saved_des, des, k=2)
                        
                        # Apply ratio test
                        good_matches = []
                        for m, n in matches:
                            if m.distance < 0.7 * n.distance:
                                good_matches.append(m)
                        
                        # Count number of good matches
                        match_count = len(good_matches)
                        
                        if match_count > best_match_score:
                            best_match_score = match_count
                        
                        # Display match count on frame
                        match_text = f"Matches: {match_count}/{threshold}"
                        cv2.putText(display_frame, match_text, (x, y-10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Check if match exceeds threshold
                if best_match_score >= threshold:
                    cv2.putText(display_frame, f"MATCH FOUND: {saved_username}", (30, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    match_result = True
                else:
                    cv2.putText(display_frame, "NO MATCH", (30, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Show frame
                cv2.imshow('Face Recognition', display_frame)
                
                # Wait for key press
                key = cv2.waitKey(1)
                
                # Press 'q' to quit, 'y' to confirm match
                if key == ord('q'):
                    break
                elif key == ord('y'):
                    match_result = True
                    break
                
        finally:
            # Release camera and close windows
            cap.release()
            cv2.destroyAllWindows()
        
        return match_result

def register_new_user(username):
    """Register a new user by capturing and saving their face"""
    matcher = SimpleFaceMatcher()
    
    # Open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Could not open camera")
        return False
    
    saved = False
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to grab frame")
                break
            
            # Show instructions
            cv2.putText(frame, "Press 's' to save your face", (30, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display the frame
            cv2.imshow('Register Face', frame)
            
            # Wait for key press
            key = cv2.waitKey(1)
            
            # Press 's' to save face, 'q' to quit
            if key == ord('s'):
                saved = matcher.save_face(frame, username)
                if saved:
                    print(f"Face registered for user: {username}")
                    break
            elif key == ord('q'):
                break
                
    finally:
        # Release camera and close windows
        cap.release()
        cv2.destroyAllWindows()
    
    return saved

def authenticate_user(username):
    """Authenticate a user by matching their face with saved face"""
    matcher = SimpleFaceMatcher()
    result = matcher.match_faces(username)
    
    if result:
        print(f"Authentication successful for {username}")
    else:
        print(f"Authentication failed for {username}")
    
    return result

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Face Authentication System")
    parser.add_argument("action", choices=["register", "authenticate"], 
                        help="Action to perform")
    parser.add_argument("username", help="Username for registration or authentication")
    
    args = parser.parse_args()
    
    if args.action == "register":
        register_new_user(args.username)
    elif args.action == "authenticate":
        authenticate_user(args.username)