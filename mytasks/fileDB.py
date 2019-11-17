import cPickle as pickle
import json
from tree import deb


## This is a simple flat file storage.
## The input and output is a dictionary
## Expects a json file
class FileDB:
    def __init__(self, fileName):
        self.fileName = fileName;

    # Decode the dict object obtained from json file 
    def str_hook(self, obj):
        if isinstance(obj, dict):
            return {k.encode('utf-8') if isinstance(k, unicode) else k :
                    self.str_hook(v) for k,v in obj.items()}
        else:
            return obj.encode('utf-8') if isinstance(obj, unicode) else obj

    def readAll(self):
        data = {}
        with open(self.fileName, 'rb') as output:
            data = json.loads(output.read(), object_hook=self.str_hook)

        deb('readFromFile: keys are = ' + str(data.keys()))
        if data == {}:
            raise Exception('could not read Json file, or the file was empty!')
        return data

    def writeAll(self, inputDict):
        with open(self.fileName,'wb') as output:
            json.dump(inputDict, output)

