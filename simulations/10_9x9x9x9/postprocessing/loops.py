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


# http://stackoverflow.com/questions/34017866/arrow-on-a-line-plot-with-matplotlib
def add_arrow(line, position, direction='right', size=10, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   index in the data at which arrow is drawn
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    start_ind = position
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1
    line.axes.annotate('',
                       xytext=(xdata[start_ind], ydata[start_ind]),
                       xy=(xdata[end_ind], ydata[end_ind]),
                       arrowprops=dict(arrowstyle="simple", fc=color, ec=color),
                       size=size)


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
    print(fname)

gs = gridspec.GridSpec(5, 4)


def plotloops(savefname, arrow=False, panels=True):
    plt.clf()
    for ci in range(4):     
        col0 = ('blue', 'pink',  'lightgreen',  'pink')[ci]
        col1 = ( 'red',       'darkorange', 'darkgreen', 'brown')[ci]
        dname = ('AT', 'WS', 'TP', 'DOC')[ci]
        for ri in range(5):
            lim0 = (8,  0,   0, 1e0, 0.01)[ri]
            lim1 = (0, 21, 0.7, 1e4, 10)[ri]
            if (ri == 0) and (not ci == 1):
                lim0 = 3.2 ; lim1 = 1.8
            if (ri == 4) and (not ci == 2):
                lim0 = 0.08; lim1 = 1

            plt.subplot(gs[ri, ci], aspect='equal')
            d = da[ci, ri, :, :]  # doy x sim
            if ri == 0: # mixing depth only wants JJ months
                d[:(31+28+31+30+31), :] = np.nan
                d[(31+28+31+30+31+30+31):, :] = np.nan
            print(ci, ri, d.shape)
            plt.subplot(gs[ri, ci]).plot([lim0, lim1], [lim0, lim1], 
                                         color='lightgray', linewidth=lw)
            if ri == 3: # oxygen
                plt.subplot(gs[ri, ci]).set_xscale('log')
                plt.subplot(gs[ri, ci]).set_yscale('log')
                plt.subplot(gs[ri, ci]).axhline(3000, color='lightgray', linewidth=lw)
                plt.subplot(gs[ri, ci]).axhline(16, color='lightgray', linewidth=lw)
                plt.subplot(gs[ri, ci]).axvline(3000, color='lightgray', linewidth=lw)
                plt.subplot(gs[ri, ci]).axvline(16, color='lightgray', linewidth=lw)
            if ri == 4: # chl
                plt.subplot(gs[ri, ci]).set_xscale('log')
                plt.subplot(gs[ri, ci]).set_yscale('log')
            L0 = plt.subplot(gs[ri, ci]).plot(d[:, 0], d[:, 1], 
                                              color=col0, 
                                              label='low {:s}'.format(dname))[0]
            L1 = plt.subplot(gs[ri, ci]).plot(d[:, 0], d[:, 2],
                                              color=col1,
                                              label='high {:s}'.format(dname))[0]
            plt.subplot(gs[ri, ci]).set_xlim([lim0, lim1])
            plt.subplot(gs[ri, ci]).set_ylim([lim0, lim1])
            if arrow:
                add_arrow(L0, 15) # mid-january
                add_arrow(L0, 31+28+31+15) # mid-april
                add_arrow(L0, 31+28+31+30+31+30+15) # mid-july
                add_arrow(L0, 31+28+31+30+31+30+31+31+30+15) # mid-october
                add_arrow(L1, 15) # mid-january
                add_arrow(L1, 31+28+31+15) # mid-april
                add_arrow(L1, 31+28+31+30+31+30+15) # mid-july
                add_arrow(L1, 31+28+31+30+31+30+31+31+30+15) # mid-october
            
                
    # legends at the top
    for ci in range(4):
        plt.subplot(gs[0, ci]).legend(
            bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
            ncol=1, mode='expand', borderaxespad=0.)

    # left labels
    plt.subplot(gs[0, 0]).set_ylabel('mixing depth, m')
    plt.subplot(gs[1, 0]).set_ylabel('water temperature\nsurface')
    plt.subplot(gs[2, 0]).set_ylabel('ice thickness')
    plt.subplot(gs[3, 0]).set_ylabel('O2 concentration\nbottom')
    plt.subplot(gs[4, 0]).set_ylabel('chl pool\nentire lake')

    # panel labels
    plt.subplot(gs[0, 0]).text(0.1, 0.9, 'a', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[0, 0]).transAxes)
    plt.subplot(gs[1, 0]).text(0.1, 0.9, 'b', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[1, 0]).transAxes)
    plt.subplot(gs[2, 0]).text(0.1, 0.9, 'c', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[2, 0]).transAxes)
    plt.subplot(gs[3, 0]).text(0.1, 0.9, 'd', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[3, 0]).transAxes)
    plt.subplot(gs[4, 0]).text(0.1, 0.9, 'e', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[4, 0]).transAxes)
    plt.subplot(gs[0, 1]).text(0.1, 0.9, 'f', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[0, 1]).transAxes)
    plt.subplot(gs[1, 1]).text(0.1, 0.9, 'g', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[1, 1]).transAxes)
    plt.subplot(gs[2, 1]).text(0.1, 0.9, 'h', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[2, 1]).transAxes)
    plt.subplot(gs[3, 1]).text(0.1, 0.9, 'i', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[3, 1]).transAxes)
    plt.subplot(gs[4, 1]).text(0.1, 0.9, 'j', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[4, 1]).transAxes)
    plt.subplot(gs[0, 2]).text(0.1, 0.9, 'k', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[0, 2]).transAxes)
    plt.subplot(gs[1, 2]).text(0.1, 0.9, 'l', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[1, 2]).transAxes)
    plt.subplot(gs[2, 2]).text(0.1, 0.9, 'm', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[2, 2]).transAxes)
    plt.subplot(gs[3, 2]).text(0.1, 0.9, 'n', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[3, 2]).transAxes)
    plt.subplot(gs[4, 2]).text(0.1, 0.9, 'o', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[4, 2]).transAxes)
    plt.subplot(gs[0, 3]).text(0.1, 0.9, 'p', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[0, 3]).transAxes)
    plt.subplot(gs[1, 3]).text(0.1, 0.9, 'q', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[1, 3]).transAxes)
    plt.subplot(gs[2, 3]).text(0.1, 0.9, 'r', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[2, 3]).transAxes)
    plt.subplot(gs[3, 3]).text(0.1, 0.9, 's', ha='center', va='center',
                               weight='bold', size=10, 
                               transform=plt.subplot(gs[3, 3]).transAxes)
    plt.subplot(gs[4, 3]).text(0.1, 0.9, 't', ha='center', va='center',
                               weight='bold', size=10,
                               transform=plt.subplot(gs[4, 3]).transAxes)


    fig = plt.gcf()
    fig.set_figheight(10)
    fig.set_figwidth(9)

    fig.savefig('{:s}.png'.format(savefname), dpi=150, bbox_inches='tight')
    fig.savefig('{:s}.pdf'.format(savefname), dpi=150, bbox_inches='tight')

plotloops('loops', False, True)
# plotloops('loops arrows', arrow=True)
