#Python libraries that we need to import for our bot
import random, os, time
from flask import Flask, request
from pymessenger.bot import Bot

import utils, quickreplies

app = Flask(__name__)

ACCESS_TOKEN = ''
VERIFY_TOKEN = ''

bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
	
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	
	else:
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					#Facebook Messenger ID for user so we know where to send response back to
					recipient_id = message['sender']['id']
					message_read(recipient_id)
					typing_on(recipient_id)
					time.sleep(1)
					
					if message['message'].get('text'):	
						time.sleep(1)
						input_text = message['message'].get('text').lower()
						typing_off(recipient_id)

						if input_text == 'yes':
							response_raw = utils.user_says_yes()
							quickreplies.send(recipient_id, response_raw['text'], response_raw['replyOptions'])

						elif input_text == 'no':
							response_raw = utils.user_says_no()
							quickreplies.send(recipient_id, response_raw['text'], response_raw['replyOptions'])

						elif 'hey' == input_text[:3] or 'hello' == input_text[:5] or 'hi' == input_text[:2]:
							response_raw = utils.initialize()
							quickreplies.send(recipient_id, response_raw['text'], response_raw['replyOptions'])

						else:
							response_raw = utils.process_user_input(input_text)
							quickreplies.send(recipient_id, response_raw[0], response_raw[1])
							# send_message(recipient_id, response_text)
					
					if message['message'].get('attachments'):
						# [{'type': 'image', 'payload': {'url': 'https://scontent.xx.fbcdn.net/...'}}
						send_message(recipient_id, "Please wait while we process your image!")
						typing_on(recipient_id)
						img_object = message['message'].get('attachments')[0]
						img_url = img_object['payload']['url']
						response_raw = utils.clarify_image(img_url)
						typing_off(recipient_id)
						quickreplies.send(recipient_id, response_raw[0], response_raw[1])
						# send_message(recipient_id, response_text)
	return "Message Processed"


def verify_fb_token(token_sent):
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'

def message_read(recipient_id):
	bot.send_action(recipient_id, "mark_seen")
	return "success"

def typing_on(recipient_id):
	bot.send_action(recipient_id, "typing_on")
	return "success"

def typing_off(recipient_id):
	bot.send_action(recipient_id, "typing_off")
	return "success"

def send_message(recipient_id, response):
	bot.send_text_message(recipient_id, response)
	return "success"


if __name__ == "__main__":
	app.run()
