#################################
#	Coding Standards	#
#################################

You are free to use any of the following programming languages for your submission :
	- Python 3
	- C++
	- C#
	- Java

NOTE : Sloppy, undocumented, or otherwise unreadable code will be penalized for not following good coding standards (as laid out in the grading rubric on the course website) : https://www.eng.auburn.edu/~drt0015/coding.html

#################################
#	Submission Rules	#
#################################

Included in your repository is a script named ”finalize.sh”, which you will use to indicate which version of your code is the one to be graded. When you are ready to submit your final version, run the command ./finalize.sh or ./finalize.sh -language_flag from your local Git directory, then commit and push your code. Running the finalize script without a language flag will cause the script to run an interactive prompt where you may enter your programming language. Alternatively, you can pass a -j flag when running the finalize script to indicate that you are submitting in Java (i.e. ./finalize.sh -j). The flag -j indicates Java, -cpp indicates C++, -cs indicates C#, and -p indicates Python 3. This script also has an interactive prompt where you will enter your Auburn username so the graders can identify you. The finalize script will create a text file, readyToSubmit.txt, that is populated with information in a known format for grading purposes. You may commit and push as much as you want, but your submission will be confirmed as ”final” if ”readyToSubmit.txt” exists and is populated with the text generated by ”finalize.sh” at 10:00pm on the due date. If you do not plan to submit before the deadline, then you should NOT run the ”finalize.sh” script until your final submission is ready. If you accidentally run ”finalize.sh” before you are ready to submit, do not commit or push your repo and delete ”readyToSubmit.txt.” Once your final submission is ready, run ”finalize.sh”, commit and push your code, and do not make any further changes to it

Late submissions will be penalized 5% for the first 24 hour period and an additional 10% for every 24 hour period thereafter.

#################################
#       Compiling & Running	#
#################################

Your final submission must include the script "run.sh" which should compile and run your code.

Your script should run on a standard linux machines with the following commands :
```
./run.sh
```
```
./run.sh optional_config
```
Note that running without a config implies the use of a default configuration file "default.cfg" and NOT the use of hardcoded values in your code.

#################################
# Configuration File Explanation #
#################################

runType: (Required) String that can either be "GA" or "Random". Represents the type of algorithm used.

mu: (Required) Integer that represents the size of the starting population and the population that survives each generation for Pac-Man.\
lambda: (Required) Integer that represents the number of offspring created from mu sized population for Pac-Man. Should be greater than or equal to mu since parents cannot survive to the next generation.\
muGhost: (Required) Integer that represents the size of the starting population and the population that survives each generation for Ghost.\
lambdaGhost: (Required) Integer that represents the number of offspring created from mu sized population for Ghost. Should be greater than or equal to mu since parents cannot survive to the next generation.

pillDensity: (Required) An integer or float containing the percent probability that each blank space will produce a pill. For example, if pillDensity=50, then approximately 50% of blank spaces on the board will be given pills.\
fruitSpawnProb: (Required) An integer or float containing the percent probability that at the start of each turn a fruit will appear. Fruit will only appear if there are open blank spaces and if there are no existing fruit on the map.\
fruitScore: (Required) An integer representing how much the game score will increase given that PacMan eats a fruit.\
timeMult: (Required) An integer representing how many times the area of the map gets multiplied by to represent time.

parentSelect: (Required) String that can either be "Over-Selection" or "Fitness Proportional". Represents the method for selecting parents for Pac-Man.\
survivalSelect: (Required) String that can either be "Truncation" or "k-Tournament". Represents the method for selecting survivors to next generation for Pac-Man.\
survivalTournyK: (Optional) Integer that is only used if survivalSelect is "k-Tournament". It is Required if this is the case. Represents the size of the of k for the tournaments determining survival for Pac-Man.

parentSelectGhost: (Required) String that can either be "Over-Selection" or "Fitness Proportional". Represents the method for selecting parents for Ghost.\
survivalSelectGhost: (Required) String that can either be "Truncation" or "k-Tournament". Represents the method for selecting survivors to next generation for Ghost.\
survivalTournyKGhost: (Optional) Integer that is only used if survivalSelect is "k-Tournament". It is Required if this is the case. Represents the size of the of k for the tournaments determining survival for Ghost.

numOfRuns: (Required) An integer representing the number of times that a single run happens.\
numOfFitnessEvals: (Required) An integer representing the number of fitness evaluations that each run gets.\
givenRandomSeed: (Optional) An integer that, if present, will be used as the random seed. If not present, then time in microseconds gets used instead.

dMax: (Required) Integer representing the maximum depth that a tree can be upon initialization.\
parsimony: (Required) Integer representing the coefficient of the parsimony punishment for Pac-Man.\
parsimonyGhost: (Required) Integer representing the coefficient of the parsimony punishment for Ghost.

overSelectionPercentage: (Optional) If the Over-Selection method is chosen for either Pac-Man or Ghost, then this is actually Required. It is a float (0.0, 1.0) representing the percentage that Over-Select uses.\
nodeThreshold: (Required) Integer representing the number of nodes allowed before parsimony pressure occurs.\
fruitConst: (Required) An integer representing what will be used for map value F instead of a manhattan distance if there is no fruit on the board.

logPath: (Required) A string representing where the log file will be output.\
worldPath: (Required) A string representing where the world file will be output.\
solPath: (Required) A string representing where the solution file for Pac-Man will be output.\
solPathGhost: (Required) A string representing where the solution file for Ghost will be output.
