import os
import base64
import numpy as np
from io import BytesIO
from PIL import Image
from flask import jsonify
from Database import Imgrnd


def convert_image_to_base64(base64_data):
    try:
        decoded_data = base64.b64decode(base64_data.split(',')[1])
        image = Image.open(BytesIO(decoded_data))
        image_new = BytesIO()
        image.save(image_new,format='png')
        image_new.seek(0)
        return image_new
    except Exception as e:
        print("Error decoding base64 data:", e)
        return None
    
def normalize_image(image, target_size=(224, 224)):
    image_rgb = image.convert("RGB")
    image_resized = image_rgb.resize(target_size)
    image_array = np.array(image_resized)
    normalized_image = (image_array - 128.0) / 128.0
    return normalized_image

def get_image(grid_out):
    try:
        image_binary = grid_out.read()
        image = Image.open(BytesIO(image_binary))
        return image
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
def result_finalizer(frame_id):
    try:
        find_result = Imgrnd.find_one({
            'Frame_id': frame_id
        })
        if find_result is None:
            return jsonify({'message': 'Not found.'})
      
        s1_value = find_result.get('Mask Picture', 0)

        # Find the highest value and its corresponding column name
        if s1_value == 0:
            results_value = 'No Sunglasses Detected'
        elif s1_value == 1:
            results_value = 'Sunglasses Detected'
        else:
            results_value = 'null'

        # Update the Results field in the document
        Imgrnd.update_one({'Frame_id': frame_id}, {'$set': {'Results': results_value}})

        return results_value
    
    except Exception as e:
        return jsonify({'error': str(e)})


