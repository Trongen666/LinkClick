# from fastapi import WebSocket, WebSocketDisconnect
# import json
# import base64
# import cv2
# import numpy as np
# import asyncio
# from datetime import datetime
# from typing import Dict, List, Optional

# from .face_auth_backend import SimpleFaceMatcher, create_access_token

# # WebSocket manager
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
        
#     async def send_personal_json(self, data: dict, websocket: WebSocket):
#         await websocket.send_text(json.dumps(data))

# manager = ConnectionManager()
# face_matcher = SimpleFaceMatcher()

# # Function to handle the webcam authentication
# async def handle_face_auth_webcam(websocket: WebSocket, username: str):
#     """
#     Handle the webcam authentication process with 15-second timer and 3 attempts
#     """
#     try:
#         # Check if the username exists (load saved face)
#         face_path = f"{face_matcher.save_dir}/{username}.jpg"
        
#         import os
#         if not os.path.exists(face_path):
#             await manager.send_personal_json(
#                 {"status": "error", "message": "User not found"}, 
#                 websocket
#             )
#             return False
        
#         # Setup timer variables
#         MAX_TIME = 15  # 15 seconds
#         CAPTURES = 3   # Capture 3 times (every 5 seconds)
#         AUTH_THRESHOLD = 10  # Match threshold
        
#         # Tell client to start capturing
#         await manager.send_personal_json(
#             {"status": "info", "message": f"Starting authentication for {username}. You have {MAX_TIME} seconds."}, 
#             websocket
#         )
        
#         # Time remaining counter
#         for i in range(CAPTURES):
#             # Tell client we are capturing
#             capture_number = i + 1
#             await manager.send_personal_json(
#                 {"status": "capturing", "message": f"Capture {capture_number}/{CAPTURES}", "seconds_left": MAX_TIME - (i * 5)}, 
#                 websocket
#             )
            
#             # Wait for client to send an image
#             try:
#                 data = await asyncio.wait_for(websocket.receive_text(), timeout=6.0)
#                 data = json.loads(data)
                
#                 if "image" not in data:
#                     await manager.send_personal_json(
#                         {"status": "error", "message": "No image received"}, 
#                         websocket
#                     )
#                     continue
                
#                 # Process base64 image
#                 base64_image = data["image"]
                
#                 # Remove data URL prefix if present
#                 if ',' in base64_image:
#                     base64_image = base64_image.split(',', 1)[1]
                
#                 # Decode base64 image
#                 image_bytes = base64.b64decode(base64_image)
                
#                 # Create a temporary user name for comparison
#                 temp_username = f"temp_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
#                 # Convert bytes to OpenCV image
#                 nparr = np.frombuffer(image_bytes, np.uint8)
#                 img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
#                 if img is None:
#                     await manager.send_personal_json(
#                         {"status": "error", "message": "Invalid image format"}, 
#                         websocket
#                     )
#                     continue
                
#                 # Save face for comparison
#                 saved = face_matcher.save_face(img, temp_username)
                
#                 if not saved:
#                     await manager.send_personal_json(
#                         {"status": "error", "message": "No face detected"}, 
#                         websocket
#                     )
#                     continue
                
#                 # Compare with stored face
#                 match = face_matcher.compare_saved_faces(temp_username, username, AUTH_THRESHOLD)
                
#                 # Clean up temporary file
#                 temp_path = f"{face_matcher.save_dir}/{temp_username}.jpg"
#                 if os.path.exists(temp_path):
#                     os.remove(temp_path)
                
#                 if match:
#                     # Authentication success
#                     access_token = create_access_token(data={"sub": username})
#                     await manager.send_personal_json(
#                         {
#                             "status": "success", 
#                             "message": "Authentication successful", 
#                             "access_token": access_token,
#                             "token_type": "bearer"
#                         }, 
#                         websocket
#                     )
#                     return True
#                 else:
#                     # Authentication failed for this attempt
#                     await manager.send_personal_json(
#                         {"status": "attempt_failed", "message": f"Attempt {capture_number} failed. Trying again..."}, 
#                         websocket
#                     )
            
