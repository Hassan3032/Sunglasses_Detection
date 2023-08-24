import numpy as np
from flask import Flask, request, jsonify,render_template
from prediction import convert_image_to_base64,get_image,normalize_image
from Database_Query import insert_data,get_image_mango,insert_result1
from keras.models import load_model
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

model_path1 = "/Service1/mask_detector.h5"

model1 = load_model(model_path1)

def predict_image(image_data):
    try:

        image_new = convert_image_to_base64(image_data)        
        frame_id = insert_data(image_new)
        image_ds = get_image_mango(frame_id)
        get_db_image = get_image(image_ds)
        normalized_image = normalize_image(get_db_image)

        input_data = np.expand_dims(normalized_image, axis=0)
        try:
            prediction = model1.predict(input_data)
            frame_id = insert_result1(frame_id, prediction)
            return frame_id
        except Exception as e:
            print("Error predicting:", e)
            return None
    
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_image', methods=['POST'])
def get_image_route():
    try:
        data = request.get_json()
        image_data = data['image']
        frame_id = predict_image(image_data)
        return {'frame_id': frame_id}
    
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)