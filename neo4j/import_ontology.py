'''
DOC NEO4J
https://neo4j.com/docs/labs/nsmntx/current/config/
https://neo4j.com/docs/labs/nsmntx/current/importing-ontologies/
'''

from py2neo import Graph

ONTOLOGY_URL = "http://motools.sourceforge.net/doc/musicontology.rdfs"
ONTOLOGY_FORMAT = "RDF/XML"

# Connect to neo4j db
graph = Graph(uri="bolt://localhost:7687", auth=("neo4j", "try"))

# Init Semantics with default values
# TODO : this script can fail if already initiated
graph.run('CALL n10s.graphconfig.init();')

# Create ontology constraint
# TODO : this script can fail if already initiated
graph.run('CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;')

# Fetch ontology and import it
graph.run('CALL n10s.rdf.import.fetch("{}","{}");'.format(ONTOLOGY_URL, ONTOLOGY_FORMAT))