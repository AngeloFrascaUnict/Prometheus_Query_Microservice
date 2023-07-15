#entry point dell'applicazione
from applicationModule import create_app

#import threadsModule.prometheus 
from threadsModule.PrometheusScraperThread import PrometheusScraperThread 


app = create_app()

# avvio lo scraping dei dati su Prometheus con un thread distinto
# solo se Prometheus server è avviato e pronto a ricevere query
thread_scraper = PrometheusScraperThread()
if thread_scraper.isHealth() and thread_scraper.isReady():
    thread_scraper.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0')