# Test the Agent's performance

## Compile program:
- Clone/download the AI-Sudoku-Solver repository
- cd into the folder and execute the command: make
- This creates a bin folder with compiled product

## Run program:
- python3 bin/Main.pyc

## Generate custom boards (optional):
Run: python3 board_generator.py \<File Prefix\> \<Number of boards\> \<P\> \<Q\> \<M\><br>
Where:<br>
  P = the number of rows in each block<br>
  Q = the number of columns in each block<br>
  M = the number of filled-in values at the start<br>

## Run program with token(s):
-  Token order doesn't matter<br>
- The following tokens are valid:<br>
    MRV: Minimum Remaining Value Variable Selector<br>
    MAD: MRV and DEG tie breaker<br>
    LCV: Least Constraining Value Value Selector<br>
    FC: Forward Checking Constraint Propagation<br>
    NOR: Norvig's Sudoku Constraint Propagation<br>
- Examples:<br>
    python3 bin/Main.pyc MRV<br>
    python3 bin/Main.pyc MRV LCV FC path/to/board/files<br>
