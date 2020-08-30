'''
DOC NEO4J
https://neo4j.com/docs/labs/nsmntx/current/config/
https://neo4j.com/docs/labs/nsmntx/current/importing-ontologies/
'''

from py2neo import Graph

class MusicGraph():
        
    def __init__(self, *args, **kwargs):
        self.graph = Graph(*args, **kwargs)
        
    def import_ontology(self, owl_url = "http://motools.sourceforge.net/doc/musicontology.rdfs",  owl_format= "RDF/XML"):
        # Init Semantics with default values
        self.graph.run('CALL n10s.graphconfig.init();')

        # Create ontology constraint
        # this script can fail if already initiated
        try :
            self.graph.run('CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;')
        except :
            pass

        # Fetch ontology and import it
        self.graph.run('CALL n10s.rdf.import.fetch("{}","{}");'.format(owl_url, owl_format))
        
    def clear(self):
        self.graph.run("MATCH (n) DETACH DELETE n")