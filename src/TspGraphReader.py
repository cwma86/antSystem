import logging
import os

from Environment import Environment

class TspGraphReader:
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

            count = 0
            # Starting on the first graph vertex. Grab all the vertices
            while 'EOF' not in currentLine and count <= self.dimension:
                foodData = [i.strip() for i in currentLine.split(' ')]

                # TODO we should create a class for food sources so that 
                #      the values each of these represent is more clear
                try:
                    self.foodSources.append((int(foodData[0]), 
                                            float(foodData[1]), 
                                            float(foodData[2])))
                except ValueError:
                    logging.warning(f"Unable to parse line: {currentLine}")
                    return
                currentLine = file.readline()
                count = count + 1
        environment = Environment(self.foodSources)
        trails = environment.explore()

        sortedTrails = sorted(trails.values())
        print(sortedTrails)

        # Print out the vertices
        self.print_foodSources()

        self.print_header()
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

    def print_header(self):
        logging.debug(f"graphName: {self.graphName}")
        logging.debug(f"graphType: {self.graphType}")
        logging.debug(f"graphComment: {self.graphComment}")
        logging.debug(f"edgeType: {self.edgeType}")
        logging.debug(f"dimension: {self.dimension}")

    def print_foodSources(self, index=-1):
        if logging.root.level  >= logging.DEBUG:
            # Print all
            if index == -1:
                for food in self.foodSources:
                    logging.debug(f"food: {food}")
            else:
                try:
                    logging.debug(f"food{index}: {self.foodSources[index]}")
                except ValueError:
                    logging.warning("Invalid index: {index}")

