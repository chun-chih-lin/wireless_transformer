#!/bin/bash



if [[ $1 = "1" ]]
then
    clear
    echo "Restarting the service..."
    ./agent_service_stop.sh
fi

echo "Trying starting the service..."

IS_RUNNING=`redis-cli -h localhost -p 6379 GET AGENT:COLLECT`
if [[ $IS_RUNNING = "Running" ]]
then
    echo "It is already running. Stop first. Abort."
    exit 0
fi

echo "Starting the service..."
# Import default keys into redis db
redis-cli -h localhost -p 6379 SET AGENT:COLLECT Starting

# Start agents.
python3 ./collect_agent.py &

redis-cli -h localhost -p 6379 SET AGENT:COLLECT Running
