"""
module1runner.py 

Project: United States Trip File Generation
Author: A.P. Hill Wyrough
version date: 3.15.14

Purpose: module1runner is a basic three part threading of module1.py. It accepts command line arguments of 
1, 2, or 3 (string) and it invokes one of three functions that creates resident NNModule1 files for all of 
the states within the United States. The states are indexed by FIPS code (which is done alphabetically). 
The expected runtime of all three running simultaneously is approximately 5 - 6 hours on a PC. 

Dependencies: module1.py

Notes: Ensure that the file paths are correct for module1.py. If module1.py is running, this will prove
an efficient execution for the entire 51 state dataset. 

"""

import module1

def runner1():
    allStates = module1.read_states()
    module1.executive(allStates[0][0].decode(), allStates[0][1].decode())
    module1.executive(allStates[1][0].decode(), allStates[1][1].decode())
    module1.executive(allStates[2][0].decode(), allStates[2][1].decode())
    module1.executive(allStates[3][0].decode(), allStates[3][1].decode())
    module1.executive(allStates[4][0].decode(), allStates[4][1].decode())
    module1.executive(allStates[5][0].decode(), allStates[5][1].decode())
    module1.executive(allStates[6][0].decode(), allStates[6][1].decode())
    module1.executive(allStates[7][0].decode(), allStates[7][1].decode())
    module1.executive(allStates[8][0].decode(), allStates[8][1].decode())
    module1.executive(allStates[9][0].decode(), allStates[9][1].decode())
    module1.executive(allStates[10][0].decode(), allStates[10][1].decode())
    module1.executive(allStates[11][0].decode(), allStates[11][1].decode())
    module1.executive(allStates[12][0].decode(), allStates[12][1].decode())
    module1.executive(allStates[13][0].decode(), allStates[13][1].decode())
    module1.executive(allStates[14][0].decode(), allStates[14][1].decode())
    module1.executive(allStates[15][0].decode(), allStates[15][1].decode())
    module1.executive(allStates[16][0].decode(), allStates[16][1].decode())

def runner2():
    allStates = module1.read_states()
    module1.executive(allStates[17][0].decode(), allStates[17][1].decode())
    module1.executive(allStates[18][0].decode(), allStates[18][1].decode())
    module1.executive(allStates[19][0].decode(), allStates[19][1].decode())
    module1.executive(allStates[20][0].decode(), allStates[20][1].decode())
    module1.executive(allStates[21][0].decode(), allStates[21][1].decode())
    module1.executive(allStates[22][0].decode(), allStates[22][1].decode())
    module1.executive(allStates[23][0].decode(), allStates[23][1].decode())
    module1.executive(allStates[24][0].decode(), allStates[24][1].decode())
    module1.executive(allStates[25][0].decode(), allStates[25][1].decode())
    module1.executive(allStates[26][0].decode(), allStates[26][1].decode())
    module1.executive(allStates[27][0].decode(), allStates[27][1].decode())
    module1.executive(allStates[28][0].decode(), allStates[28][1].decode())
    module1.executive(allStates[29][0].decode(), allStates[29][1].decode())
    module1.executive(allStates[30][0].decode(), allStates[30][1].decode())
    module1.executive(allStates[31][0].decode(), allStates[31][1].decode())
    module1.executive(allStates[32][0].decode(), allStates[32][1].decode())
    module1.executive(allStates[33][0].decode(), allStates[33][1].decode())
    
def runner3():
    allStates = module1.read_states()
    module1.executive(allStates[34][0].decode(), allStates[34][1].decode())
    module1.executive(allStates[35][0].decode(), allStates[35][1].decode())
    module1.executive(allStates[36][0].decode(), allStates[36][1].decode())
    module1.executive(allStates[37][0].decode(), allStates[37][1].decode())
    module1.executive(allStates[38][0].decode(), allStates[38][1].decode())
    module1.executive(allStates[39][0].decode(), allStates[39][1].decode())
    module1.executive(allStates[40][0].decode(), allStates[40][1].decode())
    module1.executive(allStates[41][0].decode(), allStates[41][1].decode())
    module1.executive(allStates[42][0].decode(), allStates[42][1].decode())
    module1.executive(allStates[43][0].decode(), allStates[43][1].decode())
    module1.executive(allStates[44][0].decode(), allStates[44][1].decode())
    module1.executive(allStates[45][0].decode(), allStates[45][1].decode())
    module1.executive(allStates[46][0].decode(), allStates[46][1].decode())
    module1.executive(allStates[47][0].decode(), allStates[47][1].decode())
    module1.executive(allStates[48][0].decode(), allStates[48][1].decode())
    module1.executive(allStates[49][0].decode(), allStates[49][1].decode())
    module1.executive(allStates[50][0].decode(), allStates[50][1].decode())
    
import sys
if sys.argv[1] == '1':
    exec('runner1()')
elif sys.argv[1] == '2':
    exec('runner2()')
else:
    exec('runner3()')  
    
#print(runner1.__doc__)