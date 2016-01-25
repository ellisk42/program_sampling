from data import *

import numpy as np
import matplotlib.pyplot as plt
import math







raw_data = sort_data #long1_data

tt = [ [ x[3] for x in a ] for a in raw_data ]
scale = 12840 #55435 # |S|+1, which is the baseline
tt = [ [ (scale if x < 0 else min(x,scale)) for x in a ] for a in tt ]
plt.matshow(np.log(np.array(tt)), cmap=plt.cm.gray)
plt.xlabel('# random projections')
plt.ylabel('alpha - |x_*|')
plt.title('Expected solver invocations')
plt.colorbar()
plt.show()
