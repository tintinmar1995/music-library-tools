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
        try :
            self.graph.run('CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;')
        except :
            pass # this script can fail if already initiated

        # Fetch ontology and import it
        ## "n10s.ONTO.import" is way better than "n10s.RDF.import" to import ONTOLOGIES
        ## A lot of information in RDF files are used to help Neo4j importing ONTOLOGY
        self.graph.run('CALL n10s.onto.import.fetch("{}","{}");'.format(owl_url, owl_format))
    
    def save(self):
        pass #TODO : save as RDFS
    
    def load_backup(self):
        # self.graph.run('CALL n10s.rdf.import.fetch("{}","{}");'.format(owl_url, owl_format))
        pass #TODO : load from RDFS
    
    def clear(self):
        res = input("Press yyy to confirm...")
        if res == "yyy" :
            self.graph.run("MATCH (n) DETACH DELETE n")