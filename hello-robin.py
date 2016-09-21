import requests
from flask import Flask, render_template, jsonify, request
from flask import Response
import os
from base64 import b64encode as encode
import json
import thread
from time import time
from operator import truediv

number = 5
exitFlag = 0
app = Flask(__name__)

replacement = {
	'locoH1': 1,
	'locoH2': 1,
	'locoH3': 1,
    'locoTmpg1': 450,
    'locoTmpg2': 450,
    'locoTmpg3': 450,
    'temp':25,
    'rain':0,
}

port = int(os.getenv("PORT", 64781))


@app.route('/change', methods=['GET', 'POST'])
def ui():
    if request.method == 'GET':
        return render_template('change.html')
    else:
        print replacement
        print "\n"
        input = request.form
        for key in input:
            replacement[key] = input[key]
        print replacement
        print "\n"
        return jsonify({'status': 'success'}), 201


@app.route('/change_no_ui', methods=['POST'])
def change_without_ui():
	input = request.form
	for key in input:
			replacement[key] = input[key]
	return jsonify({'status': 'success'}), 201


def bgJob(self):
        while exitFlag == 0:
            number +=1;
            time.sleep(10)

@app.route('/')
def hello_world():
    headers = {'Authorization': 'Basic ' +encode('robin' + ':' + 'robin')}
    query_string = {'grant_type':'client_credentials'}
    response =requests.get('https://317cffe5-50b1-4e91-b497-948b80d899e4.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token',
    headers=headers, params=query_string)
    token =json.loads(response.text).get('access_token')

    headers = {'Authorization': 'Bearer ' + token, 'Predix-Zone-Id': '4e55e51e-415d-4d18-806a-2b17ac214f5d'}

    querystring = {"query":"{\"start\":\"1h-ago\",\"tags\":[{\"name\":\"test\",\"order\":\"desc\",\"limit\":1}]}"}
    response = requests.request('GET', 'https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/datapoints', headers =headers, params=querystring)

