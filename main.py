import flask
import flask_socketio as fsio
from flask import Flask, jsonify
from datetime import datetime


last_messages = list()


app = Flask(__name__)
socketio = fsio.SocketIO(app)


def append_message_to_lasts(message):
    if len(last_messages) == 10:
        last_messages.pop(0)
    last_messages.append(message)


def create_message(text, username):
    time = int(datetime.now().timestamp())

    payload = {
        'message': text,
        'time': time,
        'username': username
    }

    return payload


@app.route('/send', methods=['POST', ])
def send_message_to_socket():
    body = flask.request.json
    if 'message' not in body:
        return jsonify({'error': 'There is no "message" parameter.'})

    payload = create_message(body.get('message'), body.get('username'))

    fsio.emit('message', payload, json=True, namespace='/chat', broadcast=True)
    return '', 200


# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     fsio.join_room(room)
#     fsio.send(f'{username} has entered the room.', room=room)


@socketio.on('join chat', namespace='/chat')
def handle_connect(data):
    payload = create_message(data.get('message'), 'SERVER')

    fsio.emit('message', payload, namespace='/chat', broadcast=True)
    for msg in last_messages:
        fsio.emit('message', msg, namespace='/chat', broadcast=True)


@socketio.on('message', namespace='/chat')
def handle_message(data):
    print(data)
    fsio.emit('message', data, json=True, namespace='/chat', broadcast=True)
    append_message_to_lasts(data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=50005)
