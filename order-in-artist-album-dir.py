from eyed3 import mp3
import os
path = os.getcwd()
for music_file in os.listdir(path) :
    cursor = "{}/{}".format(path, music_file)
    if music_file[-4:] == ".mp3" : 
        trackinfo = mp3.Mp3AudioFile(cursor)
        dir_album = "{}/{} - {}".format(path, trackinfo.tag.artist, trackinfo.tag.album)
        # ensure album dir exists
        if not os.path.isdir(dir_album) :
            os.mkdir(dir_album)
        os.rename(path+"/"+music_file, dir_album+"/"+music_file)
