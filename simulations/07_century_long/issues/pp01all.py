import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

vv = ['NH4', 'NO3', 'O2', 'OM', 'OMb', 'OMS', 'PO4', 'PO4adsa']

sns.set_style('whitegrid')

atdepths = [0, 4, 8, 16, 32, 63]

def drawsediment(v):
    '''draws and saves figures based on a variable in sediment'''

    dlist = [pd.read_csv('../results/{:d}sed{:s}.csv.bz2'.format(cent, v), 
                         header=None)
             for cent in range(10)]
    for d in dlist:
        d.index = pd.period_range('2001-01-01', '2100-12-31')
    dlist = [d.groupby((d.index.year - 1) // 4, as_index=False, 
                           group_keys=False).mean() 
                 for d in dlist]
    for d in dlist:
        d.index = pd.PeriodIndex(range(2001, 2100, 4), freq='4A')

    fig = plt.figure(0)
    plt.clf()
    ax = fig.add_subplot(111)
    for centi, d in enumerate(dlist):
        ax.plot(d.index.start_time, d.iloc[:, 0], 
                label='century run {:d}'.format(centi), 
                color=plt.cm.coolwarm(centi/10.0))
    leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
    ax.set_title('{:s} concentration top sediment (4y mean)'.format(v))
    ax.set_ylabel('{:s} concentration sediment'.format(v))
    ax.set_xlabel('start year for 4-y cycles')
    fig.savefig('figures/{:s}sedtop.png'.format(v))

    fig = plt.figure(0)
    plt.clf()
    ax = fig.add_subplot(111)
    for centi, d in enumerate(dlist):
        if centi < 1:
            continue
        ax.plot(d.index.start_time, d.iloc[:, 0], 
                label='century run {:d}'.format(centi), 
                color=plt.cm.coolwarm(centi/10.0))
    leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
    ax.set_title('{:s} concentration top sediment (4y mean)\nzoom level 1'.format(v))
    ax.set_ylabel('{:s} concentration sediment'.format(v))
    ax.set_xlabel('start year for 4-y cycles')
    fig.savefig('figures/{:s}sedtopzoomed1.png'.format(v))

    fig = plt.figure(0)
    plt.clf()
    ax = fig.add_subplot(111)
    for centi, d in enumerate(dlist):
        if centi < 2:
            continue
        ax.plot(d.index.start_time, d.iloc[:, 0], 
                label='century run {:d}'.format(centi), 
                color=plt.cm.coolwarm(centi/10.0))
    leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
    ax.set_title('{:s} concentration top sediment (4y mean)\nzoom level 2'.format(v))
    ax.set_ylabel('{:s} concentration sediment'.format(v))
    ax.set_xlabel('start year for 4-y cycles')
    fig.savefig('figures/{:s}sedtopzoomed2.png'.format(v))

    fig = plt.figure(0)
    plt.clf()
    ax = fig.add_subplot(111)
    for centi, d in enumerate(dlist):
        ax.plot(d.index.start_time, d.iloc[:, 32], 
                label='century run {:d}'.format(centi), 
                color=plt.cm.coolwarm(centi/10.0))
    leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
    ax.set_title('{:s} concentration middle sediment (4y mean)'.format(v))
    ax.set_ylabel('{:s} concentration sediment layer 33/64'.format(v))
    ax.set_xlabel('start year for 4-y cycles')
    fig.savefig('figures/{:s}sedmid.png'.format(v))

    fig = plt.figure(0)
    plt.clf()
    ax = fig.add_subplot(111)
    for centi, d in enumerate(dlist):
        if centi < 1:
            continue
        ax.plot(d.index.start_time, d.iloc[:, 32], 
                label='century run {:d}'.format(centi), 
                color=plt.cm.coolwarm(centi/10.0))
    leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
    ax.set_title('{:s} concentration middle sediment (4y mean)\nzoom level 1'.format(v))
    ax.set_ylabel('{:s} concentration sediment layer 33/64'.format(v))
    ax.set_xlabel('start year for 4-y cycles')
    fig.savefig('figures/{:s}sedmidzoomed1.png'.format(v))

    fig = plt.figure(0)
    plt.clf()
    ax = fig.add_subplot(111)
    for centi, d in enumerate(dlist):
        if centi < 2:
            continue
        ax.plot(d.index.start_time, d.iloc[:, 32], 
                label='century run {:d}'.format(centi), 
                color=plt.cm.coolwarm(centi/10.0))
    leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
    ax.set_title('{:s} concentration middle sediment (4y mean)\nzoom level 2'.format(v))
    ax.set_ylabel('{:s} concentration sediment layer 33/64'.format(v))
    ax.set_xlabel('start year for 4-y cycles')
    fig.savefig('figures/{:s}sedmidzoomed2.png'.format(v))

def writemarkdown(v):
    TEMPLATE = '''# OM concentration sediment TOP (3 levels of zoom, same data) 

![](../figures/OMsedtop.png) 
![](../figures/OMsedtopzoomed1.png) 
![](../figures/OMsedtopzoomed2.png) 

# OM concentration sediment MIDDLE (3 levels of zoom, same data) 

![](../figures/OMsedmid.png) 
![](../figures/OMsedmidzoomed1.png) 
![](../figures/OMsedmidzoomed2.png)
'''
    out = TEMPLATE.replace('OM', v)
    fname = 'before_annotation/{:s}.md'.format(v)
    with open(fname, 'w') as f:
        f.write(out)

if __name__ == '__main__':
    for v in vv:
        # drawsediment(v)
        writemarkdown(v)







