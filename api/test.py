# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 15:41:44 2021

@author: Bill Sun
"""

import json
from flask import jsonify, Flask
app= Flask(__name__)
@app.route('/')
def index():
    
    tmp = jsonify({'name': 'bill', 'age':18})
    
    print(tmp)
    
    # out = json.loads(tmp)
    # print(out)
    return tmp
if __name__ == '__main__':
    app.run(debug=False)