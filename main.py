from google.cloud import storage
from helper.predict import predict_json
from helper.firestore import updateData

import io
import numpy as np
import json
from PIL import Image

def detectImage(event, context):  # Change the name of the function
    file_name = event["name"]
    bucket_name = event["bucket"]

    # Client-Initialization
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    file = bucket.get_blob(file_name)
    
    blob = file.download_as_string()
    bytes = io.BytesIO(blob)
    im = Image.open(bytes)

    resize = im.resize((150, 150), 2)
    arrayImage = np.array(resize)
    arrayImage = np.expand_dims(arrayImage, axis=0)
    convertImage = np.vstack([arrayImage])
    jsonImage = json.dumps(convertImage.tolist())
    result = json.loads(jsonImage)

    firePredict = predict_json("quiport", "us-central1", "quiport_predictions", instances=result, version="fire_v1")
    accidentPredict = predict_json("quiport", "us-central1", "quiport_predictions", instances=result, version="accident_v1")

    uid = file.metadata['firebaseStorageDownloadTokens']
    fireDetected = 0
    accidentDetected = 0
    categories = []
    
    if not firePredict[0][0] == False :
        categories.append("Non Fire")
    else:
        categories.append("Fire")
        fireDetected = 1

    if not accidentPredict[0][0] == False :
        categories.append("Non Accident")
    else:
        categories.append("Accident")
        accidentDetected = 1

    updateData(uid, fireDetected, accidentDetected, categories)

    return 'Result Fire: {}, Result Accident: {}'.format(firePredict[0][0], accidentPredict[0][0])