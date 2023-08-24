from flask import Flask, render_template, request, jsonify
import requests
from prediction import result_finalizer

app = Flask(__name__)

# Replace these URLs with the appropriate URLs for your services
SERVICE1_URL = 'http://localhost:5001/'

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        image_data = data['image']
        print(image_data)

        try:
            response = requests.post(SERVICE1_URL + "get_image" , json={'image': image_data})
            if response.status_code == 200:
                print("Request successful")
                print("Response:", response.content)
                
                # Extract the frame_id from the response
                frame_id = response.json().get('frame_id')
                
                # Process the frame_id and get the result
                pic_result = result_finalizer(frame_id)
                
                # Return the result
                return jsonify({'result': pic_result})
                
            else:
                print("Request failed with status code:", response.status_code)
                return jsonify({'error': 'Request to Service 1 failed'})

        except Exception as e:
            print("An error occurred:", str(e))
            return jsonify({'error': 'An error occurred during the request to Service 1'})

    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(host='0.0.0.0',port =5000,debug=True)