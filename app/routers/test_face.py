import insightface
from PIL import Image
import numpy as np

# Load the pre-trained model
model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=0)  # Use GPU if available

# Load and process the image
img = np.array(Image.open(io.BytesIO(image_bytes)))
faces = model.get(img)

if faces:
    embedding = faces[0].embedding
else:
    embedding = None
