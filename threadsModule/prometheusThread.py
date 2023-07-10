
import threading
import requests
import json
import time
import os

from applicationModule.prometheus.models import QueryResultVector, DataVector, ResultVector, Metric
from applicationModule.prometheus.models import QueryResultMatrix, DataMatrix, ResultMatrix

from flask import jsonify

# classe di metodi per effettuare lo scrape dei dati da Prometheus e salvare i dati su MongoDB
class PrometheusScraperThread(threading.Thread):

  def scrape(query):

      # è necessario mettere il protocollo http
      # query = "process_virtual_memory_bytes"
      uri = "http://localhost:9090/api/v1/query?query=" + query

      try:
        uriResponse = requests.get(uri)
      except requests.ConnectionError:
        print("Connection Error")  
    
      textResponse = uriResponse.text
      jsonResponse = uriResponse.json()

      #Jresponse = uResponse.text
      #data = json.loads(Jresponse)

      return jsonResponse

  def parseData(jsonData):

    # costruisco un oggetto QueryResultVector a partire dai dati JSON restituiti dalla HTTP API Query su Prometheus 
    # se si tratta di 'Instant queries' o un oggetto QueryResultMatrix se la query è di tipo 'Range queries'
    try:

      # se ci sono errori nella query restituisco il tipo di errore
      if "error" in jsonData:
        #return jsonData['errorType']
        return 'error'
      
      resultList = []

      for x in jsonData['data']['result']:

        if "group" in x['metric']:
          metricX = {"__name__" : x['metric']['__name__'], "group" : x['metric']['group']
          , "instance" : x['metric']['instance'], "job" : x['metric']['job']}
        else:
          metricX = {"__name__" : x['metric']['__name__'], "instance" : x['metric']['instance']
          , "job" : x['metric']['job']}

        valueX = x['value']
        resultMatrixItem = {"metric" : metricX, "value" : valueX}
        resultList.append(resultMatrixItem)

      if jsonData['data']['resultType'] == 'vector':
        dataVector = {"resultType" : jsonData['data']['resultType'], "result" : resultList}
        query = QueryResultVector(status = jsonData['status'], data = dataVector)

      elif jsonData['data']['resultType'] == 'matrix':
        dataMatrix = {"resultType" : jsonData['data']['resultType'], "result" : resultList}
        query = QueryResultMatrix(status = jsonData['status'], data = dataMatrix)

      return query

    except:
      return 'error' 

  def saveDataOnMongoDB(jsonData):

    query = PrometheusScraperThread.parseData(jsonData)

    if query != 'error':
      query.save()

  def run(self):

    while True:

      # batch di query

      # current directory
      #print(os.getcwd())     
      with open("threadsModule/queries.txt", 'r') as f:
        for line in f:
          if ('#' not in line) and line[0] != '\n':
            query = line
            print(query)
            jsonResponse = PrometheusScraperThread.scrape(query)
            PrometheusScraperThread.saveDataOnMongoDB(jsonResponse)

      time.sleep(5)

      #da commentare
      break

    #print("This is my first scrape!")
    print("Fine task thread")




















