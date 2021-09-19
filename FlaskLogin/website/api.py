from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from .models import Document
from . import db
import json
import numpy as np
from more_itertools import one

from transformers import pipeline
from website.textrank_keyword_extraction import TextRank4Keyword
from .topic_classification_gcp import topic_classify, topic_dict_to_list
from .extractive_summarizer import generate_summary

api = Blueprint('api', __name__)


# classifier = pipeline('sentiment-analysis')
keyword_extractor = TextRank4Keyword()

# generate an adjacency array for graph representation
def generateAdjArr(jsonList):
    #jsonList.sort()
    AdjArr = np.zeros((len(jsonList),len(jsonList)), dtype=int)
    out = {}
    out["nodes"] = []
    out["links"] = []
    for i,json_i in enumerate(jsonList):
        out['nodes'].append({
            'id': json_i['id'],
            'name': json_i['title'],
            'val': 4
        })
        for j,json_j in enumerate(jsonList):
            i_list = json_i["predictions"]["keywords"].split(",")
            j_list = json_j["predictions"]["keywords"].split(",")
            #print(i_list)
            if i == j:
                AdjArr[i][j] = 0
            else:
                if len(set(i_list).intersection(set(j_list))) > 0:
                    AdjArr[i][j] = 1
                    out['links'].append({
                        'source': json_i['id'],
                        'target': json_j['id'],
                    })
                else:
                    AdjArr[i][j] = 0
    #print(AdjArr)
    #print(out)
    return out

@api.route('/pull_all_topics', methods=['POST'])
def pull_all_topics():
    documents = Document.query.all()
    topics = ""
    for document in documents:
        topics = topics + document.topics + ","

    topics = topics[:-1]
    
    topic_list = topics.split(',')
    topic_list = list(set(topic_list))

    return jsonify({
        'topics' : topic_list
    })


@api.route('/pull_all', methods=['POST'])
@cross_origin(supports_credentials=True)
def pull_all():
    documents = Document.query.all()
    json_list = []
    for document in documents:
        json_list.append({
            'id' : document.id,
            'title' : document.title,
            'content' : document.data,
            'date' : document.date,
            'predictions' : {
                # 'sentiment' : document.sentiment,
                'keywords' : document.keywords,
                'topics' : document.topics,
                'summary' : document.summary
            }
        })

    data = generateAdjArr(json_list)
    print(data)

    return jsonify(data)

@api.route('/pull_document', methods=['POST'])
@cross_origin(supports_credentials=True)
def pull_document():
    id = request.get_json()['id']
    document = Document.query.get(id)
    json = {
        'id' : document.id,
        'title' : document.title,
        'content' : document.data,
        'date' : document.date,
        'predictions' : {
            # 'sentiment' : document.sentiment,
            'keywords' : document.keywords,
            'topics' : document.topics,
            'summary' : document.summary
        }
    }
    return jsonify(json)

@api.route('/pull_topic', methods=['POST'])
def pull_topic():
    field = request.get_json()
    topic = field['topic']

    documents = Document.query.filter(Document.topics.like('%' + topic + '%'))
    json_list = []
    for document in documents:
        json_list.append({
            'id' : document.id,
            'title' : document.title,
            'content' : document.data,
            'date' : document.date,
            'predictions' : {
                # 'sentiment' : document.sentiment,
                'keywords' : document.keywords,
                'topics' : document.topics,
                'summary' : document.summary
            }
        })

    data = generateAdjArr(json_list)
    print(data)

    return jsonify(data)



@api.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload():
    if request.method == 'POST':
        fields = request.get_json()
        document = fields['content']
        title = fields['title']

        # may want to change this
        if len(document) < 30:
            # flash('Document is too short!', category='error')
            return jsonify({
                'message':'error'
            })
        else:
            # pred_sentiment = classifier(document)[0]['label']
            keyword_extractor.analyze(
                document, 
                candidate_pos = ['NOUN', 'PROPN'], 
                window_size=4, 
                lower=True
            )

            # user_id = current_user.id
            # placeholder for one account, TODO: fix login issue
            user_id = 1
            
            keywords_list = [list(element.keys())[0] for element in keyword_extractor.get_keywords(10)]
            print('keywords_list:', keywords_list)
            pred_keywords = ",".join(keywords_list)
            pred_topics = ",".join(topic_dict_to_list(topic_classify(document, verbose=False), 5))
            # TODO: implement summarization
            summary = generate_summary(document, top_n=3)
            new_document = Document(title=title, data=document, keywords=pred_keywords, summary=summary,
                                topics=pred_topics, user_id=user_id)

            db.session.add(new_document)
            db.session.commit()
            flash('Document added!', category='success')
            return jsonify({
                'message':'success',
                'user': user_id
            })


@api.route('/delete-document', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_document():
    document = json.loads(request.data)
    documentId = document['documentd']
    document = Document.query.get(documentId)
    if document:
        if document.user_id == current_user.id:
            db.session.delete(document)
            db.session.commit()

    return jsonify({})