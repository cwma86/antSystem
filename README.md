# antSystem

ant system code for our CS510 project


## Installation

Install python 3.x
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

## Min-max Ant Colony optimization
```bash
./src/MMACO/runTspFile.py --filename TSPData/lin318.tsp
```
## Brute force solution
This solution take a long time and uses a lot of memory. Don't go over 20 nodes
```bash
 ./src/BruteForce/BruteForce.py --filename TSPData/lin20.tsp 
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
