import cPickle
from os import listdir

def getCarMakes(dir = 'C:\\Projects\\CarBuying\\Car_makes'):
    makes = listdir(dir)
    return makes

def getCarModels(carMake, dir = 'C:\\Projects\\CarBuying\\Car_makes', fileNames = False):
    folder = dir + '\\' + carMake
    models = listdir(folder)
    for i in range(len(models)):
        if fileNames == False:
            models[i] = models[i].split('.')[0]
        else:
            models[i] = dir + '\\' + carMake + '\\' + models[i]
    return models

class getMakeData(object):
    def __init__(self, carMake, dir = 'C:\\Projects\\CarBuying\\Car_makes'):
        self.data = {}
        self.makeFolder = dir + '\\' + carMake
        self.getData()

    def getData(self):
        files = listdir(self.makeFolder)

        for file in files:
            modelName = file.split('.')[0]
            fileName = self.makeFolder + '\\' + file

            with open(fileName, mode = 'r') as openedFile:
                self.data[modelName] = cPickle.load(openedFile)
        return

def _finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            return _finditem(v, key)  #added return statement


if __name__ == '__main__':
    dir = 'C:\\Projects\\Car_makes'
    makes = getCarMakes()

    x = getMakeData('Honda')

    #print _finditem(x.data, 'Civic')