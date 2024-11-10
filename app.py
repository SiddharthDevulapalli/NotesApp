from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.note_app_db
notes_collection = db.notes

@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = []
    for note in notes_collection.find():
        notes.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"]
        })
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    new_note = {
        "title": data['title'],
        "content": data['content']
    }
    result = notes_collection.insert_one(new_note)
    return jsonify({"id": str(result.inserted_id), "message": "Note added successfully!"}), 201

@app.route('/api/notes/<id>', methods=['DELETE'])
def delete_note(id):
    print("test")
    print("checked--------------------",id)
    print(type(id), len(id))
    print(ObjectId(id))
    result = notes_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Note deleted successfully!"}), 200
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route('/api/health-check', methods=['GET'])
def health_check():
    try:
        # Attempt to retrieve a single document from the 'notes' collection
        note = notes_collection.find_one()  # This will be `None` if the collection is empty
        if note is not None:
            return jsonify({"status": "success", "message": "Connected to MongoDB and data found!"}), 200
        else:
            return jsonify({"status": "success", "message": "Connected to MongoDB, but no data in the collection!"}), 200
    except Exception as e:
        # If there is an error, return the error message
        return jsonify({"status": "error", "message": str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True, port=3001)