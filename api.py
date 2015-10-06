__author__ = 'abkhanna'

import web
import Store
import StoreUtils
import uuid
import ast
import json
import requests



urls = (
    '/respond/fetch', 'RespondFetchQuestionsAskedToMe',
    '/respond/fetch/question/detail', 'RespondFetchQuestionDetail',
    '/respond/reply', 'RespondReply',
    '/member/create', 'MemberCreate',
    '/member/login', 'MemberLogin',
    '/member/logout', 'MemberLogout',
    '/contact/list', 'ContactList',
    '/contact/add', 'ContactAdd',
    '/ask/detail', 'AskDetail',
    '/ask/list', 'AskList',
    '/ask/create', 'AskCreate'
)

class AskDetail:
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(askerUrn='', questionUrn='')
        asker_urn = request_input.askerUrn
        question_urn = request_input.questionUrn
        if asker_urn == '' or question_urn == '':
            return web.badrequest()
        question_key = StoreUtils.Question.createKey(askerUrn=asker_urn, questionUrn=question_urn)
        question_data = Store.Question.get(key=question_key)
        reply_data = list(Store.Reply.fetch(askerUrn=asker_urn, questionUrn=question_urn))
        return json.dumps({'question_data': question_data, 'reply_data': reply_data})

class AskList:
    def GET(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(askerUrn='')
        asker_urn = request_input.askerUrn
        if asker_urn == '':
            return web.badrequest()
        return json.dumps(list(Store.Question.fetch(askerUrn=asker_urn)))

class AskCreate:
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(askerUrn='', data={})
        asker_urn = request_input.askerUrn
        data = ast.literal_eval(request_input.data)
        if asker_urn == '' or data == {}:
            return web.badrequest()
        question_urn = StoreUtils.createUrn('question', uuid.uuid1())
        key = StoreUtils.Question.createKey(askerUrn=asker_urn, questionUrn=question_urn)
        result = Store.Question.put(key=key, data=data)
        recipients = Store.Contact.fetch(asker_urn)
        # put a promise into the
        for recipient in recipients:
            recipient_urn = recipient['member_urn']
            key = StoreUtils.ReplyPromise.createKey(targetMember=recipient_urn, questionUrn=question_urn, askerUrn=asker_urn)
            Store.ReplyPromise.put(key=key, data={'question_data': data})

            # once you have created the question, create the notifications as well
            dataForRequest = {
                "recipientUrn": recipient_urn,
                "askerUrn": asker_urn,
                "text": data.get("questionText", ""),
                "urn": question_urn
            }
            requests.post(url="http://" + "trust-network-notifications.herokuapp.com" + "/notification/create", data=dataForRequest)

class RespondFetchQuestionsAskedToMe:
    def GET(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(targetMember='')
        target_member = request_input.targetMember
        if target_member == '':
            return web.badrequest()
        return json.dumps(list(Store.ReplyPromise.fetch(targetMember=target_member)))


class RespondFetchQuestionDetail:
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(askerUrn='', questionUrn='', actorUrn='')
        asker_urn = request_input.askerUrn
        question_urn = request_input.questionUrn
        actor_urn = request_input.actorUrn
        if asker_urn == '' or question_urn == '' or actor_urn == '':
            return web.badrequest()
        key = StoreUtils.Question.createKey(askerUrn=asker_urn, questionUrn=question_urn)
        question_data = Store.Question.get(key=key)
        reply_key = StoreUtils.Reply.createKey(askerUrn=asker_urn, questionUrn=question_urn, actorUrn=actor_urn)
        reply_data = Store.Reply.get(key=reply_key)
        return json.dumps({"question_data": question_data, "reply_data": reply_data})

class RespondReply:
    # actorUrn is the person who posted the reply
    # recipientUrn is the person receiving the reply
    # data is data associated with the reply
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(askerUrn='', data={}, actorUrn='', questionUrn='')
        if request_input.askerUrn == '' or request_input.data == {} or request_input.actorUrn == '' \
                or request_input.questionUrn == '':
            return web.badrequest()
        key = StoreUtils.Reply.createKey(request_input.askerUrn, request_input.questionUrn, request_input.actorUrn)
        Store.Reply.put(key=key, data=ast.literal_eval(request_input.data))

class MemberCreate:
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(phoneNumber='', data={})
        phone_number = request_input.phoneNumber
        data = ast.literal_eval(request_input.data)
        if phone_number == '' or data == {}:
            return web.badrequest()

        if Store.Member.get(key=phone_number).count() > 0:
            return web.badrequest()

        Store.Member.put(key=phone_number, data=data) # true on success, false otherwise.

class MemberLogin:
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(phoneNumber='')
        phone_number = request_input.phoneNumber
        if phone_number == '':
            return web.badrequest()
        return json.dumps(Store.Member.get(key=phone_number))  # returns the memberUrn associated with the phone_number

class MemberLogout:
    def POST(self):
        return

class ContactList:
    def GET(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(actorUrn='')
        actor_urn = request_input.actorUrn
        if actor_urn == '':
            return web.badrequest()
        return json.dumps(list(Store.Contact.fetch(actorUrn=actor_urn)))

class ContactAdd:
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(actorUrn='', memberUrn='', data={})
        actor_urn = request_input.actorUrn
        member_urn = request_input.memberUrn
        data = ast.literal_eval(request_input.data)
        if actor_urn == '' or member_urn == '' or data == {}:
            return web.badrequest()

        key = StoreUtils.Contact.createKey(actorUrn=actor_urn, memberUrn=member_urn)
        Store.Contact.put(key=key, data=data)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
