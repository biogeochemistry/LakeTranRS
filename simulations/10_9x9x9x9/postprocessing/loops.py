'''This file expects that there are

results_raw2/AT.npy
results_raw2/WS.npy
results_raw2/TP.npy
results_raw2/DOC.npy

and each has the following format

        loopd.iloc[0, :, :] = mdeps  # mixing depth
        loopd.iloc[1, :, :] = t0s    # surface water temperature
        loopd.iloc[2, :, :] = ices   # ice thickness
        loopd.iloc[3, :, :] = o23s   # O2 concentration bottom
        loopd.iloc[4, :, :] = chlps  # chl pool entire lake

with (variable x 365 days x simulations) in array dimensions, and
there are 3 simulations in the following order:

    AT5 WS5 TP5 DOC5 base simulation
    variation A where one of the 4 dimensions has level 1
    variation B where one of the 4 dimensions has level 9

So, there's a lot of hardcoding and fixed numbers.
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os.path
import matplotlib.gridspec as gridspec

sns.set_style('whitegrid')
lw = 1

da = np.zeros((4, 5, 365, 3)) * np.nan
# input dimensions                   PANEL SIDEWAYS
# output variables (DOY based means) PANEL VERTICAL
# DOY                                LOOP DIRECTION
# 3 simulations, see above docstring base against 2 simulations, TWO LOOPS

for ii in range(4):
    fname = os.path.join('results_raw2',
                         ['AT', 'WS', 'TP', 'DOC'][ii] + '.npy')
    da[ii, :, :, :]  = np.load(fname)

gs = gridspec.GridSpec(5, 4)

for ci in range(4):
    col0 = ('blue', 'darkorange',  'darkgreen',  'darkbrown')[ci]
    col1 = ( 'red',       'pink', 'lightgreen', 'lightbrown')[ci]
    dname = ('AT', 'WS', 'TP', 'DOC')[ci]
    for ri in range(5):
        lim0 = (8,  0,   0, 1e0,  1)[ri]
        lim1 = (0, 21, 0.7, 1e4, 50)[ri]
        ax = plt.subplot(gs[ri, ci], aspect='equal')
        d = da[ci, ri, :, :]  # doy x sim
        ax.plot([lim0, lim1], [lim0, lim1], color='lightgray', linewidth=lw)
        ax.plot(d[:, 0], d[:, 1], col=col0, label='high {:s}'.format(dname))
        ax.plot(d[:, 0], d[:, 2], col=col1, label='low {:s}'.format(dname))
        ax.set_xlim([lim0, lim1])
        ax.set_ylim([lim0, lim1])
        if ri == 3: # oxygen
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.axhline(3000, color='lightgray', linewidth=lw)
            ax.axhline(16, color='lightgray', linewidth=lw)
            ax.axvline(3000, color='lightgray', linewidth=lw)
            ax.axvline(16, color='lightgray', linewidth=lw)
        if ri == 4: # chl
            ax.set_xscale('log')
            ax.set_yscale('log')

# legends at the top
for ci in range(4):
    gs([0, ci]).legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                       ncol=3, mode='expand', borderaxespad=0.)

# left labels
gs([0, 0]).set_ylabel('mixing depth, m')
gs([1, 0]).set_ylabel('water temperature\nsurface')
gs([2, 0]).set_ylabel('ice thickness')
gs([3, 0]).set_ylabel('O2 concentration\nbottom')
gs([4, 0]).set_ylabel('chl pool\nentire lake')

fig = plt.gcf()
fig.set_figheight(10)
fig.set_figwidth(9)

fig.savefig('loops.pdf')