#             except asyncio.TimeoutError:
#                 await manager.send_personal_json(
#                     {"status": "timeout", "message": f"Timed out waiting for capture {capture_number}"}, 
#                     websocket
#                 )
        
#         # All attempts failed
#         await manager.send_personal_json(
#             {"status": "auth_failed", "message": "Authentication failed after all attempts"}, 
#             websocket
#         )
#         return False
        
#     except Exception as e:
#         await manager.send_personal_json(
#             {"status": "error", "message": f"Error during authentication: {str(e)}"}, 
#             websocket
#         )
#         return False

# # Register WebSocket route in FastAPI app
# def register_websocket_routes(app):
#     @app.websocket("/ws/auth/{username}")
#     async def websocket_auth(websocket: WebSocket, username: str):
#         await manager.connect(websocket)
#         try:
#             await handle_face_auth_webcam(websocket, username)
#         except WebSocketDisconnect:
#             manager.disconnect(websocket)
#         except Exception as e:
#             await manager.send_personal_json(
#                 {"status": "error", "message": f"Error: {str(e)}"}, 
#                 websocket
#             )
#             manager.disconnect(websocket)

# face_matcher.py
# import os, cv2, numpy as np
# from datetime import datetime
# from ..config import settings

# class SimpleFaceMatcher:
#     def __init__(self, save_dir=settings.FACE_SAVE_DIR):
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         self.save_dir, self.sift = save_dir, cv2.SIFT_create()
#         if not os.path.exists(save_dir): os.makedirs(save_dir)
#         self.flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))

#     def save_face(self, image, username):
#         if isinstance(image, str): image = cv2.imread(image)
#         if image is None: return False
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
#         if not faces.any(): return False
#         x, y, w, h = faces[0]
#         face_img = image[max(0, y-20):y+h+20, max(0, x-20):x+w+20]
#         return cv2.imwrite(os.path.join(self.save_dir, f"{username}.jpg"), face_img)

#     def compare_saved_faces(self, u1, u2, threshold=settings.FACE_MATCH_THRESHOLD):
#         def load_gray(path): return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
#         try:
#             kp1, des1 = self.sift.detectAndCompute(load_gray(f"{self.save_dir}/{u1}.jpg"), None)
#             kp2, des2 = self.sift.detectAndCompute(load_gray(f"{self.save_dir}/{u2}.jpg"), None)
#             matches = self.flann.knnMatch(des1, des2, k=2)
#             good = [m for m, n in matches if m.distance < 0.7 * n.distance]
#             return len(good) >= threshold
#         except: return False

#     def verify_face_from_image(self, image_bytes: bytes, username: str) -> bool:
#         img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
#         if img is None: return False
#         temp_user = f"temp_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
#         if not self.save_face(img, temp_user): return False
#         match = self.compare_saved_faces(temp_user, username)
#         os.remove(os.path.join(self.save_dir, f"{temp_user}.jpg"))
#         return match

# face_matcher = SimpleFaceMatcher()


# import os
# import cv2
# import numpy as np
# from datetime import datetime
# from ..config import settings
# from sklearn.metrics.pairwise import cosine_similarity
# from ..utils.db import users_collection

# from pymongo import MongoClient

# class SimpleFaceMatcher:
#     def __init__(self, save_dir=settings.FACE_SAVE_DIR):
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         self.save_dir = save_dir
#         self.sift = cv2.SIFT_create()
#         if not os.path.exists(save_dir):
#             os.makedirs(save_dir)
#         self.flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
#         # Setup MongoDB connection
#         self.client = MongoClient('mongodb://localhost:27017/')
#         self.db = self.client["face_database"]
#         self.users_collection = self.db["users"]

#     def save_face(self, image, username):
#         """This function saves the face image in the database."""
#         if isinstance(image, str):
#             image = cv2.imread(image)
#         if image is None:
#             return False
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
#         if not faces.any():
#             return False
#         x, y, w, h = faces[0]
#         face_img = image[max(0, y-20):y+h+20, max(0, x-20):x+w+20]

#         # Extract the face embedding from the image
#         embedding = self.extract_face_embedding(face_img)
#         if embedding is None:
#             return False

#         # Save the embedding in the database instead of the filesystem
#         user_data = {
#             "username": username,
#             "face_embedding": embedding.tolist(),  # Convert numpy array to list for MongoDB storage
#             "timestamp": datetime.now()
#         }

