import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


d = pd.read_csv('../results/sedfluxes.csv.bz2', 
                names =  ['OM', 'OM2', 'Oxygen', 'PO4', 'Fe2+', 
                          'NO3-', 'NH4+', 'Al(OH)3', 'PO4adsa', 'Fe(OH)3'])
d.index = pd.period_range('2001-01-01', '2100-12-31')


sns.set_style('darkgrid')

for name, ser in d.resample('A').mean().iteritems():
    plt.clf()
    a = ser.iloc[3:].plot()
    a.set_ylabel(name)
    fig = plt.gcf()
    fig.set_figheight(4)
    fig.set_figwidth(6)
    fig.set_dpi(600)
    fig.savefig('../figures/sed{:s}.png'.format(name), bbox_inches='tight')





