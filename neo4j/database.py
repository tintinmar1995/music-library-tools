'''
DOC NEO4J
https://neo4j.com/docs/labs/nsmntx/current/config/
https://neo4j.com/docs/labs/nsmntx/current/importing-ontologies/
'''

from py2neo import Graph
from eyed3 import mp3

from utils import * 

class MusicGraph():
        
    def __init__(self, *args, **kwargs):
        self.graph = Graph(*args, **kwargs)
        self.matcher = NodeMatcher(self.graph)
                
    ########################
    # Database Management
    ######################## 
       
    def save(self):
        pass #TODO : save as RDFS
    
    def load_backup(self):
        # self.graph.run('CALL n10s.rdf.import.fetch("{}","{}");'.format(owl_url, owl_format))
        pass #TODO : load from RDFS
    
    def clear(self):
        res = input("Press yyy to confirm...")
        if res == "yyy" :
            self.graph.run("MATCH (n) DETACH DELETE n")
    
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
    
    def import_musicotek(self, mutek, limit=None):
        allMusics = mutek.music_paths() if limit is None else mutek.music_paths()[:limit]
        for filename in allMusics[:500] :
            try :
                trackinfo = mp3.Mp3AudioFile(filename)

                music_title = trackinfo.tag.title if hasattr(trackinfo.tag, 'title') else filename.split("/")[-1]
                music = self.look_and_create("Song",
                                             path=filename,
                                             title=music_title,
                                             track_num=trackinfo.tag.track_num)

                ## Album info
                album = self.look_and_create("Album",
                                             name=trackinfo.tag.album,
                                             release_date=str(trackinfo.tag.release_date))
                self.graph.create(Relationship(music, "album", album))

                ## Genre
                genre = self.look_and_create("Genre", name=str(trackinfo.tag.genre))
                self.graph.create(Relationship(music, "genre", genre))

                for role in ["artist", "album_artist", "composer"]:
                    for name in parse_artists(getattr(trackinfo.tag, role)):
                        artist = self.look_and_create("Person", name=name)
                        self.graph.create(Relationship(music, role, artist))
            except :
                pass
    
    def reset(self):
        self.clear()
        self.import_ontology()
    
    ########################
    # Node Management
    ########################
    
    def look_and_create(self, *labels, **kwargs):
        end = self.matcher.match(*labels, **kwargs).first()
        if end is None:
            end = Node(*labels, **kwargs)           
        return end
    
    ########################
    # Analyse
    ########################
    
    def length(self):
        return self.graph.run("MATCH (n) RETURN count(*)")
        
    def get_labels(self):
        return self.graph.run("MATCH (n) RETURN distinct labels(n), count(*)")


class Musicotek():
    
    def __init__(self, path):
        self.path = path
        
    def music_paths(self):
        path = self.path
        allFiles = get_list_of_files(path)
        extensions = set([get_extension(p) for p in allFiles])
        extensions_music = {'flac', 'm4a', 'mp3', 'ogg'}
        return [filename for filename in allFiles if get_extension(filename) in extensions_music]