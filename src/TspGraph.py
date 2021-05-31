import logging
import os
import sys

from Environment import Environment
from FoodSource import FoodSource
from MetricsTracker import MetricsTracker
from Underling import Underling

class TspGraph:
    def __init__(self, filename, workerAntCount = None):
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
                try:
                    self.foodSources.append(FoodSource(currentLine))
                except ValueError:
                    logging.error(f"Unable to parse line: {currentLine}, expected { self.dimension - count + 1} lines")
                    sys.exit(1)
                currentLine = file.readline()
                count = count + 1

        # metricsTracker = MetricsTracker()
        # cycleCount = 1
        # for i in range(cycleCount):
        #     environment = Environment(self.foodSources, workerAntCount)
        #     environment.explore()
        #     metricsTracker.addCycle(i,environment.bestAnt.get_ant_trail_total_length())

        # metricsTracker.getReport()

        environment = Environment(self.foodSources, workerAntCount)
        environment.explore()

        underling = Underling(environment)
        underling.execute_mcts()

        # Write the vertices to log file
        if logging.root.level  >= logging.DEBUG:
            self.foodSources_toFile()

        logging.debug(self.header_toString())
        logging.info('finished')

    @classmethod
    def _validate(cls, *args, **kwargs):
        try:
            hasFilenameArgument = False
            for argument in kwargs.keys():
                if argument == 'filename':
                    hasFilenameArgument = True
                    break
            assert hasFilenameArgument
            assert not args
            assert os.path.isfile(kwargs['filename'])
        except AssertionError:
            logging.warning(f"Filename argument not present")
            return False

        try:
            assert not args
            assert os.path.isfile(kwargs['filename'])
        except AssertionError:
            logging.warning(f"invalid file path {kwargs['filename']} - failed to construct")
            return False

        try:
            isAllValidArguments = True
            validArguments = ['filename', 'v', 'verbose', 'a', 'workerAntCount']
            for argument in kwargs.keys():
                try:
                    validArguments.index(argument)
                except ValueError:
                    isAllValidArguments = False
            assert isAllValidArguments
        except AssertionError:
            logging.warning(f"invalid arguments present: {kwargs.keys()}")
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
