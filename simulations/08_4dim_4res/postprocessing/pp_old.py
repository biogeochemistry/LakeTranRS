import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy.ma as ma

n1 = 5
n2 = 5
n3 = 5
n4 = 5
nt = 2922
nz = 90
nr = 3 # responses

ser = pd.period_range('2010-01-01', periods=(365*4+1)*2)

a = np.ndarray((n1, n2, n3, n4, nr), dtype=np.float) * np.nan
a0 = np.ndarray((n1, n2, n3, n4, nr), dtype=np.float) * np.nan
m = np.zeros((n1, n2, n3, n4, nr), dtype=bool) 

d = pd.read_csv('../intermediate/parameterdict.csv')

for i, x1, x2, x3, x4, id in d.itertuples():
    if i % 100 == 100:
        print(i)
    if not os.path.exists('../simulations/id/{:05d}/t.csv.bz2'.format(id)):
        print(i, x1, x2, x3, x4, id)
        continue
    if id == 172:  # 2,5,2,2
        continue
    if id == 272:  # 2,5,1,3
        continue
    if id == 447:  # 2,5,3,4
        continue
    if id == 522:  # 2,5,1,5
        continue
    if id == 572:  # 2,5,3,5
        continue

    # t = pd.read_csv('../simulations/id/{:05d}/t.csv.bz2'.format(id), header=None)
    # t.index = ser
    chl = pd.read_csv('../simulations/id/{:05d}/chl.csv.bz2'.format(id), header=None)
    chl.index = ser
    # tp = pd.read_csv('../simulations/id/{:05d}/totp.csv.bz2'.format(id), header=None)
    # tp.index = ser
    o2 = pd.read_csv('../simulations/id/{:05d}/O2abs.csv.bz2'.format(id), header=None)
    o2.index = ser
    his = pd.read_csv('../simulations/id/{:05d}/His.csv.bz2'.format(id), header=None)
    his.index = ser


    # number of anoxia (O2 < 0.05 at bottom) per year (last 4 years)
    anoxia = (o2.loc[o2.index.year >= 2014].iloc[:, 89] < 0.05).sum() / 4 
    
    # mean annual maximum chl at surface (last 4 years)
    amc = chl.iloc[:, 89].groupby(chl.index.year).max()
    mamc = amc[amc.index >= 2014].mean()

    # number of ice covered days per year (last 4 years)
    ic = (his.loc[his.index.year >= 2014].iloc[:, 0] > 0).sum() / 4

    a0[x1-1, x2-1, x3-1, x4-1, 0] = anoxia
    a0[x1-1, x2-1, x3-1, x4-1, 1] = mamc * 1e3
    a0[x1-1, x2-1, x3-1, x4-1, 2] = ic


for i, x1, x2, x3, x4, id in d.itertuples():
    if not os.path.exists('../simulations/id/{:05d}/t.csv.bz2'.format(id)):
        m[x1-1, x2-1, x3-1, x4-1, :] = True

a = ma.masked_array(a0, mask=m)


## contour preparation
x = np.arange(5)
y = np.arange(5)
X, Y = np.meshgrid(x, y)


min0 = np.nanmin(a[:, :, :, :, 0])
max0 = np.nanmax(a[:, :, :, :, 0])
min1 = np.nanmin(a[:, :, :, :, 1])
max1 = np.nanmax(a[:, :, :, :, 1])
min2 = np.nanmin(a[:, :, :, :, 2])
max2 = np.nanmax(a[:, :, :, :, 2])



def rs(ax, thisa, cmapname, thismin, thismax, thisfmt, label1st, label2nd):
    img = ax.imshow(thisa, cmap=plt.get_cmap(cmapname), 
                    norm=matplotlib.colors.Normalize(thismin, thismax, True), 
                    origin='lower', interpolation='none')
    cont = ax.contour(X, Y, thisa, colors='black')
    ax.clabel(cont, infline=1, fontsize=8, colors='black', fmt=thisfmt)
    # ax.set_xlabel(label2nd)
    # ax.set_ylabel(label1st)
    ax.text(2.0, -0.9, label2nd, ha='center', va='center') ; 
    ax.text(-0.6, 2.0, label1st, va='center', ha='right', rotation='vertical')

    
