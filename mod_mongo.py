import datetime
from pymongo import MongoClient

#mongourl = 'mongodb://localhost:27017'

client = MongoClient("mongodb://localhost", 27017)
coll = client.db.posts_coll

json_posts = [
    {
        "auteur": "flouflou",
        "texte": "Mon premier du mois",
        "tags": ['python', 'mongo'],
        "datetime": datetime.datetime.now()
    },
    {
        "auteur": "flouclair",
        "texte": "Mon deuxieme du mois",
        "tags": ['python', 'mongo'],
        "datetime": datetime.datetime.now()
    },
{
        "auteur": "clairclair",
        "texte": "Mon troisieme post du mois",
        "tags": ['python', 'mongo'],
        "datetime": datetime.datetime.now()
    },
    {
        "auteur": "smith",
        "texte": "Mon quatrieme post du mois",
        "tags": ['python', 'mongo'],
        "datetime": datetime.datetime.now()
    }
]

#coll.delete_many({})

#find data
#post_id = coll.find_one()
post_id = coll.delete_one()

post_id = coll.find_one({"auteur":"flouflou"})

if post_id:
    print('We have already data')
    print(post_id)
else:
    #insert data
    post_id = coll.insert_one(json_posts[0]).inserted_id
    print(f'le 1er post est {post_id}')

#ins
mongo_posts = coll.find()

for post in mongo_posts:
    print(post)


