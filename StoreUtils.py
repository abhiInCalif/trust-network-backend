__author__ = 'abkhanna'

def createUrn(identifier, uniqueKey):
    return 'urn:tn:' + str(identifier) + ':' + str(uniqueKey)

class QuestionKey:
    def __init__(self, asker_urn, question_urn):
        self.asker_urn = asker_urn
        self.question_urn = question_urn

    def __str__(self):
        return '/' + self.asker_urn + '/' + self.question_urn

    def getKeyParts(self):
        return {'asker_urn': self.asker_urn, 'question_urn': self.question_urn}

class Question:
    @staticmethod
    def createKey(askerUrn, questionUrn):
        return QuestionKey(askerUrn, questionUrn)

class ReplyKey:
    def __init__(self, askerUrn, questionUrn, actorUrn):
        self.asker_urn = askerUrn
        self.question_urn = questionUrn
        self.actor_urn = actorUrn

    def __str__(self):
        return '/' + self.asker_urn + '/' + self.question_urn + '/' + self.actor_urn

    def getKeyParts(self):
        return {'asker_urn': self.asker_urn, 'question_urn': self.question_urn, 'actor_urn': self.actor_urn}

class Reply:
    @staticmethod
    def createKey(askerUrn, questionUrn, actorUrn):
        return ReplyKey(askerUrn, questionUrn, actorUrn)

class ContactKey:
    def __init__(self, actorUrn, memberUrn):
        self.actor_urn = actorUrn
        self.member_urn = memberUrn

    def __str__(self):
        return '/' + self.actor_urn + '/' + self.member_urn

    def getKeyParts(self):
        return {'actor_urn': self.actor_urn, 'member_urn': self.member_urn}

class Contact:
    @staticmethod
    def createKey(actorUrn, memberUrn):
        return ContactKey(actorUrn, memberUrn)

class ReplyPromiseKey:
    def __init__(self, targetMember, questionUrn, askerUrn):
        self.target_member = targetMember
        self.question_urn = questionUrn
        self.asker_urn = askerUrn

    def __str__(self):
        return '/' + self.target_member + '/' + self.asker_urn + '/' + self.question_urn

    def getKeyParts(self):
        return {'target_member': self.target_member, 'question_urn': self.question_urn, 'asker_urn': self.asker_urn}

class ReplyPromise:
    @staticmethod
    def createKey(targetMember, questionUrn, askerUrn):
        return ReplyPromiseKey(targetMember, questionUrn, askerUrn)
