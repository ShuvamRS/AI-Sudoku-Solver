# Test Agent's performance

## Compile program:
- Clone/download the AI-Sudoku-Solver repository
- cd into the folder and execute the command: make
- This creates a bin folder with compiled product

## Run program: python3 bin/Main.pyc

## Generate custom boards (optional):
Run: python3 board_generator.py \<File Prefix\> \<Number of boards\> \<P\> \<Q\> \<M\>
Where:
	N = the length of one side of the NxN grid, also the number of distinct tokens
	P = the number of rows in each block (Norvig's box is a synonym for block as used here)
	Q = the number of columns in each block
	M = the number of filled-in values at the start

## Run program with token(s):
-  Token order doesn't matter
- The following tokens are valid:
	MRV: Minimum Remaining Value Variable Selector
	MAD: MRV and DEG tie breaker
	LCV: Least Constraining Value Value Selector
	FC: Forward Checking Constraint Propagation
	NOR: Norvig's Sudoku Constraint Propagation
- Examples:
	python3 bin/Main.pyc MRV
	python3 bin/Main.pyc MRV LCV FC path/to/board/files
