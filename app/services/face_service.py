# """
# Face recognition service.
# """
# from typing import List, Optional
# import numpy as np
# from PIL import Image
# import io
# import face_recognition  # You'll need to install this package

# from ..config import FACE_SIMILARITY_THRESHOLD

# def extract_face_embedding(image_bytes: bytes) -> Optional[List[float]]:
#     """
#     Extract face embedding from image
#     """
#     try:
#         # Convert bytes to image
#         image = face_recognition.load_image_file(io.BytesIO(image_bytes))
        
#         # Find all faces in the image
#         face_locations = face_recognition.face_locations(image)
        
#         # If no face found
#         if not face_locations:
#             return None
            
#         # Get face encoding for the first face found
#         face_encoding = face_recognition.face_encodings(image, face_locations)[0]
        
#         # Convert to list for MongoDB storage
#         return face_encoding.tolist()
#     except Exception as e:
#         print(f"Error extracting face embedding: {e}")
#         return None

# def compare_face_embeddings(stored_embedding: List[float], new_embedding: List[float]) -> float:
#     """
#     Compare face embeddings and return similarity score (0 to 1)
#     Higher value means more similar
#     """
#     if not stored_embedding or not new_embedding:
#         return 0.0
        
#     # Convert to numpy arrays
#     stored = np.array(stored_embedding)
#     new = np.array(new_embedding)
    
#     # Calculate face distance (lower means more similar)
#     face_distance = face_recognition.face_distance([stored], new)[0]
    
#     # Convert distance to similarity score (0 to 1)
#     similarity = 1.0 - face_distance
    
#     return float(similarity)

# def verify_face(stored_embedding: List[float], new_embedding: List[float]) -> bool:
#     """
#     Verify if face matches stored embedding
#     """
#     similarity = compare_face_embeddings(stored_embedding, new_embedding)
#     return similarity >= FACE_SIMILARITY_THRESHOLD

from typing import List, Optional
import numpy as np
from PIL import Image
import io
from deepface import DeepFace
import cv2
import tempfile

from ..config import settings

def extract_face_embedding(image_bytes: bytes) -> Optional[List[float]]:
    """
    Extract face embedding using DeepFace (Facenet backend)
    """
    try:
        # Convert bytes to image and save temporarily
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)[:, :, ::-1]  # Convert RGB to BGR for OpenCV

        # DeepFace needs a path or OpenCV image
        embeddings = DeepFace.represent(img_path=image_np, model_name='Facenet', enforce_detection=True)
        
        if embeddings and isinstance(embeddings, list):
            return embeddings[0]["embedding"]  # 128-dim Facenet embedding
        return None
    except Exception as e:
        print(f"Error extracting face embedding: {e}")
        return None

def compare_face_embeddings(stored_embedding: List[float], new_embedding: List[float]) -> float:
    """
    Compare embeddings using cosine similarity (used by DeepFace)
    """
    if not stored_embedding or not new_embedding:
        return 0.0

    stored = np.array(stored_embedding)
    new = np.array(new_embedding)

    # Normalize
    stored /= np.linalg.norm(stored)
    new /= np.linalg.norm(new)

    similarity = np.dot(stored, new)  # Cosine similarity
    return float(similarity)

def verify_face(stored_embedding: List[float], new_embedding: List[float]) -> bool:
    """
    Verify if face matches stored embedding
    """
    similarity = compare_face_embeddings(stored_embedding, new_embedding)
    return similarity >= settings.FACE_RECOGNITION_THRESHOLD
