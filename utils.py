from clarifai.rest import ClarifaiApp
from wit import Wit
import requests
import json

WIT_API_TOKEN = ''
CLARIFAI_API_TOKEN = ''

locations = []
solutions = {}
categories = ['plastics', 'batteries', 'electronics', 'clothes', 'glass', 'makeup', 'aluminum cans', 'paper', 'hazardous waste']
categories_dict = {
    'electronics': ["Recycling E-waste is possible at so many different locations throughout the Bay Area. Check out the following website to find the closest place near you!",
                    "https://www2.calrecycle.ca.gov/Electronics/eRecycle"
    ],

    ##batteries is zip modifiable
    'batteries': ["Each type of battery has to be recycled a certain way. Use the following website or call 1-800-CLEANUP to find the closest recycle center to you",
                  "https://search.earth911.com/?what=Batteries&where=95050&list_filter=all&max_distance=25&family_id=&latitude=&longitude=&country=&province=&city=&sponsor="
    ],

    ##SalvationArmy is zip modifiable, GoodWill is not
    'clothes': ["Clothes are best to be donated for them to be enjoyed by someone else. Find your local GoodWill or SalvationArmy to donate!",
                "http://www.goodwill.org/locator/", "https://www.salvationarmyusa.org/usn/plugins/gdosCenterSearch?start=1"
    ],

    'books': [
        'Almost all public libraries in the Bay Area accept used-book donations as fund-raising tools. Phone or check their Web sites. Find your local library using the following URL',
        "https: // find - your - public - library.dp.la /"
    ],

    'hazardous waste': [
        'Hazardous waste, like batteries, has to be handled very carefully when disposing. The following website by SaveTheBay is a great resource to find the closest center that takes hazardous waste!',
        'https://bit.ly/2NFC57k'
    ],

    'aluminum cans': [
        "Glass, bottles, and cans can be recycled for cash back from CRV! Find a local recycling center:",
        "https://www2.calrecycle.ca.gov/BevContainer/RecyclingCenters/"
    ],

    'glass': [
        "Glass, bottles, and cans can be recycled for cash back from CRV! Find a local recycling center:",
        "https://www2.calrecycle.ca.gov/BevContainer/RecyclingCenters/"

    ],

    'makeup': [
        'Origins, M.A.C. and Aveda offer free recycling if you bring their container back to one of their retail stores.',
        'Alternatively, all makeup can be recycled through TerraCycle. Sign up using https://www.terracycle.com/',
    ],

    'paper': [
        "Paper can be recycled through any generic recycling bin"
    ],

    'plastics': [
        "Great news! Plastics can be recycled through any generic recycling bin!"
    ],
}


def initialize():
    introMessage = introMessage = "Hello! What would you like to recycle today? Please send a picture or pick from the following suggestions:"
    returnString = {'text': introMessage, 'replyOptions': categories}
    return returnString


def user_says_yes():
    replyMessage = "Great! What would you like to search for?"
    returnString = {'text': replyMessage, 'replyOptions': categories}
    return returnString


def user_says_no():
    replyMessage = "Okay, bye! :("
    returnString = {'text': replyMessage, 'replyOptions': categories}
    return returnString


def get_tag_from_text(text):
    client = Wit('Y32LHERSN4FMZCFPYFETBBRMXVRJCCNZ')
    resp = client.message(text)
    if len(resp['entities']) > 0:
        if resp['entities']['item'][0]['confidence'] >= 0.68:
            return ['\n'.join(categories_dict[resp['entities']['item'][0]['value']])]

    return ["We're having trouble identifying what you are trying to recycle."]


