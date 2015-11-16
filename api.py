__author__ = 'abkhanna'

import web
import Store
import StoreUtils
import uuid
import ast
import json
import requests
import pysolr



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
    '/ask/create', 'AskCreate',
    '/stories/list', 'StoryList',
    '/stories/view', 'HumanMarkStoryList',
    '/stories/create', 'HumanMarkStoryScrapeCreate',
    '/accept/story', 'HumanMarkForward',
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
        print request_input.data
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

        if Store.Member.get(key=phone_number):
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

class StoryList:
    def GET(self):
        # this api endpoint is responsible for tossing back the next 10 stories given a starting point.
        web.header('Content-type', 'application/json')
        request_input = web.input(start=0, count=10)
        start = request_input.start
        count = request_input.count
        solr = pysolr.Solr('http://localhost:8983/solr/survivor_stories/', timeout=10)
        results = solr.search("*:*", **{'start': start, 'rows': count})
        formatted_result_list = []
        for r in results:
            formatted_result_list.append({
                "title": r["title"],
                "url": r["id"],
                "image": r.get("picture", ""),
                "hasImage": False if r.get("picture", "") == "" else True
            })
        return json.dumps(formatted_result_list)


"""
The section that follows will be constrained to have code that displays the checking system
"""
class HumanMarkStoryList:
    def GET(self):
        # page to allow humans to mark the different aggreagted texts as valid or not valid.
        render = web.template.render('templates')
        doc = Store.StoryDraft.dequeue()
        if doc is None:
            return render.stories("", "", "", 0, 0, "")

        url = doc['url']
        title = doc['title']
        image = doc['image']
        emotional_score = doc['emotional_score']
        quality_score = doc['quality_score']
        body = doc['body']
        return render.stories(url, title, image, emotional_score, quality_score, body)

class HumanMarkStoryScrapeCreate:
    def POST(self):
        # api endpoint that allows you to post a story to the draft section.
        web.header('Content-type', 'application/json')
        request_input = web.input(url='', title='', image='', emotional_score=-1, quality_score=-1, body='')
        url = request_input.url
        title = request_input.title
        image = request_input.image
        emotional_score = request_input.emotional_score
        quality_score = request_input.quality_score
        body = request_input.body
        if url == '' or title == '' or image == '' or emotional_score == -1 or quality_score == -1 or body == '':
            return web.badrequest()

        data = {
            "url": url,
            "title": title,
            "image": image,
            "emotional_score": emotional_score,
            "quality_score": quality_score,
            "body": body,
        }
        # we have a good set on our hands, go ahead and store a draft
        Store.StoryDraft.create(data)

class HumanMarkForward:
    def POST(self):
        web.header('Content-type', 'application/json')
        data = web.data()
        requests.post(url="http://" + "localhost:8081" + "/accept/story", data=data)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
