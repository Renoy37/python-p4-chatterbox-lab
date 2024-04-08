from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        message_list = []

        for message in messages:
            message_data = {
                'id': message.id,
                'body': message.body
            }
            message_list.append(message_data)

            return jsonify(message_list)

    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify({
            "body": new_message.body,
            "username": new_message.username
        }), 201


  
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if message is None:
        return jsonify({'error': 'Message not found'}), 404

    if request.method == 'PATCH':
        new_message_body = request.json.get('body')
        if new_message_body is None:
            return jsonify({'error': 'Message body not provided'}), 400
                
        message.body = new_message_body
        db.session.commit()
            
        return jsonify({'message': 'Message patched successfully', 'body': message.body}), 200

    if request.method == 'DELETE':
        try:
            db.session.delete(message)
            db.session.commit()
            return jsonify({'message': 'Message deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555)