#    return (jsonify(json.loads(response.text)))
    data = json.loads(response.text)
    jsonToPython = json.loads(response.text)
    Raw = jsonToPython[u'tags'][0][u'results'][0][u'values'][0][1]
    loco = Raw.split(';', 2)
    loco1Val = loco[0].split(',',8)
    loco2Val = loco[1].split(',',8)
    loco3Val = loco[2].split(',',8)

    
    loco1Val[0] = loco1Val[0].encode('ascii','ignore')
    loco2Val[0] = loco2Val[0].encode('ascii','ignore')
    loco3Val[0] = loco3Val[0].encode('ascii','ignore')
    for i in range(1,7):
        loco1Val[i] = int(loco1Val[i])
        loco2Val[i] = int(loco2Val[i])
        loco3Val[i] = int(loco3Val[i])



    loco1Val[7] = loco1Val[7].encode('ascii','ignore')
    if(loco1Val[7] == 'GOOD'):
        loco1Val[7] = 1

    loco2Val[7] = loco2Val[7].encode('ascii','ignore')
    if(loco2Val[7] == 'GOOD'):
        loco2Val[7] = 1

    loco3Val[7] = loco3Val[7].encode('ascii','ignore')
    if(loco3Val[7] == 'GOOD;'):
        loco3Val[7] = 1

    c11 = loco1Val[1]
    c21 = loco2Val[1]
    c31 = loco3Val[1]
    c12 = loco1Val[2]
    c22 = loco2Val[2]
    c32 = loco3Val[2]

    
    x1 = False
    x2 = False
    x3 = False
    c13 = False
    c23 = False
    c33 = False
    c16 = False
    c26 = False
    c36 = False
    c17 = False
    c27 = False
    c37 = False

    temp = truediv(c12,c11)
    if temp >= 2.6:
        x1 = True
    
    temp = truediv(c22,c21)
    if temp >= 2.6:
        x2 = True
    temp = truediv(c32,c31)
    if temp >= 2.6:
        x3 = True

    if loco1Val[3] == 8:
        c13 = True
    if loco2Val[3] == 8:
        c23 = True
    if loco3Val[3] == 8:
        c33 = True

    if loco1Val[6] == 0:
        c16 = False
    if loco2Val[6] == 0:
        c26 = False
    if loco3Val[6] == 0:
        c36 = False
    if loco1Val[7] == 1:
        c17 = True
    if loco2Val[7] == 1:
        c27 = True
    if loco3Val[7] == 1:
        c37 = True

    out1 = 0
    out2 = 0
    out3 = 0

    off1 = True
    off2 = True
    off3 = True

    analog1 = True
    analog2 = True
    analog3 = True

    adh = True
    if int(replacement['locoH1']) == 0:
        off1 = False;
    if int(replacement['locoH2']) == 0:
        off2 = False;
    if int(replacement['locoH3']) == 0:
        off3 = False;

    

    if int(replacement['locoTmpg1']) < 450:
        analog1 = False;
    if int(replacement['locoTmpg2']) < 450:
        analog2 = False;
    if int(replacement['locoTmpg3']) < 450:
        analog3 = False;

    if int(replacement['temp']) < 25 and int(replacement['rain']) > 0:
        adh = False;

    if c13 == True and c23 == True and c33 == True:
        if c16 == False and c26 == False and c36 == False:
            if c17 == True and c27 == True and c37 == True:
                if x1 == True and x2 == True and x3 == True:
                    if off1 == True and off2 == True and off3 == True:
                        if analog1 == True and analog2 == True and analog3 == True:
                            if adh == True:
                                out1 = 1
                                out2 = 1
                                out3 = 2
    #2nd loop
    if c13 == True and c23 == True and c33 == True:
        if c16 == False and c26 == False and c36 == False:
            if c17 == True and c27 == True and c37 == True:
                if x1 == True and x2 == False and x3 == True:
                    if off1 == True and off2 == True and off3 == True:
                        if analog1 == True and analog2 == True and analog3 == True:
                            if adh == True:
                                out1 = 1
                                out2 = 2
                                out3 = 1
    #loop3
    if c13 == True and c23 == True and c33 == True:
        if c16 == False and c26 == False and c36 == False:
            if c17 == True and c27 == True and c37 == True:
                if x1 == False and x2 == True and x3 == True:
                    if off1 == True and off2 == True and off3 == True:
                        if analog1 == True and analog2 == True and analog3 == True:
                            if adh == True:
                                out1 = 2
                                out2 = 1
                                out3 = 1

    #loop4
    if c13 == True and c23 == True and c33 == True:
        if c16 == False and c26 == False and c36 == False:
            if c17 == True and c27 == True and c37 == True:
                if x1 == True and x2 == True and x3 == True:
                    if off1 == False and off2 == True and off3 == True:
                        if analog1 == True and analog2 == True and analog3 == True:
                            if adh == True:
                                out1 = 2
                                out2 = 1
                                out3 = 1

    if c13 == True and c23 == True and c33 == True:
        if c16 == False and c26 == False and c36 == False:
            if c17 == True and c27 == True and c37 == True:
                if x1 == True and x2 == True and x3 == True:
                    if off1 == True and off2 == True and off3 == True:
                        if analog1 == False and analog2 == True and analog3 == True:
                            if adh == True:
                                out1 = 2
                                out2 = 1
                                out3 = 1

    if c13 == True and c23 == True and c33 == True:
        if c16 == False and c26 == False and c36 == False:
            if c17 == True and c27 == True and c37 == True:
                    if off1 == True and off2 == True and off3 == True:
                        if analog1 == True and analog2 == True and analog3 == True:
                            if adh == False:
                                out1 = 1
                                out2 = 1
                                out3 = 3

    result = str(out1) + ',' + str(out2) + ',' + str(out3)
    return result




if __name__ == '__main__':
    #thread1 = serverConnectionThread.myThread("Thread1")
    #thread1.start()
    thread.start_new_thread( bgJob, () )
    app.run(host='0.0.0.0', port=port)

    
