__author__ = 'abkhanna'

from pymongo import MongoClient

def database():
    client = MongoClient()
    db = client.trustnetwork
    return db

class Question:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key),
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().Question.insert_one(doc)

    @staticmethod
    def fetch(askerUrn):
        return database().Question.find({'asker_urn': askerUrn})

    @staticmethod
    def get(key):
        return database().Question.find({'_id': str(key)})[0]

class Reply:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().Reply.insert_one(doc)

    @staticmethod
    def fetch(askerUrn, questionUrn):
        return database().Reply.find({'asker_urn': askerUrn, 'question_urn': questionUrn})

    def get(self):
        pass

class ReplyPromise:
    @staticmethod
    def fetch(targetMember):
        return database().ReplyPromise.find({'target_member': targetMember})

    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().ReplyPromise.insert_one(doc)

class Member:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        # doc.update(key.getKeyParts()), not needed since currently just phone number key
        doc.update(data)
        return database().Member.insert_one(doc)

    def fetch(self):
        pass

    @staticmethod
    def get(key):
        return database().Member.find({'_id': str(key)})[0]

class Contact:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().Contact.insert_one(doc)

    @staticmethod
    def fetch(actorUrn):
        return database().Contact.find({'actor_urn': str(actorUrn)})

    def get(self):
        pass
