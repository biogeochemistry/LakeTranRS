import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy.ma as ma

lambdai = 5   # m-1
lambdas = 15  # m-1

n1 = 5
n2 = 5
n3 = 5
n4 = 5
nt = 2922
nz = 18
if nz == 18:
    zi = 17
    zim = 4
else:
    error 
nr = 7 # responses

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

    # if id == 573:
    #     continue


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


    # number of anoxia (O2 < 0.05 at bottom) per year (last 4 years) def I
    anoxia1 = (o2.loc[o2.index.year >= 2014].iloc[:, zi] < 0.05).sum() / 4 

    # number of anoxia (O2 < 0.2 at bottom) per year (last 4 years) def II
    anoxia2 = (o2.loc[o2.index.year >= 2014].iloc[:, zi] < 0.2).sum() / 4 

    # number of anoxia (O2 < 0.4 at 2m at zim) per year (last 4 years) def III
    anoxia3 = (o2.loc[o2.index.year >= 2014].iloc[:, zim] < 0.4).sum() / 4 

    # mean O2 concentration at the bottom (last 4 years)
    mo21 = o2.iloc[:, zi].mean()

    # mean O2 concentration at 2m (last 4 years)
    mo22 = o2.iloc[:, zim].mean()

    
    # mean annual maximum chl at surface (last 4 years)
    amc = chl.iloc[:, zi].groupby(chl.index.year).max()
    mamc = amc[amc.index >= 2014].mean()

    # number of ice covered days per year (last 4 years)
    ic = (his.loc[his.index.year >= 2014].iloc[:, 0] > 0).sum() / 4

    a0[x1-1, x2-1, x3-1, x4-1, 0] = anoxia1
    a0[x1-1, x2-1, x3-1, x4-1, 1] = anoxia2
    a0[x1-1, x2-1, x3-1, x4-1, 2] = anoxia3
    a0[x1-1, x2-1, x3-1, x4-1, 3] = mo21
    a0[x1-1, x2-1, x3-1, x4-1, 4] = mo22
    a0[x1-1, x2-1, x3-1, x4-1, 5] = mamc * 1e3
    a0[x1-1, x2-1, x3-1, x4-1, 6] = ic


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
min3 = np.nanmin(a[:, :, :, :, 3])
max3 = np.nanmax(a[:, :, :, :, 3])
min4 = np.nanmin(a[:, :, :, :, 4])
max4 = np.nanmax(a[:, :, :, :, 4])
min5 = np.nanmin(a[:, :, :, :, 5])
max5 = np.nanmax(a[:, :, :, :, 5])
min6 = np.nanmin(a[:, :, :, :, 6])
max6 = np.nanmax(a[:, :, :, :, 6])



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
a00 = plt.subplot2grid((6, nr), (0, 0))
a01 = plt.subplot2grid((6, nr), (1, 0))
a02 = plt.subplot2grid((6, nr), (2, 0))
a03 = plt.subplot2grid((6, nr), (3, 0))
a04 = plt.subplot2grid((6, nr), (4, 0))
a05 = plt.subplot2grid((6, nr), (5, 0))
a10 = plt.subplot2grid((6, nr), (0, 1))
a11 = plt.subplot2grid((6, nr), (1, 1))
a12 = plt.subplot2grid((6, nr), (2, 1))
a13 = plt.subplot2grid((6, nr), (3, 1))
a14 = plt.subplot2grid((6, nr), (4, 1))
a15 = plt.subplot2grid((6, nr), (5, 1))
a20 = plt.subplot2grid((6, nr), (0, 2))
a21 = plt.subplot2grid((6, nr), (1, 2))
a22 = plt.subplot2grid((6, nr), (2, 2))
a23 = plt.subplot2grid((6, nr), (3, 2))
a24 = plt.subplot2grid((6, nr), (4, 2))
a25 = plt.subplot2grid((6, nr), (5, 2))
a30 = plt.subplot2grid((6, nr), (0, 3))
a31 = plt.subplot2grid((6, nr), (1, 3))
a32 = plt.subplot2grid((6, nr), (2, 3))
a33 = plt.subplot2grid((6, nr), (3, 3))
a34 = plt.subplot2grid((6, nr), (4, 3))
a35 = plt.subplot2grid((6, nr), (5, 3))
a40 = plt.subplot2grid((6, nr), (0, 4))
a41 = plt.subplot2grid((6, nr), (1, 4))
a42 = plt.subplot2grid((6, nr), (2, 4))
a43 = plt.subplot2grid((6, nr), (3, 4))
a44 = plt.subplot2grid((6, nr), (4, 4))
a45 = plt.subplot2grid((6, nr), (5, 4))
a50 = plt.subplot2grid((6, nr), (0, 5))
a51 = plt.subplot2grid((6, nr), (1, 5))
a52 = plt.subplot2grid((6, nr), (2, 5))
a53 = plt.subplot2grid((6, nr), (3, 5))
a54 = plt.subplot2grid((6, nr), (4, 5))
a55 = plt.subplot2grid((6, nr), (5, 5))
a60 = plt.subplot2grid((6, nr), (0, 6))
a61 = plt.subplot2grid((6, nr), (1, 6))
a62 = plt.subplot2grid((6, nr), (2, 6))
a63 = plt.subplot2grid((6, nr), (3, 6))
a64 = plt.subplot2grid((6, nr), (4, 6))
a65 = plt.subplot2grid((6, nr), (5, 6))

