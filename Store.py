__author__ = 'abkhanna'

from pymongo import MongoClient

def database():
    client = MongoClient("mongodb://heroku_pw3tw66l:f6u3bvhehp4es6u4emoo23snol@ds035137.mongolab.com:35137/heroku_pw3tw66l")
    db = client.heroku_pw3tw66l
    return db

class Question:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key),
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().Question.update({'_id': str(key)}, doc, upsert=True)

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
        return database().Reply.update({'_id': str(key)}, doc, upsert=True)

    @staticmethod
    def fetch(askerUrn, questionUrn):
        return database().Reply.find({'asker_urn': askerUrn, 'question_urn': questionUrn})

    @staticmethod
    def get(key):
        cursor_list = list(database().Reply.find({'_id': str(key)}))
        return cursor_list[0] if len(cursor_list) > 0 else {}

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
        return database().ReplyPromise.update({'_id': str(key)}, doc, upsert=True)

class Member:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        # doc.update(key.getKeyParts()), not needed since currently just phone number key
        doc.update(data)
        return database().Member.update({'_id': str(key)}, doc, upsert=True)

    def fetch(self):
        pass

    @staticmethod
    def get(key):
        cursor_list = list(database().Member.find({'_id': str(key)}))
        return cursor_list[0] if len(cursor_list) > 0 else {}

class Contact:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().Contact.update({'_id': str(key)}, doc, upsert=True)

    @staticmethod
    def fetch(actorUrn):
        return database().Contact.find({'actor_urn': str(actorUrn)})

    @staticmethod
    def find(query):
        return list(database().Contact.find(query))

    @staticmethod
    def get(key):
        cursor_list = list(database().Contact.find({'_id': str(key)}))
        return cursor_list[0] if len(cursor_list) > 0 else {}

class StoryDraft:
    @staticmethod
    def create(data):
        doc = {}
        doc.update(data)
        exist_doc = database().StoryDraft.find_one({"url": data.get('url', '')})
        if exist_doc is None:
            return database().StoryDraft.insert_one(doc)
        else:
            print "caught duplicates\n\n"

    @staticmethod
    def dequeue():
        # gets the first entry from the table and deletes it after returning it to the api.
        # think queue.dequeue
        doc = database().StoryDraft.find_one()
        database().StoryDraft.remove(doc)
        return doc
