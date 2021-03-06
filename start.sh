export KAFKA_HEAP_OPTS=-Xmx512m
cd $HOME/confluent-4.0.0
bin/zookeeper-server-start -daemon etc/kafka/zookeeper.properties
bin/kafka-server-start -daemon etc/kafka/server.properties 

cd $HOME/gaia
python ./gaia.py&

cd $HOME/core
nodejs server.js -p 8080 --listen "0.0.0.0" -a : -w ~/&
