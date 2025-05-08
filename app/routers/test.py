import os
import cv2
import numpy as np
from datetime import datetime
from ..config import settings
from sklearn.metrics.pairwise import cosine_similarity
from ..utils.db import users_collection
from motor.motor_asyncio import AsyncIOMotorClient  # Use motor for async MongoDB access
from ..services.face2_test import SimpleFaceMatcher
face_matcher = SimpleFaceMatcher()

test_image = cv2.imread("path_to_test_image.jpg")  # Replace with an actual image path
embedding = face_matcher.extract_face_embedding(test_image)
if embedding is None:
    print("No embedding extracted.")
else:
    print(f"Embedding: {embedding}")
