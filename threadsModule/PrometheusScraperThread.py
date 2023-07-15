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

  # funzione che verifica se Prometheus server è attivo
  def isHealth(self):

      boolReturn = False
      uriResponse = None

      # è necessario mettere il protocollo http
      uri = "http://localhost:9090/-/healthy"

      try:
        uriResponse = requests.get(uri)
      except requests.ConnectionError:
        print("Connection Error")  
    
      if uriResponse != None:
        if uriResponse.status_code == 200:
          boolReturn = True

      return boolReturn

  # funzione che verifica se Prometheus server è pronto a ricevere query
  def isReady(self):

      boolReturn = False
      uriResponse = None

      # è necessario mettere il protocollo http
      uri = "http://localhost:9090/-/ready"

      try:
        uriResponse = requests.get(uri)
      except requests.ConnectionError:
        print("Connection Error")  
    
      if uriResponse != None:
        if uriResponse.status_code == 200:
          boolReturn = True

      return boolReturn
  
  # funzione che effettua lo scrape di una query
  def scrape(self, query):

      # è necessario mettere il protocollo http
      # query = "process_virtual_memory_bytes"
      uri = "http://localhost:9090/api/v1/query?query=" + query

      try:
        uriResponse = requests.get(uri)
      except requests.ConnectionError:
        print("Connection Error")  
    
      textResponse = uriResponse.text
      jsonResponse = uriResponse.json()

      return jsonResponse

  # funzione che parserizza i dati restituiti dalla query su Prometheus server e ne crea un Model per MongoDB
  def parseData(self, query, jsonData):

    # costruisco un oggetto PrometheusQueryResult a partire dai dati JSON restituiti dalla HTTP API Query su Prometheus 
    # sia che si tratti di 'Instant queries' o di 'Range queries'
    try:

      # se ci sono errori nella query restituisco il tipo di errore
      if "error" in jsonData:
        queryModel = PrometheusQueriesResult(query = query, status = jsonData['status'], errorType = jsonData['errorType'], error = jsonData['error'])
        return queryModel
      
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
      queryModel = PrometheusQueriesResult(query = query, status = jsonData['status'], data = data)

      return queryModel

    except:
      return 'error' 

  # funzione che salva il Model su un'istanza locale di MongoDB
  def saveDataOnMongoDB(self, query, jsonData):

    query = PrometheusScraperThread.parseData(self, query, jsonData)

    if query != 'error':
      query.save()

  # task del Thread : legge una query dal file queries.txt, ne fa lo scrape e dopo avere creato 
  # e caricato un Model MongoDB lo salva su un'istanza locale di MongoDB.
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
            jsonResponse = PrometheusScraperThread.scrape(self, query)
            PrometheusScraperThread.saveDataOnMongoDB(self, query, jsonResponse)

      time.sleep(60)

      #da commentare
      #break

    #print("This is my first scrape!")
    print("Fine task thread")




