n = ['air temperature', 'wind speed', 'total P', 'DOC']

rs(a00, a[:, :, 2, 2, 0], 'Blues', min0, max0, '%.f', n[0], n[1])
rs(a01, a[:, 2, :, 2, 0], 'Blues', min0, max0, '%.f', n[0], n[2])
rs(a02, a[:, 2, 2, :, 0], 'Blues', min0, max0, '%.f', n[0], n[3]) 
rs(a03, a[2, :, :, 2, 0], 'Blues', min0, max0, '%.f', n[1], n[2])
rs(a04, a[2, :, 2, :, 0], 'Blues', min0, max0, '%.f', n[1], n[3])
rs(a05, a[2, 2, :, :, 0], 'Blues', min0, max0, '%.f', n[2], n[3])
rs(a10, a[:, :, 2, 2, 1], 'Blues', min1, max1, '%.f', n[0], n[1])
rs(a11, a[:, 2, :, 2, 1], 'Blues', min1, max1, '%.f', n[0], n[2])
rs(a12, a[:, 2, 2, :, 1], 'Blues', min1, max1, '%.f', n[0], n[3]) 
rs(a13, a[2, :, :, 2, 1], 'Blues', min1, max1, '%.f', n[1], n[2])
rs(a14, a[2, :, 2, :, 1], 'Blues', min1, max1, '%.f', n[1], n[3])
rs(a15, a[2, 2, :, :, 1], 'Blues', min1, max1, '%.f', n[2], n[3])
rs(a20, a[:, :, 2, 2, 2], 'Blues', min2, max2, '%.f', n[0], n[1])
rs(a21, a[:, 2, :, 2, 2], 'Blues', min2, max2, '%.f', n[0], n[2])
rs(a22, a[:, 2, 2, :, 2], 'Blues', min2, max2, '%.f', n[0], n[3]) 
rs(a23, a[2, :, :, 2, 2], 'Blues', min2, max2, '%.f', n[1], n[2])
rs(a24, a[2, :, 2, :, 2], 'Blues', min2, max2, '%.f', n[1], n[3])
rs(a25, a[2, 2, :, :, 2], 'Blues', min2, max2, '%.f', n[2], n[3])
rs(a30, a[:, :, 2, 2, 3], 'Blues', min3, max3, '%.f', n[0], n[1])
rs(a31, a[:, 2, :, 2, 3], 'Blues', min3, max3, '%.f', n[0], n[2])
rs(a32, a[:, 2, 2, :, 3], 'Blues', min3, max3, '%.f', n[0], n[3]) 
rs(a33, a[2, :, :, 2, 3], 'Blues', min3, max3, '%.f', n[1], n[2])
rs(a34, a[2, :, 2, :, 3], 'Blues', min3, max3, '%.f', n[1], n[3])
rs(a35, a[2, 2, :, :, 3], 'Blues', min3, max3, '%.f', n[2], n[3])
rs(a40, a[:, :, 2, 2, 4], 'Blues', min4, max4, '%.f', n[0], n[1])
rs(a41, a[:, 2, :, 2, 4], 'Blues', min4, max4, '%.f', n[0], n[2])
rs(a42, a[:, 2, 2, :, 4], 'Blues', min4, max4, '%.f', n[0], n[3]) 
rs(a43, a[2, :, :, 2, 4], 'Blues', min4, max4, '%.f', n[1], n[2])
rs(a44, a[2, :, 2, :, 4], 'Blues', min4, max4, '%.f', n[1], n[3])
rs(a45, a[2, 2, :, :, 4], 'Blues', min4, max4, '%.f', n[2], n[3])
rs(a50, a[:, :, 2, 2, 5], 'Blues', min5, max5, '%.f', n[0], n[1])
rs(a51, a[:, 2, :, 2, 5], 'Blues', min5, max5, '%.f', n[0], n[2])
rs(a52, a[:, 2, 2, :, 5], 'Blues', min5, max5, '%.f', n[0], n[3]) 
rs(a53, a[2, :, :, 2, 5], 'Blues', min5, max5, '%.f', n[1], n[2])
rs(a54, a[2, :, 2, :, 5], 'Blues', min5, max5, '%.f', n[1], n[3])
rs(a55, a[2, 2, :, :, 5], 'Blues', min5, max5, '%.f', n[2], n[3])
rs(a60, a[:, :, 2, 2, 6], 'Blues', min6, max6, '%.f', n[0], n[1])
rs(a61, a[:, 2, :, 2, 6], 'Blues', min6, max6, '%.f', n[0], n[2])
rs(a62, a[:, 2, 2, :, 6], 'Blues', min6, max6, '%.f', n[0], n[3]) 
rs(a63, a[2, :, :, 2, 6], 'Blues', min6, max6, '%.f', n[1], n[2])
rs(a64, a[2, :, 2, :, 6], 'Blues', min6, max6, '%.f', n[1], n[3])
rs(a65, a[2, 2, :, :, 6], 'Blues', min6, max6, '%.f', n[2], n[3])

a00.set_title('anoxia days y-1\nbottom')
a50.set_title('mean annual\nmax chl\nsurface')
a60.set_title('ice cover\ndays y-1')

for ax in fig.get_axes():
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_bgcolor('black')

fig.set_figheight(11)
fig.set_figwidth(12)
fig.savefig('RSver2.png', dpi=150)
