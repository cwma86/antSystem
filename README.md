# antSystem

ant system code for our CS510 project


## Installation

[Install python 3.x](https://wiki.python.org/moin/BeginnersGuide/Download)
[install opencv-python](https://pypi.org/project/opencv-python/)
clone this repo

## Usage

for the help menu

```bash
./src/antSystem.py -h
```

for processing the default file 'TSPData/pcb1173.tsp'
```bash
./src/antSystem.py
```

for providing a different data file 
```bash
./src/antSystem.py --filename <path to file>
```

## MCTS Ant Colony optimization

```bash
./src/Runner/runTspFile.py --filename TSPData/pcb10_test.tsp  --MCTS
```

## Min-Max Ant Colony optimization
This Algorithm was developed as a comparision mechanism for our MCTS ant colony optimization problem

Warning: due to run time complexity, This algorithmn should be limited to solving TSP data sets of about 50 nodes
```bash
./src/Runner/runTspFile.py --filename TSPData/pcb10_test.tsp  --MMAS
```
## Ant Colony optimization
This Algorithm was developed as a comparision mechanism for our MCTS ant colony optimization problem

Warning: due to run time complexity, This algorithmn should be limited to solving TSP data sets of about 50 nodes
```bash
./src/Runner/runTspFile.py --filename TSPData/pcb10_test.tsp  --AntSystem
```
## Brute force solution
A Brute force solution was created to prove optimal solutions and as a comparision agianst AntSystem and MCTSACO

Warning: This solution is both memory and computationally intensive, I would not reccomend running on a TSP data set over 5 nodes.

```bash
 ./src/Runner/runTspFile.py --filename TSPData/pcb10_test.tsp  --Brute
 ```

## testing

To run project unit test run 
```bash
make check
```
or
```bash
	python3 -m unittest discover test/
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
