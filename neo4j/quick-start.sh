# Quick Start

## Docker
# https://neo4j.com/developer/docker-run-neo4j/
# First user / mdp => neo4j / neo4j if not specified in docker cmd line

docker pull neo4j

docker run \
     --name=neo4j-rdf \
     --publish=7474:7474 --publish=7687:7687 \
     --volume=$HOME/neo4j/data:/data \
     --env='NEO4J_AUTH=neo4j/neo' \
     --env='NEO4JLABS_PLUGINS=["n10s"]' \
     neo4j:4.0.7


## Python
# Driver 
pip3 install neo4j
# Libraries
pip3 install py2neo pypher
