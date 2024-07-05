from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.orm import Session
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)

migrate = Migrate(app, db)


CORS(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        return make_response(jsonify([message.to_dict() for message in messages]), 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE', 'GET'])
def messages_by_id(id):
    with Session(db.engine) as session:
        message = session.get(Message, id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404

        if request.method == 'PATCH':
            data = request.get_json()
            if 'body' in data:
                message.body = data['body']
            if 'username' in data:
                message.username = data['username']
            session.add(message)
            session.commit()
            return make_response(jsonify(message.to_dict()), 200)

        elif request.method == 'DELETE':
            session.delete(message)
            session.commit()
            return make_response(jsonify({'deleted': True}), 200)

        elif request.method == 'GET':
            return jsonify(message.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)