#         # Save user face embedding to MongoDB
#         self.users_collection.update_one(
#             {"username": username},
#             {"$set": user_data},
#             upsert=True
#         )
#         return True

#     def compare_saved_faces(self, u1, u2, threshold=settings.FACE_MATCH_THRESHOLD):
#         """This function compares two faces saved in the database."""
#         # Fetch face embeddings from the database
#         user1 = self.users_collection.find_one({"username": u1})
#         user2 = self.users_collection.find_one({"username": u2})

#         if not user1 or "face_embedding" not in user1:
#             return False
#         if not user2 or "face_embedding" not in user2:
#             return False

#         embedding1 = np.array(user1["face_embedding"])
#         embedding2 = np.array(user2["face_embedding"])

#         # Compare embeddings using cosine similarity
#         similarity = cosine_similarity([embedding1], [embedding2])[0][0]
#         return similarity >= threshold

#     def verify_face_from_image(self, image_bytes: bytes, username: str):
#         """This function verifies the face embedding from an uploaded image."""
#         img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
#         if img is None:
#             return False

#         # Extract the face embedding from the uploaded image
#         new_embedding = self.extract_face_embedding(img)
#         if new_embedding is None:
#             return False

#         # Fetch the stored embedding for the user from the database
#         user = self.users_collection.find_one({"username": username})
#         if not user or "face_embedding" not in user:
#             return False

#         # Compare the uploaded face embedding with the stored embedding
#         stored_embedding = np.array(user["face_embedding"])
#         similarity = cosine_similarity([new_embedding], [stored_embedding])[0][0]

#         return similarity >= settings.FACE_MATCH_THRESHOLD

#     def extract_face_embedding(self, face_img):
#         """This function extracts the face embedding from the face image."""
#         # Convert face image to a feature vector (embedding)
#         kp, des = self.sift.detectAndCompute(face_img, None)
#         if des is None:
#             return None
#         return des.flatten()  # Return flattened embedding as a placeholder


# # Example usage:
# face_matcher = SimpleFaceMatcher()

# # Save face embedding to DB for a user
# # Assuming `image` is a loaded image and `username` is provided
# # face_matcher.save_face(image, "some_user")

# # Verify face embedding with an uploaded image
# # Assuming `image_bytes` contains the uploaded image data
# # result = face_matcher.verify_face_from_image(image_bytes, "some_user")
# # print(f"Face match result: {result}")

# import os
# import cv2
# import numpy as np
# from datetime import datetime
# from ..config import settings
# from sklearn.metrics.pairwise import cosine_similarity
# from ..utils.db import users_collection
# from motor.motor_asyncio import AsyncIOMotorClient  # Use motor for async MongoDB access

# class SimpleFaceMatcher:
#     def __init__(self, save_dir=settings.FACE_SAVE_DIR):
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         self.save_dir = save_dir
#         self.sift = cv2.SIFT_create()
#         if not os.path.exists(save_dir):
#             os.makedirs(save_dir)
#         self.flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))

#         # Setup MongoDB Atlas connection
#         # Use the connection string from settings for MongoDB Atlas
#         self.client = AsyncIOMotorClient(settings.MONGODB_URI)  # MongoDB Atlas URI
#         self.db = self.client[settings.DATABASE_NAME]  # Use the database name from settings
#         self.users_collection = self.db["users"]  # Collection name "users"

#     async def save_face(self, image, username):
#         """This function saves the face image in the database."""
#         if isinstance(image, str):
#             image = cv2.imread(image)
#         if image is None:
#             return False
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
#         if not faces.any():
#             return False
#         x, y, w, h = faces[0]
#         face_img = image[max(0, y-20):y+h+20, max(0, x-20):x+w+20]

#         # Extract the face embedding from the image
#         embedding = self.extract_face_embedding(face_img)
#         if embedding is None:
#             return False

#         # Save the embedding in the database instead of the filesystem
#         user_data = {
#             "username": username,
#             "face_embedding": embedding.tolist(),  # Convert numpy array to list for MongoDB storage
#             "timestamp": datetime.now()
#         }

