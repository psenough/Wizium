# ############################################################################	

__license__ = \
	"""This file is part of the Wizium distribution (https://github.com/jsgonsette/Wizium).
	Copyright (c) 2019 Jean-Sebastien Gonsette.

	This program is free software : you can redistribute it and / or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, version 3.

	This program is distributed in the hope that it will be useful, but
	WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU
	General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.If not, see <http://www.gnu.org/licenses/>."""

__author__ = "Jean-Sebatien Gonsette"
__email__ = "jeansebastien.gonsette@gmail.com"

# ############################################################################	

import os
import re
import platform
import random
import time
from libWizium import Wizium

# ############################################################################	

# Update those paths if needed !
if platform.system()=='Linux':
    PATH = './../../Binaries/Linux/libWizium.so'
else:
    PATH = './../../Binaries/Windows/libWizium_x64.dll'

#DICO_PATH = './../../Dictionaries/Fr_Simple.txt'
DICO_PATH = 'C:/Users/Filipe Cruz/Downloads/pouetdatadump-prods-20210421.json/all_outline_prods.dic'

# ============================================================================
def draw (wiz):
    """Draw the grid content, with a very simple formating
        
    wiz     Wizium instance"""
# ============================================================================
    lines = wiz.grid_read ()
    for l in lines:
        print (''.join ([s + '   ' for s in l]))


# ============================================================================
def set_grid_1 (wiz):
    """Set the grid skeleton with a pattern of black boxes
        
    wiz     Wizium instance"""
# ============================================================================

    tx = [0, 2, 3]

    wiz.grid_set_size (11,11)
    wiz.grid_set_box (5, 5, 'BLACK')

    for i in range (3):
        wiz.grid_set_box (tx [i], 5-tx [i], 'BLACK')
        wiz.grid_set_box (5+tx [i], tx [i], 'BLACK')
        wiz.grid_set_box (10-tx [i], 5+tx [i], 'BLACK')
        wiz.grid_set_box (5-tx [i], 10-tx [i], 'BLACK')

    wiz.grid_set_box (5, 1, 'BLACK')
    wiz.grid_set_box (5, 9, 'BLACK')


# ============================================================================
def set_grid_2 (wiz):
    """Set the grid as a rectangular area with a hole at the center
    
    wiz     Wizium instance"""
# ============================================================================

    # Grid size
    wiz.grid_set_size (17,15)

    # Hole
    for i in range (5):
        for j in range (5):
            wiz.grid_set_box (6+i, 5+j, 'VOID')

    # Place some words on the grid
    wiz.grid_write (0,0, 'CONSTRAINT', 'H', add_block=True)
    wiz.grid_write (16,5, 'CONSTRAINT', 'V', add_block=True)
    wiz.grid_set_box (16, 4, 'BLACK')


# ============================================================================
def load_dictionary (wiz, dico_path):
    """Load the dictionary content from a file
        
    wiz         Wizium instance
    dico_path   Path to the dictionary to load
    """
# ============================================================================

    # Read file content
    with open (dico_path, 'r') as f:
        words = f.readlines ()

    # Remove what is not a letter, if any
    words = [re.sub('[^a-zA-Z0-9]+', '', s) for s in words]
  
    # Load dictionary
    wiz.dic_clear ()
    n = wiz.dic_add_entries (words)

    print ("Number of words: ")
    print (" - in file: ", len (words))
    print (" - added: ", n)
    print (" - final: ", wiz.dic_gen_num_words ())


# ============================================================================
def solve (wiz, max_black=0, heuristic_level=0, seed=0):
    """Solve the grid
        
    wiz             Wizium instance
    max_black       Max number of black cases to add (0 if not allowed)
    heuristic_level Heuristic level (0 if deactivated)
    seed            Random Number Generator seed (0: take at random)
    """
