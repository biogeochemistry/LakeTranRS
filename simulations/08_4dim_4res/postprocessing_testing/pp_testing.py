import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy.ma as ma

# bz2 = '.bz2'  
bz2 = ''

bath = pd.read_csv('../bathymetry05.csv', header=None)
bath.columns = ['zz', 'Az']

lambdai = 5   # m-1
lambdas = 15  # m-1

n1 = 5
n2 = 5
n3 = 5
n4 = 5
nt = 2922
nz = 18
if nz == 18:
    zi = 17 ; z = 8.5
    zim = 4 ; zm = 2.0
    dz = 0.5
else:
    error 
nr = 11 # responses

ser = pd.period_range('2010-01-01', periods=(365*4+1)*2)

a = np.ndarray((n1, n2, n3, n4, nr), dtype=np.float) * np.nan
a0 = np.ndarray((n1, n2, n3, n4, nr), dtype=np.float) * np.nan
m = np.zeros((n1, n2, n3, n4, nr), dtype=bool) 

d = pd.read_csv('../intermediate/parameterdict.csv')

for i, x1, x2, x3, x4, id in d.itertuples():
    if i % 100 == 0:
        print(i)
    di = '../simulations/idtest/{:05d}'.format(id)
    if not os.path.exists(os.path.join(di, 't.csv{:s}'.format(bz2))):
        print(i, x1, x2, x3, x4, id)
        continue

    # if id == 599:
    #     continue

    t = pd.read_csv(os.path.join(di, 't.csv{:s}'.format(bz2)), header=None)
    t.index = ser
    chl = pd.read_csv(os.path.join(di, 'chl.csv{:s}'.format(bz2)), header=None)
    chl.index = ser
    # tp = pd.read_csv(os.path.join(di, 'totp.csv{:s}'.format(bz2)), header=None)
    # tp.index = ser
    o2 = pd.read_csv(os.path.join(di, 'O2abs.csv{:s}'.format(bz2)), header=None)
    o2.index = ser
    his = pd.read_csv(os.path.join(di, 'His.csv{:s}'.format(bz2)), header=None)
    his.index = ser
    lam = pd.read_csv(os.path.join(di, 'lambda.csv{:s}'.format(bz2)), header=None)
    lam.index = ser
    qst = pd.read_csv(os.path.join(di, 'Qst.csv{:s}'.format(bz2)), header=None)
    qst.index = ser ; qst.columns = ('sw', 'lw', 'sl')
                      

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
    amc = chl.iloc[:, 0].groupby(chl.index.year).max()
    mamc = amc[amc.index >= 2014].mean()

    # mean JJA chl at surface (last 4 yers)
    chlJJA = chl[(chl.index.month > 5) & (chl.index.month < 9) & 
                 (chl.index.year >= 2014)].iloc[:, 0].mean()

    # number of ice covered days per year (last 4 years)
    ic = (his.loc[his.index.year >= 2014].iloc[:, 0] > 0).sum() / 4
    
    # mean MAM irradiance at middle (last 4 years)
    # mean JJA irradiance at middle (last 4 years)
    ir00 = qst.sw * np.exp(-zm * lam.iloc[:, zim])
    ir00.index = ser
    ir1 = ir00[(ir00.index.month > 2) & (ir00.index.month < 6) &
               (ir00.index.year >= 2014)].mean()
    ir2 = ir00[(ir00.index.month > 5) & (ir00.index.month < 9) &
               (ir00.index.year >= 2014)].mean()

    # mixing depth -- mean JJ (last 4 years)
    pycnothresholdunit = 0.1 ## as per MyLake, kg m-3 m-1
    # pycnothresholdunit = 0.5 ## kg m-3 m-1 
    # 0.5 allows rigidness of the finer resolution? 
    pycnothreshold = pycnothresholdunit * dz
    tm = t.as_matrix()
    rho = 999.842594 + tm * (6.793952e-2 + tm * (-9.09529e-3 +                                                   tm * (1.001685e-4 + tm * (-1.120083e-6 + 6.536332e-9 * tm))))
    drho = rho[:, 1:] - rho[:, :(nz-1)]
    drhosig = drho * (drho > pycnothreshold)
    mdepbottom = np.zeros((drhosig.shape[0], )) * np.nan
    zzbottom = (np.flipud(bath.zz[:(nz-1)].as_matrix()+(dz/2)).\
                reshape((nz-1, 1))).flatten()
    for ri in range(drhosig.shape[0]):
        dsum = drhosig[ri, :].sum()
        if dsum == 0:
            mdepbottom[ri] = 0
        else:
            mdepbottom[ri] = (drhosig[ri, :] * zzbottom).sum() / dsum
    mdep = bath.zz.max() + dz - mdepbottom
    mdep = pd.DataFrame(mdep, index=ser)
    mdepJJ = mdep[(mdep.index.month > 5) & (mdep.index.month < 8)].mean()


    a0[x1-1, x2-1, x3-1, x4-1, 0] = anoxia1
    a0[x1-1, x2-1, x3-1, x4-1, 1] = anoxia2
    a0[x1-1, x2-1, x3-1, x4-1, 2] = anoxia3
    a0[x1-1, x2-1, x3-1, x4-1, 3] = mo21
    a0[x1-1, x2-1, x3-1, x4-1, 4] = mo22
    a0[x1-1, x2-1, x3-1, x4-1, 5] = mamc * 1e3
    a0[x1-1, x2-1, x3-1, x4-1, 6] = chlJJA * 1e3
    a0[x1-1, x2-1, x3-1, x4-1, 7] = ic
    a0[x1-1, x2-1, x3-1, x4-1, 8] = ir1
    a0[x1-1, x2-1, x3-1, x4-1, 9] = ir2
    a0[x1-1, x2-1, x3-1, x4-1, 10] = mdepJJ
    
    


