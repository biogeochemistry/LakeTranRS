import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

atdepths = [0, 4, 8, 16, 32, 63]

dlist = [pd.read_csv('../results/{:d}sedO2.csv.bz2'.format(cent), header=None)
         for cent in range(10)]
for d in dlist:
    d.index = pd.period_range('2001-01-01', '2100-12-31')
# dlist = [d.resample('A').mean() for d in dlist]
dlist = [d.groupby((d.index.year - 1) // 4, as_index=False, 
                   group_keys=False).mean() 
         for d in dlist]
for d in dlist:
    d.index = pd.PeriodIndex(range(2001, 2100, 4), freq='4A')

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)
for centi, d in enumerate(dlist):
    # if centi == 0:
    #     continue
    ax.plot(d.index.start_time, d.iloc[:, 0], 
            label='century run {:d}'.format(centi), 
            color=plt.cm.coolwarm(centi/10.0))
leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
ax.set_title('O2 concentration top sediment (4y mean)')
ax.set_ylabel('O2 concentration sediment')
ax.set_xlabel('start year for 4-y cycles')
fig.savefig('../figures/O2sedtop.png')
plt.clf()

fig = plt.figure()
ax = fig.add_subplot(111)
for centi, d in enumerate(dlist):
    if centi < 1:
        continue
    ax.plot(d.index.start_time, d.iloc[:, 0], 
            label='century run {:d}'.format(centi), 
            color=plt.cm.coolwarm(centi/10.0))
leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
ax.set_title('O2 concentration top sediment (4y mean)')
ax.set_ylabel('O2 concentration sediment')
ax.set_xlabel('start year for 4-y cycles')
fig.savefig('../figures/O2sedtopzoomed1.png')

fig = plt.figure()
ax = fig.add_subplot(111)
for centi, d in enumerate(dlist):
    if centi < 2:
        continue
    ax.plot(d.index.start_time, d.iloc[:, 0], 
            label='century run {:d}'.format(centi), 
            color=plt.cm.coolwarm(centi/10.0))
leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
ax.set_title('O2 concentration top sediment (4y mean)')
ax.set_ylabel('O2 concentration sediment')
ax.set_xlabel('start year for 4-y cycles')
fig.savefig('../figures/O2sedtopzoomed2.png')




plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)
for centi, d in enumerate(dlist):
    # if centi == 0:
    #     continue
    ax.plot(d.index.start_time, d.iloc[:, 32], 
            label='century run {:d}'.format(centi), 
            color=plt.cm.coolwarm(centi/10.0))
leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
ax.set_title('O2 concentration middle sediment (4y mean)')
ax.set_ylabel('O2 concentration sediment layer 33/64')
ax.set_xlabel('start year for 4-y cycles')
fig.savefig('../figures/O2sedmid.png')
plt.clf()

fig = plt.figure()
ax = fig.add_subplot(111)
for centi, d in enumerate(dlist):
    if centi < 1:
        continue
    ax.plot(d.index.start_time, d.iloc[:, 32], 
            label='century run {:d}'.format(centi), 
            color=plt.cm.coolwarm(centi/10.0))
leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
ax.set_title('O2 concentration middle sediment (4y mean)')
ax.set_ylabel('O2 concentration sediment layer 33/64')
ax.set_xlabel('start year for 4-y cycles')
fig.savefig('../figures/O2sedmidzoomed1.png')

fig = plt.figure()
ax = fig.add_subplot(111)
for centi, d in enumerate(dlist):
    if centi < 2:
        continue
    ax.plot(d.index.start_time, d.iloc[:, 32], 
            label='century run {:d}'.format(centi), 
            color=plt.cm.coolwarm(centi/10.0))
leg = ax.legend(loc='bottom right', ncol=2, frameon=True)
ax.set_title('O2 concentration middle sediment (4y mean)')
ax.set_ylabel('O2 concentration sediment layer 33/64')
ax.set_xlabel('start year for 4-y cycles')
fig.savefig('../figures/O2sedmidzoomed2.png')





