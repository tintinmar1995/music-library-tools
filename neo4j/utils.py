import os

get_extension = lambda filename : filename.split('.')[-1]

def get_list_of_files(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)        
    return allFiles

def parse_artists(label):
    for sep in [" feat. ", " ft. ", " ft ", " feat "]:
        label = ";".join(label.split(sep))
    return label.split(";")