import threading
import requests
import json
import time
import os

# import MongoEngine models
from applicationModule.prometheus.models import PrometheusQueriesResult, Data, Result, Metric
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

    # costruisco un oggetto PrometheusQueryResult a partire dai dati JSON restituiti dalla HTTP API Query su Prometheus 
    # sia che si tratti di 'Instant queries' o di 'Range queries'
    try:

      # se ci sono errori nella query restituisco il tipo di errore
      if "error" in jsonData:
        query = PrometheusQueriesResult(status = jsonData['status'], errorType = jsonData['errorType'], error = jsonData['error'])
        return query
      
      resultList = []

      for x in jsonData['data']['result']:

        metricX = {}
        metricX["__name__"] = x['metric']['__name__'] if "__name__" in x['metric'] else ""
        metricX["code"] = x['metric']['code'] if "code" in x['metric'] else ""
        metricX["handler"] = x['metric']['handler'] if "handler" in x['metric'] else ""
        metricX["method"] = x['metric']['method'] if "method" in x['metric'] else ""
        metricX["group"] = x['metric']['group'] if "group" in x['metric'] else ""
        metricX["instance"] = x['metric']['instance'] if "instance" in x['metric'] else ""
        metricX["job"] = x['metric']['job'] if "job" in x['metric'] else ""        

        if jsonData['data']['resultType'] == 'vector':
          valueX = x['value']
          resultVectorItem = {"metric" : metricX, "value" : valueX}
          resultList.append(resultVectorItem)

        elif jsonData['data']['resultType'] == 'matrix':
          valueX = x['values']
          resultMatrixItem = {"metric" : metricX, "values" : valueX}
          resultList.append(resultMatrixItem)

      data = {"resultType" : jsonData['data']['resultType'], "result" : resultList}
      query = PrometheusQueriesResult(status = jsonData['status'], data = data)

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
          if ('#' not in line) and line[0] != '\n' and line[0] != ' ':
            query = line.rstrip('\n')
            print(query)
            jsonResponse = PrometheusScraperThread.scrape(query)
            PrometheusScraperThread.saveDataOnMongoDB(jsonResponse)

      time.sleep(60)

      #da commentare
      #break

    #print("This is my first scrape!")
    print("Fine task thread")




















