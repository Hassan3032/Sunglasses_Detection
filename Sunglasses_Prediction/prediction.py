from flask import jsonify
from Database import Imgrnd

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


