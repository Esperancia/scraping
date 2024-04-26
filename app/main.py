import datetime
import requests

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import OperationFailure

mongoServerUrl = 'mongodb://localhost' # if tested outside container. mongodb://mongo from Docker
mongoServerPort = 27017
urlToScrap = 'https://www.costco.ca/hot-buys.html'

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        startScraping()
        return 'Succès'
    else:
        return render_template('index.html')

def getHotBuyCollection():
    # if mypyapp tested directly outside python container
    clientConnection = MongoClient(mongoServerUrl, mongoServerPort)

    try:
        # Try to validate a collection, if it fails, create collection (see except)
        clientConnection.db.validate_collection("costco_hot_buy")
        hotBuyCollection = clientConnection.db.costco_hot_buy
        # empty collection
        #hotBuyCollection.delete_many({})
    except OperationFailure:
        #print("This collection doesn't exist. create it")
        hotBuyCollection = clientConnection.db.costco_hot_buy

    return hotBuyCollection


def saveItem(coll, item):
    saved_id = coll.insert_one(item).inserted_id
    if not saved_id:
        print('Attention, item non enregistré. A Débugguer!')


def listItems(coll):
    for i in coll.find():
        print(i)


def startScraping():
    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    pageToScrap = requests.get(url=urlToScrap, headers=headers)

    soup = BeautifulSoup(pageToScrap.content, 'html5lib')

    #costcoDeals = []

    productsBlock = soup.find('div', attrs={'class': 'product-list grid'})

    for p in productsBlock.findAll('div', attrs={'class': 'col-xs-6 col-lg-4 col-xl-3 product'}):

        try:
            pInner = p.find('div', attrs={'class': 'product-tile-set'}).find('div', attrs={'class': 'thumbnail'})

            #print(pInner)

            item = {}

            '''
            print(pInner.find('div',
                attrs={'class': 'product-img-holder link-behavior'}).find('a',
                attrs={'class': 'product-image-url'}).find('img'))
            print(pInner.find('div',
                attrs={'class': 'product-img-holder link-behavior'}).find('a',
                attrs={'class': 'product-image-url'}).img)
            '''

            imgNode = pInner.find('div',
                attrs={'class': 'product-img-holder link-behavior'}).find('a',
                attrs={'class': 'product-image-url'}).img

            if imgNode.has_attr('src'):
                item['img'] = pInner.find('div',
                    attrs={'class': 'product-img-holder link-behavior'}).find('a',
                    attrs={'class': 'product-image-url'}).img['src']
            else:
                item['img'] = pInner.find('div',
                                          attrs={'class': 'product-img-holder link-behavior'}).find('a',
                                                attrs={
                                                    'class': 'product-image-url'}).img[
                    'data-src']

            item['url'] = pInner.find('div',
                attrs={'class': 'product-img-holder link-behavior'}).find('a',
                attrs={'class': 'product-image-url'})['href']

            item['prix'] = pInner.find('div', attrs={'class': 'caption link-behavior'}).find('div',
                                              attrs={'class': 'price'}).get_text().strip()

            item['nom'] = pInner.find('div', attrs={'class': 'caption link-behavior'}).find('span',
                                              attrs={'class': 'description'}).find('a').get_text().strip()

            #item['nom'] = pInner.find('div', attrs={'class': 'caption link-behavior'}).span.a.text

            item['date_creation'] = datetime.datetime.now()
            #print(item)

            #costcoDeals.append(item)
            # save in mongodb instead of collecting in array.
            saveItem(getHotBuyCollection(), item)

        except KeyError as e:
            print('insertion echouée. A vérifier: ', e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

