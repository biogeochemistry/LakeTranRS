import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

vv = ['O2abs', 'chl', 'totp', 't']

sns.set_style('whitegrid')

atdepths = [0, 10, 20, 40, 60, 89]

def drawlake(v):
    '''draws and saves figures based on a variable in lake water'''

    dlist = [pd.read_csv('../results/{:d}{:s}.csv.bz2'.format(cent, v), 
                         header=None)
             for cent in range(10)]
    for d in dlist:
        d.index = pd.period_range('2001-01-01', '2100-12-31')
    dlist = [d.groupby((d.index.year - 1) // 4, as_index=False, 
                           group_keys=False).mean() 
                 for d in dlist]
    for di, d in enumerate(dlist):
        dlist[di].index = pd.PeriodIndex(range(2001, 2100, 4), freq='4A')

    for depth in atdepths:
        fig = plt.figure(0)
        plt.clf()
        ax = fig.add_subplot(111)
        for centi, d in enumerate(dlist):
            ax.plot(d.index.start_time, d.iloc[:, depth], 
                    label='century run {:d}'.format(centi), 
                    color=plt.cm.coolwarm(centi/10.0))
        leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
        ax.set_title('{:s} lake water (4y mean), depth {:d}'.format(v, depth))
        ax.set_ylabel('{:s} lake water'.format(v))
        ax.set_xlabel('start year for 4-y cycles')
        fig.savefig('figures/{:s}depth{:02d}.png'.format(v, depth))

        fig = plt.figure(0)
        plt.clf()
        ax = fig.add_subplot(111)
        for centi, d in enumerate(dlist):
            if centi < 1:
                continue
            ax.plot(d.index.start_time, d.iloc[:, depth], 
                    label='century run {:d}'.format(centi), 
                    color=plt.cm.coolwarm(centi/10.0))
        leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
        ax.set_title('{:s} lake water (4y mean), depth {:d}'.format(v, depth))
        ax.set_ylabel('{:s} lake water'.format(v))
        ax.set_xlabel('start year for 4-y cycles')
        fig.savefig('figures/{:s}depth{:02d}zoomed1.png'.format(v, depth))
    

def writemarkdown(v):
    TEMPLATE = '''# VARIABLE lake water, depth DEPTH (2 levels of zoom, same data) 

![](../figures/VARIABLEdepthDEPTH.png) 
![](../figures/VARIABLEdepthDEPTHzoomed1.png) 

'''
    TEMPLATE = TEMPLATE.replace('VARIABLE', v)

    out = '\n'.join([TEMPLATE.replace('DEPTH', '{:02d}'.format(depth))
                     for depth in atdepths])

    fname = 'before_annotation/lake{:s}.md'.format(v)
    with open(fname, 'w') as f:
        f.write(out)

if __name__ == '__main__':
    for v in vv:
        drawlake(v)
        writemarkdown(v)







