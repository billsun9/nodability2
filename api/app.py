import os
from transformers import pipeline
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from topic_classification_gcp import topic_classify, topic_dict_to_list
from textrank_keyword_extraction import TextRank4Keyword
import numpy as np
import json
import random
from more_itertools import one

# ---
# setup env variable for gcloud api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= r"./keys/networknotetaker-dddcaba2ca84.json"
# ---
def load_topic_classifier():
    global classifier
    classifier = pipeline('sentiment-analysis')

def load_textrank_keyword_extractor():
    global keyword_extractor
    keyword_extractor = TextRank4Keyword()

def generateAdjArr(jsonList):
    #jsonList.sort()
    AdjArr = np.zeros((len(jsonList),len(jsonList)), dtype=int)
    out = {}
    out["nodes"] = []
    out["links"] = []
    for i,json_i in enumerate(jsonList):
        out['nodes'].append({
            'id': i,
            'name': json_i['title'],
            'val': 4,
            'color' : list(np.random.choice(range(256), size=3))
        })
        for j,json_j in enumerate(jsonList):
            i_list = [one(x.keys()) for x in json_i["predictions"]["keywords"]]
            j_list = [one(x.keys()) for x in json_j["predictions"]["keywords"]]
            #print(i_list)
            if i == j:
                AdjArr[i][j] = 0
            else:
                if len(set(i_list).intersection(set(j_list))) > 0:
                    AdjArr[i][j] = 1
                    out['links'].append({
                        'source': i,
                        'target': j,
                    })
                else:
                    AdjArr[i][j] = 0
    #print(AdjArr)
    print(out)
    return out
    
json_list = []
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return ":)"

@app.route('/upload', methods=["GET", "POST"])
def api():
    if request.method == "POST":
        text = request.get_json()["content"]
        title = request.get_json()["title"]

        print('Request received: %s' % (text))
        pred_sentiment = classifier(text)
        keyword_extractor.analyze(
            text, 
            candidate_pos = ['NOUN', 'PROPN'], 
            window_size=4, 
            lower=True
        )
        pred_keywords = keyword_extractor.get_keywords(10)
        pred_topics = topic_dict_to_list(topic_classify(text, verbose=False), 5)
        

        json_out = jsonify({"message": "accessed api",
                        "payload": 234,
                        "title": title,
                        "content": text,
                        "predictions": {
                            "sentiment": pred_sentiment,
                            "keywords": pred_keywords,
                            "pred_topics": pred_topics
                            }
                        })
            
        json_list.append({"message": "accessed api",
                        "payload": 234,
                        "title": title,
                        "content": text,
                        "predictions": {
                            "sentiment": pred_sentiment,
                            "keywords": pred_keywords,
                            "pred_topics": pred_topics
                            }
                        })
        print(json_list)
        #json_arr.write(test)
        generateAdjArr(json_list)
        return json_out
    else:
        return "api running"

@app.route('/api/pull', methods=["GET", "POST"])
def db_pull():
    data = {
      "nodes": [ 
          { 
            "id": "id1",
            "name": "name1",
            "val": 1,
            "url": "google.com"
          },
          { 
            "id": "id2",
            "name": "name2",
            "val": 10,
            "url": "bing.com"
          },
          { 
            "id": "id3",
            "name": "name3",
            "val": 12,
            "url": "chess.com"
          },
          { 
            "id": "id4",
            "name": "name4",
            "val": 4,
            "url": "duckduckgo.org"
          },
      ],
      "links": [
          {
              "source": "id1",
              "target": "id2"
          },
          {
            "source": "id2",
            "target": "id1"
        },
          {
            "source": "id1",
            "target": "id3"
        },
      ]
      }
    if request.method == "POST":
        secretKey = request.get_json()["key"]
        if secretKey == 123:
            return jsonify(data), 200
        else:
            return jsonify({"data": "incorrect secret key"}), 401
    else:
        return "get data from db"

users = {'b@b.com': '123'}

@app.route('/api/topic_classification', methods=["GET", "POST"])
def topic_classification_route():
    if request.method == "POST":
        secretKey, text = request.get_json()["key"], request.get_json()["content"]
        if secretKey == 123:
            pred_topics = topic_dict_to_list(topic_classify(text, verbose=False), 5)
            return jsonify({"data": pred_topics}), 200
        else:
            return jsonify({"data": "incorrect secret key"}), 401
    else:
        return "classify text documents into one of multiple topics!"

@app.route('/login', methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        username, password = request.get_json()["email"], request.get_json()["password"]
        print('querying db: ', username, ":", password)
        try:
            if users[username] == password:
                return jsonify({"data": "logged in"}), 200
            else:
                return jsonify({"data": "LOGIN FAILED!!!! wrong password"}), 401
        except KeyError:
            return jsonify({"data": "LOGIN FAILED!!!! user not found"}), 401
    
    else:
        return "login through a post request"
    
if __name__ == '__main__':
    load_topic_classifier()
    load_textrank_keyword_extractor()
    app.run(debug=False)