# ============================================================================

    if not seed: seed = random.randint(1, 1000000)

    # Configure the solver
    wiz.solver_start (seed=seed, black_mode='ANY', max_black=max_black, heuristic_level=heuristic_level)
    tstart = time.time ()
    
    # Solve with steps of 500ms max, in order to draw the grid content evolution
    while True:
        status = wiz.solver_step (max_time_ms=500)

        draw (wiz)
        print (status)

        if status.fillRate == 100: 
            print ("SUCCESS !")
            break
        if status.fillRate == 0: 
            print ("FAILED !")
            #wiz.solver_start (seed=random.randint(1, 1000000), black_mode='ANY', max_black=max_black, heuristic_level=heuristic_level)
            #tstart = time.time ()
            break
    
    # Ensure to release grid content
    wiz.solver_stop ()
    
    tend = time.time ()
    print ("Compute time: {:.01f}s".format (tend-tstart))



# ============================================================================
"""Main"""
# ============================================================================

# -->  C H O O S E  <--
EXAMPLE = 4

# Create a Wizium instance
wiz = Wizium (os.path.join (os.getcwd (), PATH))

# Load the dictionary
load_dictionary (wiz, DICO_PATH)


# Example with fixed pattern
if EXAMPLE == 1:
    set_grid_1 (wiz)
    solve (wiz, max_black=0, heuristic_level=2)

# Example with dynamic black cases placement
elif EXAMPLE == 2:
    set_grid_2 (wiz)
    solve (wiz, max_black=30, heuristic_level=2)

