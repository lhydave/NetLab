import os
from os import listdir
from os.path import isfile, join
import numpy as np

for i in range(1,41):
    os.system("rm -rf readme" + str(i) + ".txt")