#         # Save user face embedding to MongoDB (with async update_one)
#         await self.users_collection.update_one(
#             {"username": username},
#             {"$set": user_data},
#             upsert=True
#         )
#         return True

#     async def compare_saved_faces(self, u1, u2, threshold=settings.FACE_MATCH_THRESHOLD):
#         """This function compares two faces saved in the database."""
#         # Fetch face embeddings from the database
#         user1 = await self.users_collection.find_one({"username": u1})
#         user2 = await self.users_collection.find_one({"username": u2})

#         if not user1 or "face_embedding" not in user1:
#             return False
#         if not user2 or "face_embedding" not in user2:
#             return False

#         embedding1 = np.array(user1["face_embedding"])
#         embedding2 = np.array(user2["face_embedding"])

#         # Compare embeddings using cosine similarity
#         similarity = cosine_similarity([embedding1], [embedding2])[0][0]
#         return similarity >= threshold

#     async def verify_face_from_image(self, image_bytes: bytes, username: str):
#         """This function verifies the face embedding from an uploaded image."""
#         img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
#         if img is None:
#             return False

#         # Extract the face embedding from the uploaded image
#         new_embedding = self.extract_face_embedding(img)
#         if new_embedding is None:
#             return False

#         # Fetch the stored embedding for the user from the database
#         user = await self.users_collection.find_one({"username": username})
#         if not user or "face_embedding" not in user:
#             return False

#         # Compare the uploaded face embedding with the stored embedding
#         stored_embedding = np.array(user["face_embedding"])
#         similarity = cosine_similarity([new_embedding], [stored_embedding])[0][0]

#         return similarity >= settings.FACE_MATCH_THRESHOLD

#     def extract_face_embedding(self, face_img):
#         """This function extracts the face embedding from the face image."""
#         # Convert face image to a feature vector (embedding)
#         kp, des = self.sift.detectAndCompute(face_img, None)
#         if des is None:
#             return None
#         return des.flatten()  # Return flattened embedding as a placeholder


# # Example usage:
# face_matcher = SimpleFaceMatcher()

# # Save face embedding to DB for a user
# # Assuming `image` is a loaded image and `username` is provided
# # face_matcher.save_face(image, "some_user")

# # Verify face embedding with an uploaded image
# # Assuming `image_bytes` contains the uploaded image data
# # result = face_matcher.verify_face_from_image(image_bytes, "some_user")
# # print(f"Face match result: {result}")

"""
Face recognition service for user authentication.
"""
import os
import cv2
import numpy as np
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from sklearn.metrics.pairwise import cosine_similarity
from ..config import settings

