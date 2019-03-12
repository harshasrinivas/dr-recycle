import requests

ACCESS_TOKEN = ''

def send(PSID, text_message, category_list):

	quick_replies = []

	for category in category_list:
		el = {}
		el['content_type'] = 'text'
		el['title'] = category
		el['payload'] = category
		quick_replies.append(el)

	params = {
	  "recipient": {
	    "id": PSID,
	  },
	  "message":{
	    "text": text_message,
	    "quick_replies":quick_replies,
	  }
	}

	URL = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN
	r = requests.post(URL, json=params)
