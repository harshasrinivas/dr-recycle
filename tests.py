import utils

categories = ['plastics', 'batteries', 'electronics', 'clothes', 'glass', 'makeup', 'aluminum cans', 'paper', 'hazardous waste']

def test_initialize():

	response = utils.initialize()
	introMessage = "Hello! What would you like to recycle today? Please send a picture or pick from the following suggestions:"
	assert response == {'text': introMessage, 'replyOptions': categories}


def test_get_tag_from_text():

	response = utils.get_tag_from_text("I need to recycle a can")
	assert response == ['Glass, bottles, and cans can be recycled for cash back from CRV! Find a local recycling center:\nhttps://www2.calrecycle.ca.gov/BevContainer/RecyclingCenters/']


def test_process_user_input():
	response = utils.process_user_input('headphone')
	assert response == ["Here are some suggested recycling solutions for you:\n\nRecycling E-waste is possible at so many different locations throughout the Bay Area. Check out the following website to find the closest place near you!\nhttps://www2.calrecycle.ca.gov/Electronics/eRecycle\n\nWould you like to search for something else?", ['Yes', 'No']]

	response = utils.process_user_input('hasdsadad')
	assert response == ["We're having trouble identifying what you are trying to recycle.\n\nPlease try again by sending a picture or using one of the suggestions!", categories]


def test_clarify_image():

	response = utils.clarify_image('https://ksassets.timeincuk.net/wp/uploads/sites/54/2018/04/P4110002-920x518.jpg')
	assert response == ['Here are some suggested recycling solutions for you:\n\nRecycling E-waste is possible at so many different locations throughout the Bay Area. Check out the following website to find the closest place near you!\nhttps://www2.calrecycle.ca.gov/Electronics/eRecycle\n\nWould you like to search for something else?', ['Yes', 'No']]


def test_final_response_handler():
	response1 = utils.final_response_handler([{'name': 'XXX', 'address': 'XXX', 'city': 'XXX', 'state': 'XXX', 'postcode': 'XXX', 'phone': 'XXX'}, {'name': 'XXX', 'address': 'XXX', 'city': 'XXX', 'state': 'XXX', 'postcode': 'XXX', 'phone': 'XXX'}])
	response2 = utils.final_response_handler([{'name': 'XXX', 'address': 'XXX', 'city': 'XXX', 'state': 'XXX', 'postcode': 'XXX', 'phone': 'XXX'}])

	assert response1 == ['Here are some suggested recycling solutions for you:\n\n1. XXX\nXXX\nXXX XXX XXX\nXXX\n\n2. XXX\nXXX\nXXX XXX XXX\nXXX\n\nWould you like to search for something else?', ['Yes', 'No']]
	assert response2 == ['Here are some suggested recycling solutions for you:\n\nXXX\nXXX\nXXX XXX XXX\nXXX\n\nWould you like to search for something else?', ['Yes', 'No']]


test_initialize()
test_get_tag_from_text()
test_process_user_input()
test_clarify_image()
test_final_response_handler()