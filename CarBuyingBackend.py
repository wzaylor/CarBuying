import cPickle
from os import listdir

def getCarMakes(dir = 'C:\\Projects\\Car_makes'):
    makes = listdir(dir)
    return makes

class getMakeData(object):
    def __init__(self, carMake, dir = 'C:\\Projects\\Car_makes'):
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


if __name__ == '__main__':
    dir = 'C:\\Projects\\Car_makes'
    makes = getCarMakes()

    x = getMakeData(makes[0])