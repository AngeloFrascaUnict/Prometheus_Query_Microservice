#entry point dell'applicazione
from applicationModule import create_app
#import threadsModule.prometheus 
from threadsModule.PrometheusScraperThread import PrometheusScraperThread 

app = create_app()

# avvio lo scraper su Prometheus con un thread
thread_scraper = PrometheusScraperThread()
thread_scraper.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0')