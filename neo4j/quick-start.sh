# Quick Start

## Docker
# https://neo4j.com/developer/docker-run-neo4j/
# First user / mdp => neo4j / neo4j if not specified in docker cmd line

docker pull neo4j

docker run \
     --publish=7474:7474 --publish=7687:7687 \
     --volume=$HOME/neo4j/data:/data \
     --env NEO4J_AUTH=neo4j/neo \
     neo4j


## Python
# Driver 
pip3 install neo4j
# Library
pip3 install py2neo

