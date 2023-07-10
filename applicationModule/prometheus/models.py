import mongoengine as me
import datetime

# Model for save/load Prometheus queries
class Metric(me.EmbeddedDocument):
	__name__ = me.StringField()
	group = me.StringField()
	instance = me.StringField()
	job = me.StringField()

class ResultVector(me.EmbeddedDocument):
	metric = me.EmbeddedDocumentField(Metric)
	value = me.ListField(me.DecimalField())

class ResultMatrix(me.EmbeddedDocument):                    
	metric = me.EmbeddedDocumentField(Metric)
	value = me.ListField(me.ListField(me.DecimalField()))		

class ResultVector(me.EmbeddedDocument):
	metric = me.EmbeddedDocumentField(Metric)
	value = me.ListField(me.DecimalField())

class ResultMatrix(me.EmbeddedDocument):                    
	metric = me.EmbeddedDocumentField(Metric)
	value = me.ListField(me.ListField(me.DecimalField()))		

class DataVector(me.EmbeddedDocument):
	resultType = me.StringField()
	result = me.ListField(me.EmbeddedDocumentField(ResultVector))

class DataMatrix(me.EmbeddedDocument):
	resultType = me.StringField()
	result = me.ListField(me.EmbeddedDocumentField(ResultMatrix))




class QueryResultVector(me.Document):
	status = me.StringField(required=True)
	data = me.EmbeddedDocumentField(DataVector)
	errorType = me.StringField()
	error = me.StringField()
	created_at = me.DateTimeField(default=datetime.datetime.utcnow)
	#created_at = me.DateTimeField(default=datetime.datetime.now)

class QueryResultMatrix(me.Document):
	status = me.StringField(required=True)
	data = me.EmbeddedDocumentField(DataMatrix)
	errorType = me.StringField()
	error = me.StringField()
	created_at = me.DateTimeField(default=datetime.datetime.utcnow)
	#created_at = me.DateTimeField(default=datetime.datetime.now)