def clarify_image(url):
    item_list = {'batteries': 0, 'electronics': 0, 'clothes': 0, 'plastics': 0, 'glass': 0, 'makeup': 0, 'aluminum cans': 0, 'paper': 0, 'hazardous waste': 0}

    # Pywit Initialization
    client = Wit(WIT_API_TOKEN)

    # ClarifaiApp Initialization
    app = ClarifaiApp(api_key=CLARIFAI_API_TOKEN)
    model = app.public_models.general_model

    # Parse response
    response = model.predict_by_url(url=url)
    concepts = response['outputs'][0]['data']['concepts']
    # print(str(concepts))
    for concept in concepts:
        resp = client.message(concept['name'])
        # print(concept['name'], concept['value'])

        # We only consider the value of clarification over 0.9
        if concept['value'] > 0.9 and len(resp['entities']) != 0:
            # print(str(resp))
            for item in item_list:
                # We only consider the value of confidence over 0.75
                if resp['entities']['item'][0]['value'] == item and \
                        resp['entities']['item'][0]['confidence'] > 0.75:
                    item_list[item] += 1

    # Return the highest frequency category
    result = ""
    max_count = 0
    max_value = 0
    for item in item_list.keys():
        if item_list[item] > max_count:
            result = item
            max_value = concept['value']
        # When the max_count is equal and the 'value' is bigger, we replace the result
        elif item_list[item] == max_count:
            for concept in concepts:
                if concept['name'] == item and concept['value'] > max_value:
                    result = item
                    max_value = concept['value']

    # Return type is string. If no matches, return is ""
    if result == "":
        return final_response_handler(listOfAnswers=["We're having trouble identifying what you are trying to recycle."])

    return final_response_handler(listOfAnswers=['\n'.join(categories_dict[result])])


def clarify_image_2(url):
    item_list = {'batteries': 0, 'electronics': 0, 'clothes': 0, 'plastics': 0, 'glass': 0, 'makeup': 0, 'aluminum cans': 0, 'paper': 0,
                 'hazardous waste': 0}

    # Pywit Initialization
    client = Wit(WIT_API_TOKEN)

    # Google API Initialization
    payload = {"requests": [{"features": [{"type": "LABEL_DETECTION"}], "image": {"source": {"imageUri": url}}}]}
    r = requests.post('https://vision.googleapis.com/v1/images:annotate?key=AIzaSyChIiHYrv5zRMN7lc7Xr_hYPbD6Gr_0VXk', json=payload, verify=False)
    response = json.loads(r.text)

    concepts = response["responses"][0]["labelAnnotations"]

    # print(str(concepts))
    for concept in concepts:
        resp = client.get_message(concept['description'])
        # print(concept['description'], concept['score'])

        # We only consider the value of clarification over 0.9
        if concept['score'] > 0.7 and len(resp['outcomes'][0]['entities']) != 0:
            # print(str(resp))
            for item in item_list:
                # We only consider the value of confidence over 0.75
                if resp['outcomes'][0]['entities']['item'][0]['value'] == item and resp['outcomes'][0]['entities']['item'][0]['confidence'] > 0.75:
                    item_list[item] += 1

    # Return the highest frequency category
    result = ""
    max_count = 0
    max_value = 0
    for item in item_list.keys():
        if item_list[item] > max_count:
            result = item
            max_value = concept['score']
        # When the max_count is equal and the 'value' is bigger, we replace the result
        elif item_list[item] == max_count:
            for concept in concepts:
                if concept['description'] == item and concept['score'] > max_value:
                    result = item
                    max_value = concept['score']

    # Return type is string. If no matches, returns ""
    if result == "":
        return final_response_handler(listOfAnswers=["We're having trouble identifying what you are trying to recycle."])

    return final_response_handler(listOfAnswers=['\n'.join(categories_dict[result])])


def process_user_input(userInput):
    if userInput in categories_dict.keys():
        answers = ['\n'.join(categories_dict[userInput])]
    else:
        answers = get_tag_from_text(userInput)

    return final_response_handler(listOfAnswers=answers)


# Last Part of the FlowChart
# Returns the final solutions as a string
# keyword = "batteries"
# listOfAnswers = [{'name': 'XXX', 'address': 'XXX', 'city': 'XXX', 'state': 'XXX', 'postcode': 'XXX', 'phone': 'XXX'}, ...]

def final_response_handler(listOfAnswers):
    response = ""
    categories_list = categories
    
    if listOfAnswers != ["We're having trouble identifying what you are trying to recycle."]:
        response += "Here are some suggested recycling solutions for you:\n\n"
        categories_list = ["Yes", "No"]
    
    i = 1
    for e in listOfAnswers:

        if len(listOfAnswers) > 1:
            response += str(i) + ". "

        if isinstance(e, dict) :
            response += e['name'] + "\n"
            response += e['address'] + "\n"
            response += e['city'] + " " + e['state'] + " "+ e['postcode'] + "\n"
            response += e['phone'] + "\n\n"
        else:
            response += e + "\n\n"
        i += 1

    if "We're having trouble identifying what you are trying to recycle." not in response:
        response += "Would you like to search for something else?"
    else:
        response += "Please try again by sending a picture or using one of the suggestions!"

    return [response, categories_list]
