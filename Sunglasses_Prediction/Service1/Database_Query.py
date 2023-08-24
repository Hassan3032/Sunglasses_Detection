from Database import mangofs, Imgrnd

def insert_data(image_new):
    frame_id = mangofs.put(image_new)
    Imgrnd.insert_one({
        'Frame_id': frame_id,
        'Results': None,
        'Mask Picture': None})
    return frame_id

def get_image_mango(frame_id):  
    try:
        result_entry = Imgrnd.find_one({
            'Frame_id': frame_id,
            'Results': None,
            'Mask Picture': None}) 

        if result_entry is None:
            return {'message': 'No image with null results found.'}

        grid_out = mangofs.get(frame_id)
        return grid_out
    
    except Exception as e:
        return {'error': str(e)}

def insert_result1(frame_id, prediction_result):
    Imgrnd.update_one({
        'Frame_id': frame_id,
        'Results': None,
        'Mask Picture': prediction_result
    })
    return frame_id
