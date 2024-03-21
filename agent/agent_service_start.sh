#!/bin/bash
# Import default keys into redis db
redis-cli -h localhost -p 6379 SET AGENT:COLLECT Starting

# Start agents.
python3 ./collect_agent.py &

redis-cli -h localhost -p 6379 SET AGENT:COLLECT Running