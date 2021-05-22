import logging
import os
import sys

from Environment import Environment

class TspGraph:
    def __init__(self, filename):
        # initialize required vars
        self.graphName='', 
        self.graphComment=''
        self.graphType=''
        self.edgeType='',
        self.dimension=0
        self.foodSources = []
        self.filename = filename

        with open(filename) as file:
            currentLine = ''
            firstLine = ''
            
            # Get TSP header info
            file, currentLine = self.__read_header(file)

            count = 1
            # Starting on the first graph vertex. Grab all the vertices
            while count <= self.dimension:
                foodData = [i.strip() for i in currentLine.split(' ')]

                # TODO we should create a class for food sources so that 
                #      the values each of these represent is more clear
                try:
                    self.foodSources.append((int(foodData[0]), 
                                            float(foodData[1]), 
                                            float(foodData[2])))
                except ValueError:
                    logging.error(f"Unable to parse line: {currentLine}, expected { self.dimension - count + 1} lines")
                    sys.exit(1)
                currentLine = file.readline()
                count = count + 1
        environment = Environment(self.foodSources)
        trails = environment.explore()

        sortedTrails = sorted(trails.values())
        print(sortedTrails)

        # Write the vertices to log file
        if logging.root.level  >= logging.DEBUG:
            self.foodSources_toFile()

        logging.debug(self.header_toString())
        logging.info('finished')

    @classmethod
    def _validate(cls, *args, **kwargs):
        try:
            assert not args
            assert list(kwargs.keys()) == ['filename']
            assert os.path.isfile(kwargs['filename'])
        except AssertionError:
            logging.warning(f"invalid file path {kwargs['filename']} - failed to construct")
            return False
        return True

    def __new__(cls, *args, **kwargs):
        if cls._validate(*args, **kwargs):
            return super().__new__(cls)

    def __read_header(self, file):
        #Get TSP header info
        for i in range(7):
            currentLine = file.readline()
            lineData = [i.strip() for i in currentLine.split(':')]
            logging.debug(lineData)

            if(len(lineData) < 2):
                continue

            lineTitle = lineData[0]
            lineContent = lineData[1]

            if lineTitle == 'NAME':
                self.graphName = lineContent
            elif lineTitle == 'TYPE':
                self.graphType = lineContent
            elif lineTitle == 'COMMENT':
                self.graphComment = lineContent
            elif lineTitle == 'DIMENSION':
                self.dimension = int(lineContent)
            elif lineTitle == 'EDGE_WEIGHT_TYPE':
                self.edgeType = lineContent
        return file, currentLine


    def header_toString(self):
        headerString = (f"graphName: {self.graphName}, ")
        headerString += (f"graphType: {self.graphType}, ")
        headerString += (f"graphComment: {self.graphComment}, ")
        headerString += (f"edgeType: {self.edgeType}, ")
        headerString += (f"dimension: {self.dimension}")
        return headerString
 

    def foodSources_toString(self, index=-1):
        foodSourcesString = ""
        if index == -1:
            for food in self.foodSources:
                foodSourcesString += (f"food: {food}\n")
        else:
            try:
                foodSourcesString += (f"food{index}: {self.foodSources[index]}\n")
            except ValueError:
                logging.warning("Invalid index: {index}")
        return foodSourcesString


    def foodSources_toFile(self):
            # log to file
            logFile = os.path.join(os.getcwd(), "foodSources.txt")
            logging.debug(f"writing food sourcces to log file at: {logFile}")
            with open(logFile, "w") as oFile:
                oFile.write(self.foodSources_toString())