plt.clf()
fig = plt.figure()
a00 = plt.subplot2grid((6, 3), (0, 0))
a01 = plt.subplot2grid((6, 3), (1, 0))
a02 = plt.subplot2grid((6, 3), (2, 0))
a03 = plt.subplot2grid((6, 3), (3, 0))
a04 = plt.subplot2grid((6, 3), (4, 0))
a05 = plt.subplot2grid((6, 3), (5, 0))
a10 = plt.subplot2grid((6, 3), (0, 1))
a11 = plt.subplot2grid((6, 3), (1, 1))
a12 = plt.subplot2grid((6, 3), (2, 1))
a13 = plt.subplot2grid((6, 3), (3, 1))
a14 = plt.subplot2grid((6, 3), (4, 1))
a15 = plt.subplot2grid((6, 3), (5, 1))
a20 = plt.subplot2grid((6, 3), (0, 2))
a21 = plt.subplot2grid((6, 3), (1, 2))
a22 = plt.subplot2grid((6, 3), (2, 2))
a23 = plt.subplot2grid((6, 3), (3, 2))
a24 = plt.subplot2grid((6, 3), (4, 2))
a25 = plt.subplot2grid((6, 3), (5, 2))

n = ['air temperature', 'wind speed', 'total P', 'DOC']

rs(a00, a[:, :, 1, 1, 0], 'Greens', min0, max0, '%.f', n[0], n[1])
rs(a01, a[:, 2, :, 1, 0], 'Greens', min0, max0, '%.f', n[0], n[2])
rs(a02, a[:, 2, 1, :, 0], 'Greens', min0, max0, '%.f', n[0], n[3]) 
rs(a03, a[2, :, :, 1, 0], 'Greens', min0, max0, '%.f', n[1], n[2])
rs(a04, a[2, :, 1, :, 0], 'Greens', min0, max0, '%.f', n[1], n[3])
rs(a05, a[2, 2, :, :, 0], 'Greens', min0, max0, '%.f', n[2], n[3])
rs(a10, a[:, :, 1, 1, 1], 'Reds', min1, max1, '%.f', n[0], n[1])
rs(a11, a[:, 2, :, 1, 1], 'Reds', min1, max1, '%.f', n[0], n[2])
rs(a12, a[:, 2, 1, :, 1], 'Reds', min1, max1, '%.f', n[0], n[3]) 
rs(a13, a[2, :, :, 1, 1], 'Reds', min1, max1, '%.f', n[1], n[2])
rs(a14, a[2, :, 1, :, 1], 'Reds', min1, max1, '%.f', n[1], n[3])
rs(a15, a[2, 2, :, :, 1], 'Reds', min1, max1, '%.f', n[2], n[3])
rs(a20, a[:, :, 1, 1, 2], 'Blues', min2, max2, '%.f', n[0], n[1])
rs(a21, a[:, 2, :, 1, 2], 'Blues', min2, max2, '%.f', n[0], n[2])
rs(a22, a[:, 2, 1, :, 2], 'Blues', min2, max2, '%.f', n[0], n[3]) 
rs(a23, a[2, :, :, 1, 2], 'Blues', min2, max2, '%.f', n[1], n[2])
rs(a24, a[2, :, 1, :, 2], 'Blues', min2, max2, '%.f', n[1], n[3])
rs(a25, a[2, 2, :, :, 2], 'Blues', min2, max2, '%.f', n[2], n[3])

a00.set_title('anoxia days y-1\nbottom')
a10.set_title('mean annual\nmax chl\nsurface')
a20.set_title('ice cover\ndays y-1')

for ax in fig.get_axes():
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_bgcolor('black')

fig.set_figheight(11)
fig.set_figwidth(6)
fig.savefig('RSver1.png', dpi=150)