for i, x1, x2, x3, x4, id in d.itertuples():
    di = '../simulations/idtest/{:05d}'.format(id)
    if not os.path.exists(os.path.join(di, 't.csv{:s}'.format(bz2))):
        m[x1-1, x2-1, x3-1, x4-1, :] = True

a = ma.masked_array(a0, mask=m)


## contour preparation
x = np.arange(5)
y = np.arange(5)
X, Y = np.meshgrid(x, y)


def rs(ax, thisa, cmapname, thismin, thismax, thisfmt, label1st, label2nd):
    img = ax.imshow(thisa, cmap=plt.get_cmap(cmapname), 
                    norm=matplotlib.colors.Normalize(thismin, thismax, True), 
                    origin='lower', interpolation='none')
    if not (thisa.min() == thisa.max()):
        cont = ax.contour(X, Y, thisa, colors='black')
        ax.clabel(cont, infline=1, fontsize=8, colors='black', fmt=thisfmt)
    # ax.set_xlabel(label2nd)
    # ax.set_ylabel(label1st)
    ax.text(2.0, -0.9, label2nd, ha='center', va='center') ; 
    ax.text(-0.6, 2.0, label1st, va='center', ha='right', rotation='vertical')

def plotrs6(rsi, nr, aa, colorcode, fmt, n) :
    '''returns 6 axes'''
    axes = [plt.subplot2grid((6, nr), (i, rsi)) for i in range(6)]
    mi = np.nanmin(aa)
    ma = np.nanmax(aa)
    rs(axes[0], aa[:, :, 2, 2], colorcode, mi, ma, fmt, n[0], n[1])
    rs(axes[1], aa[:, 2, :, 2], colorcode, mi, ma, fmt, n[0], n[2])
    rs(axes[2], aa[:, 2, 2, :], colorcode, mi, ma, fmt, n[0], n[3]) 
    rs(axes[3], aa[2, :, :, 2], colorcode, mi, ma, fmt, n[1], n[2])
    rs(axes[4], aa[2, :, 2, :], colorcode, mi, ma, fmt, n[1], n[3])
    rs(axes[5], aa[2, 2, :, :], colorcode, mi, ma, fmt, n[2], n[3])
    axes[5].text(-0.5, -1.8, mi, fontsize=10, ha='left', va='center')
    axes[5].text(-0.5, -2.4, ma, fontsize=10, ha='left', va='center')
    return axes


plt.clf()
fig = plt.figure()

n = ['air temp', 'wind speed', 'total P', 'DOC']

aa0 = plotrs6(0, nr, a[:, :, :, :, 0], 'Blues', '%.f', n)
aa1 = plotrs6(1, nr, a[:, :, :, :, 1], 'Blues', '%.f', n)
aa2 = plotrs6(2, nr, a[:, :, :, :, 2], 'Blues', '%.f', n)
aa3 = plotrs6(3, nr, a[:, :, :, :, 3], 'Purples', '%.2f', n)
aa4 = plotrs6(4, nr, a[:, :, :, :, 4], 'Purples', '%.2f', n)
aa5 = plotrs6(5, nr, a[:, :, :, :, 5], 'Greens', '%.f', n)
aa6 = plotrs6(6, nr, a[:, :, :, :, 6], 'Greens', '%.f', n)
aa7 = plotrs6(7, nr, a[:, :, :, :, 7], 'Reds', '%.f', n)
aa8 = plotrs6(8, nr, a[:, :, :, :, 8], 'Greys_r', '%.f', n)
aa9 = plotrs6(9, nr, a[:, :, :, :, 9], 'Greys_r', '%.2f', n)
aa10 = plotrs6(10, nr, a[:, :, :, :, 10], 'Oranges', '%.1f', n)

aa0[0].set_title('anoxia d y-1\nbottom')
aa1[0].set_title('anoxia d y-1\nbottom alt')
aa2[0].set_title('anoxia d y-1\nmiddle')
aa3[0].set_title('mean [O2]\nbottom')
aa4[0].set_title('mean [O2]\nmiddle')
aa5[0].set_title('mean annual\nmax chl\nsurface')
aa6[0].set_title('mean JJA chl\nsurface')
aa7[0].set_title('ice cover\ndays y-1')
aa8[0].set_title('mean MAM\nirradiance\nmiddle')
aa9[0].set_title('mean JJA\nirradiance\nmiddle')
aa10[0].set_title('mean JJ\nmixing depth')

for ax in fig.get_axes():
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_bgcolor('black')

fig.set_figheight(10)
fig.set_figwidth(18)
fig.savefig('RSver2.png', dpi=150, bbox_inches='tight')
fig.savefig('RSver2lowres.png', dpi=75, bbox_inches='tight')
