# Prometheus_Query_Microservice

Il progetto è realizzato in linguaggio Python adoperando il framework Flask.
Si tratta di un microservizio che espone sulla rete un set di endpoint che
forniscono come servizio dati estrapolati da un software di monitoring delle 
risorse di sistema locali, il sofware Prometheus.

Il progetto si è detto, è realizzato impiegando Flask e, la struttura è
realizzata sfruttando il pattern "Application Factory".


# Sintesi per una corretta esecuzione del Microservizio su Docker :

	. rinominare .env.prod in .env
	. aggiornare  il setting MONGODB_SETTINGS la classe ProdConf  in config.py con le proprietà di una 	connessione locale di MongoDB
	. dockerizzare usando il file docker-compose.yml : docker-compose build e docker-compose up
	. testare per esempio la GET http://127.0.0.1:5000/prometheus/api/users/ , per aggiungere dati usare la POST 	http://127.0.0.1:5000/prometheus/api/users/create passando un firstname e un lastname usando Postman.