#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():

    Message.query.delete()
    
    messages = []

    for i in range(20):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()        

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return make_response({"error": "Message not found"}, 404)

    db.session.delete(message)
    db.session.commit()
    return make_response({"message": "Message deleted successfully"}, 200)


if __name__ == '__main__':
    with app.app_context():
        make_messages()