# Perfect 9x9 resolution example (french)
# Need 24e+9 tests in the worst case, which may take ~10hours
elif EXAMPLE == 3:

    wiz.grid_set_size (15,17)

    wiz.grid_set_box (4,  0, 'BLACK')
    wiz.grid_set_box (4,  1, 'BLACK')
    wiz.grid_set_box (10, 1, 'BLACK')
    wiz.grid_set_box (11, 1, 'BLACK')
    wiz.grid_set_box (12, 1, 'BLACK')
    wiz.grid_set_box (13, 1, 'BLACK')
    wiz.grid_set_box (9,  2, 'BLACK')
    wiz.grid_set_box (10, 2, 'BLACK')
    wiz.grid_set_box (14, 2, 'BLACK')
    wiz.grid_set_box (5,  3, 'BLACK')
    wiz.grid_set_box (6,  3, 'BLACK')
    wiz.grid_set_box (8,  3, 'BLACK')	
    wiz.grid_set_box (9,  3, 'BLACK')
    wiz.grid_set_box (14, 3, 'BLACK')
    wiz.grid_set_box (0,  4, 'BLACK')
    wiz.grid_set_box (1,  4, 'BLACK')
    wiz.grid_set_box (5,  4, 'BLACK')
    wiz.grid_set_box (6,  4, 'BLACK')
    wiz.grid_set_box (8,  4, 'BLACK')	
    wiz.grid_set_box (13, 4, 'BLACK')	
    wiz.grid_set_box (3,  5, 'BLACK')
    wiz.grid_set_box (4,  5, 'BLACK')
    wiz.grid_set_box (7,  5, 'BLACK')
    wiz.grid_set_box (8,  5, 'BLACK')
    wiz.grid_set_box (12, 5, 'BLACK')	
    wiz.grid_set_box (14, 5, 'BLACK')		
    wiz.grid_set_box (3,  6, 'BLACK')
    wiz.grid_set_box (4,  6, 'BLACK')
    wiz.grid_set_box (6,  6, 'BLACK')
    wiz.grid_set_box (7,  6, 'BLACK')
    wiz.grid_set_box (9,  6, 'BLACK')
    wiz.grid_set_box (11, 6, 'BLACK')	
    wiz.grid_set_box (13, 6, 'BLACK')		
    #wiz.grid_set_box (1,  7, 'BLACK')
    #wiz.grid_write (0,7, 'outline2021', 'H', add_block=True)
    #wiz.grid_write (9,7, '2021', 'H', add_block=True)
    wiz.grid_set_box (5,  7, 'BLACK')
    wiz.grid_set_box (6,  7, 'BLACK')
    wiz.grid_set_box (8,  7, 'BLACK')
    wiz.grid_set_box (9,  7, 'BLACK')
    wiz.grid_set_box (10, 7, 'BLACK')
    wiz.grid_set_box (3,  8, 'BLACK')
    wiz.grid_set_box (4,  8, 'BLACK')
    wiz.grid_set_box (5,  8, 'BLACK')
    wiz.grid_set_box (7,  8, 'BLACK')
    wiz.grid_set_box (9,  8, 'BLACK')
    wiz.grid_set_box (11, 8, 'BLACK')	
    wiz.grid_set_box (12, 8, 'BLACK')	
    wiz.grid_set_box (2,  9, 'BLACK')
    wiz.grid_set_box (3,  9, 'BLACK')
    wiz.grid_set_box (6,  9, 'BLACK')
    wiz.grid_set_box (7,  9, 'BLACK')
    wiz.grid_set_box (8,  9, 'BLACK')	
    wiz.grid_set_box (9,  9, 'BLACK')
    wiz.grid_set_box (10, 9, 'BLACK')
    wiz.grid_set_box (11, 9, 'BLACK')	
    wiz.grid_set_box (12, 9, 'BLACK')	
    wiz.grid_set_box (13, 9, 'BLACK')
    wiz.grid_set_box (1,  10, 'BLACK')
    wiz.grid_set_box (2,  10, 'BLACK')
    wiz.grid_set_box (7,  10, 'BLACK')
    wiz.grid_set_box (9,  10, 'BLACK')
    wiz.grid_set_box (10, 10, 'BLACK')
    wiz.grid_set_box (1,  11, 'BLACK')
    wiz.grid_set_box (6,  11, 'BLACK')
    wiz.grid_set_box (8,  11, 'BLACK')
    wiz.grid_set_box (9,  11, 'BLACK')	
    wiz.grid_set_box (11, 11, 'BLACK')
    wiz.grid_set_box (12, 11, 'BLACK')
    wiz.grid_set_box (13, 11, 'BLACK')	
    wiz.grid_set_box (14, 11, 'BLACK')	
    wiz.grid_set_box (1,  12, 'BLACK')
    wiz.grid_set_box (5,  12, 'BLACK')
    wiz.grid_set_box (8,  12, 'BLACK')	
    wiz.grid_set_box (9,  12, 'BLACK')
    wiz.grid_set_box (11, 12, 'BLACK')
    wiz.grid_set_box (12, 12, 'BLACK')
    wiz.grid_set_box (1,  13, 'BLACK')
    wiz.grid_set_box (4,  13, 'BLACK')
    wiz.grid_set_box (6,  13, 'BLACK')	
    wiz.grid_set_box (9,  13, 'BLACK')
    wiz.grid_set_box (11, 13, 'BLACK')
    wiz.grid_set_box (13, 13, 'BLACK')
    wiz.grid_set_box (14, 13, 'BLACK')
    wiz.grid_set_box (2,  14, 'BLACK')
    wiz.grid_set_box (3,  14, 'BLACK')
    wiz.grid_set_box (5,  14, 'BLACK')	
    wiz.grid_set_box (11, 14, 'BLACK')
    wiz.grid_set_box (13, 14, 'BLACK')

    wiz.grid_set_box (0,  16, 'BLACK')
    wiz.grid_write (1, 16, 'outline', 'H', add_block=True)
    wiz.grid_set_box (9,  16, 'BLACK')
    wiz.grid_write (10, 16, '2021', 'H', add_block=True)

    solve (wiz, max_black=16, heuristic_level=2)


elif EXAMPLE == 4:

    wiz.grid_set_size (5,6)

    wiz.grid_set_box (4,  0, 'BLACK')
    #wiz.grid_write (0, 0, '4mat', 'H')

    wiz.grid_set_box (4,  1, 'BLACK')
    #wiz.grid_write (0, 0, 'midi', 'H')
    
    wiz.grid_write (3, 0, 'titan', 'V')
	
    wiz.grid_write (4, 2, 'atd', 'V')

    wiz.grid_write (0, 5, 'rom', 'H')

    wiz.grid_set_box (0,  4, 'BLACK')
    wiz.grid_set_box (1,  4, 'BLACK')
    
    wiz.grid_set_box (3,  5, 'BLACK')
    wiz.grid_set_box (4,  5, 'BLACK')
    wiz.grid_set_box (5,  5, 'BLACK')

    solve (wiz, max_black=5, heuristic_level=2)

exit ()