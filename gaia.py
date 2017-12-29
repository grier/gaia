from localstore import *
from web import app
from scheduler import get_scheduler, read_and_publish
from sensors import *
from kafka import *

from apscheduler.triggers.interval import IntervalTrigger

inside = [
    #OneWireSensor("1", "28-0516a1891dff"),
    #OneWireSensor("2", "28-0516a1b966ff"),
    TempHumidity("sht10", 23, 24),
    DHT22("dht", 27)
]
    
outside = [
    WeatherUnderground("balcony", "pws:KCABERKE86"),
]

stores = [
    LocalStore("data.json"),
    KafkaStore()
]

@app.before_first_request
def init():
    get_scheduler().add_job(
        func=lambda: read_and_publish(outside, stores),
        trigger=IntervalTrigger(minutes=5),
        id='outside',
        name='outside fetcher',
        replace_existing=True)
        
    get_scheduler().add_job(
        func=lambda: read_and_publish(inside, stores),
        trigger=IntervalTrigger(seconds=60),
        id='inside',
        name='inside fetcher',
        replace_existing=True)

if __name__ == "__main__":
    read_and_publish(outside, stores)
    read_and_publish(inside , stores)

    app.run(host="0.0.0.0", port=5000, debug=True)
