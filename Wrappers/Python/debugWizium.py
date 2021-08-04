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
    #PATH = './../../Binaries/Windows/libWizium_x64.dll'
    PATH = './../../Projects/VS2017/x64/Debug/libWizium.dll'
    
DICO_PATH = './../../Dictionaries/test.txt'
#DICO_PATH = 'C:/Users/Filipe Cruz/Documents/assisted_performer/all_prods.dic'

# ============================================================================
def draw (wiz):
    """Draw the grid content, with a very simple formating
        
    wiz     Wizium instance"""
# ============================================================================
    lines = wiz.grid_read ()
    for l in lines:
        print (''.join ([s + '   ' for s in l]))


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

    input("Press Enter to continue...")

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

# Create a Wizium instance
wiz = Wizium (os.path.join (os.getcwd (), PATH))

# Load the dictionary
load_dictionary (wiz, DICO_PATH)

wiz.grid_set_size (3,3)
solve (wiz, max_black=4, heuristic_level=6)

exit ()