class SimpleFaceMatcher:
    def __init__(self, save_dir=None):
        """
        Initialize the face matcher service.
        
        Args:
            save_dir: Optional directory to save face images (for debugging)
        """
        # Load face cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Haar cascade file not found at {cascade_path}")
            
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Initialize SIFT feature detector
        self.sift = cv2.SIFT_create()
        
        # Initialize FLANN matcher for feature matching
        self.flann = cv2.FlannBasedMatcher(
            dict(algorithm=1, trees=5),  # KDTree parameters
            dict(checks=50)  # Search parameters
        )
        
        # Save directory for debugging (optional)
        self.save_dir = save_dir
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # Connect to MongoDB
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.DATABASE_NAME]
        self.users_collection = self.db["users"]
    
    # async def save_face(self, image, username):
    #     """
    #     Extract face from image and save its embedding to database.
        
    #     Args:
    #         image: OpenCV image or path to image
    #         username: User identifier
            
    #     Returns:
    #         bool: True if face detected and saved, False otherwise
    #     """
    #     # Load image if path provided
    #     if isinstance(image, str):
    #         image = cv2.imread(image)
            
    #     # Check image validity
    #     if image is None:
    #         return False
            
    #     # Convert to grayscale for face detection
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    #     # Detect faces
    #     faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
    #     if len(faces) == 0:
    #         return False
            
    #     # Extract first face with margin
    #     x, y, w, h = faces[0]
    #     face_img = image[
    #         max(0, y-20):min(image.shape[0], y+h+20), 
    #         max(0, x-20):min(image.shape[1], x+w+20)
    #     ]
        
    #     # Extract face embedding
    #     embedding = self.extract_face_embedding(face_img)
    #     if embedding is None:
    #         return False
            
    #     # Save to database
    #     user_data = {
    #         "username": username,
    #         "face_embedding": embedding.tolist(),
    #         "face_updated_at": datetime.utcnow()
    #     }
        
    #     # Update or insert user face data
    #     await self.users_collection.update_one(
    #         {"username": username},
    #         {"$set": user_data},
    #         upsert=True
    #     )
        
    #     return True

    async def save_face(self, image, username):
        """
        Detect face, extract embedding using SIFT, and save to DB.
        Returns:
            (success: bool, embedding: np.ndarray or None)
        """
        if isinstance(image, str):
            image = cv2.imread(image)

        if image is None:
            return False, None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return False, None

        x, y, w, h = faces[0]
        face_img = image[
            max(0, y-20):min(image.shape[0], y+h+20),
            max(0, x-20):min(image.shape[1], x+w+20)
        ]

        embedding = self.extract_face_embedding(face_img)
        if embedding is None:
            return False, None

        user_data = {
            "username": username,
            "face_embedding": embedding.tolist(),
            "face_updated_at": datetime.utcnow()
        }

        await self.users_collection.update_one(
            {"username": username},
            {"$set": user_data},
            upsert=True
        )

        return True, embedding

    
    def extract_face_embedding(self, face_img):
        """
        Extract feature embedding from face image.
        
        Args:
            face_img: Face image
            
        Returns:
            numpy.ndarray: Feature embedding or None if extraction failed
        """
        if face_img is None or face_img.size == 0:
            return None
            
        # Convert to grayscale if needed
        if len(face_img.shape) == 3 and face_img.shape[2] > 1:
            gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        else:
            gray_face = face_img
            
        # Detect keypoints and compute descriptors
        keypoints, descriptors = self.sift.detectAndCompute(gray_face, None)
        
        # Check if features were detected
        if descriptors is None or len(descriptors) == 0:
            return None
            
        # Use mean of descriptors as embedding
        return np.mean(descriptors, axis=0)
    
    async def verify_face_from_image(self, image_bytes, username, threshold=None):
        """
        Verify face in uploaded image against stored embedding.
        
        Args:
            image_bytes: Uploaded image bytes
            username: User to verify against
            threshold: Optional similarity threshold override
            
        Returns:
            bool: True if face verified, False otherwise
        """
        # Use default threshold if not specified
        if threshold is None:
            threshold = settings.FACE_MATCH_THRESHOLD
            
        # Decode image bytes
        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return False
            
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return False
            
        # Extract first face with margin
        x, y, w, h = faces[0]
        face_img = img[
            max(0, y-20):min(img.shape[0], y+h+20), 
            max(0, x-20):min(img.shape[1], x+w+20)
        ]
        
        # Extract face embedding
        new_embedding = self.extract_face_embedding(face_img)
        if new_embedding is None:
            return False
            
        # Fetch stored embedding
        user = await self.users_collection.find_one({"username": username})
        if not user or "face_embedding" not in user:
            return False
            
        # Compare embeddings
        stored_embedding = np.array(user["face_embedding"])
        similarity = cosine_similarity([new_embedding], [stored_embedding])[0][0]
        
        return similarity >= threshold
    
    async def compare_saved_faces(self, username1, username2, threshold=None):
        """
        Compare two stored face embeddings.
        
        Args:
            username1: First user
            username2: Second user
            threshold: Optional similarity threshold override
            
        Returns:
            bool: True if faces match, False otherwise
        """
        # Use default threshold if not specified
        if threshold is None:
            threshold = settings.FACE_MATCH_THRESHOLD
            
        # Fetch users
        user1 = await self.users_collection.find_one({"username": username1})
        user2 = await self.users_collection.find_one({"username": username2})
        
        # Check if users and embeddings exist
        if not user1 or "face_embedding" not in user1:
            return False
        if not user2 or "face_embedding" not in user2:
            return False
            
        # Compare embeddings
        embedding1 = np.array(user1["face_embedding"])
        embedding2 = np.array(user2["face_embedding"])
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        
        return similarity >= threshold