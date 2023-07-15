import mongoengine as me
import datetime

# Model for save/load Prometheus queries

# in questa classe vanno aggiunte le label usate per il filtering nelle queries
class Metric(me.EmbeddedDocument):
	__name__ = me.StringField()
	code = me.StringField()
	handler = me.StringField()
	method = me.StringField()
	group = me.StringField()
	instance = me.StringField()
	job = me.StringField()

class Result(me.EmbeddedDocument):                    
	metric = me.EmbeddedDocumentField(Metric)
	value = me.ListField(me.DecimalField())
	values = me.ListField(me.ListField(me.DecimalField()))		

class Data(me.EmbeddedDocument):
	resultType = me.StringField()
	result = me.ListField(me.EmbeddedDocumentField(Result))

class PrometheusQueriesResult(me.Document):
	query = me.StringField(required=True)
	status = me.StringField(required=True)
	data = me.EmbeddedDocumentField(Data)
	errorType = me.StringField()
	error = me.StringField()
	created_at = me.DateTimeField(default=datetime.datetime.now)

