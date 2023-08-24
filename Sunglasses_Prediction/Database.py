from gridfs import GridFS
from pymongo import MongoClient

# Replace 'localhost' with your actual MongoDB host if needed
mongo_client = MongoClient("mongodb://localhost:27017/ML.SunglassesDetection")
db = mongo_client.get_database()
mangofs = GridFS(db, collection='Image Frames')
Imgrnd = db['Image Result']
