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

# lambdai = 5   m-1
# lambdas = 15  m-1

# nn = 9
skip = (1, 2, 3, 4, 6, 7, 8, 9)
n1 = 51
n2 = 51
n3 = 1
n4 = 1
nt = 2922
nz = 18
if nz == 18:
    zi = 17 ; z = 8.5
    zim = 4 ; zm = 2.0
    dz = 0.5
else:
    error 

## these two below in the end should become consistent
nr = 6 # responses (used for plotting)
nrold = 11 # responses old version (used to keep the matrix collection)

ser = pd.period_range('2010-01-01', periods=(365*4+1)*2)

a = np.ndarray((n1, n2, n3, n4, nrold), dtype=np.float) * np.nan
a0 = np.ndarray((n1, n2, n3, n4, nrold), dtype=np.float) * np.nan
m = np.zeros((n1, n2, n3, n4, nrold), dtype=bool) 

d = pd.read_csv('../intermediate/parameterdict.csv')

for i, x1, x2, x3, x4, id in d.itertuples():
    if i % 100 == 0:
        print(i)
    di = '../simulations/id/{:06d}'.format(id)
    if not os.path.exists(os.path.join(di, 't.csv{:s}'.format(bz2))):
        print('missing', i, x1, x2, x3, x4, id)
        continue
    skipcount = 0
    skipcount += x1 in skip
    skipcount += x2 in skip
    skipcount += x3 in skip
    skipcount += x4 in skip
    if skipcount >= 3:
        continue

    # if id == 599:
    #     continue

    t = pd.read_csv(os.path.join(di, 't.csv{:s}'.format(bz2)), header=None)
    t.index = ser
    chl = pd.read_csv(os.path.join(di, 'chl.csv{:s}'.format(bz2)), header=None)
    chl.index = ser
    # tp = pd.read_csv(os.path.join(di, 'totp.csv{:s}'.format(bz2)), header=None)
    # tp.index = ser
    o2 = pd.read_csv(os.path.join(di, 'O2zt.csv{:s}'.format(bz2)), header=None)
    o2.index = ser
    his = pd.read_csv(os.path.join(di, 'His.csv{:s}'.format(bz2)), header=None)
    his.index = ser
    # lam = pd.read_csv(os.path.join(di, 'lambda.csv{:s}'.format(bz2)), header=None)
    # lam.index = ser
    # qst = pd.read_csv(os.path.join(di, 'Qst.csv{:s}'.format(bz2)), header=None)
    # qst.index = ser ; qst.columns = ('sw', 'lw', 'sl')
                      

    # number of anoxia (O2 < 0.05 at bottom) per year (last 4 years) def I
    anoxia1 = (o2.loc[o2.index.year >= 2014].iloc[:, zi] < 3000).sum() / 4 

    # number of anoxia (O2 < 0.2 at bottom) per year (last 4 years) def II
    anoxia2 = (o2.loc[o2.index.year >= 2014].iloc[:, zi] < 16).sum() / 4 

    # # number of anoxia (O2 < 0.4 at 2m at zim) per year (last 4 years) def III
    # anoxia3 = (o2.loc[o2.index.year >= 2014].iloc[:, zim] < 0.4).sum() / 4 

    # # mean O2 concentration at the bottom (last 4 years)
    # mo21 = o2.iloc[:, zi].mean()

    # # mean O2 concentration at 2m (last 4 years)
    # mo22 = o2.iloc[:, zim].mean()
    
    # # mean annual maximum chl at surface (last 4 years)
    # amc = chl.iloc[:, 0].groupby(chl.index.year).max()
    # mamc = amc[amc.index >= 2014].mean()

    # mean JJA chl at surface (last 4 yers)
    chlJJA = chl[(chl.index.month > 5) & (chl.index.month < 9) & 
                 (chl.index.year >= 2014)].iloc[:, 0].mean()

    # number of ice covered days per year (last 4 years)
    ic = (his.loc[his.index.year >= 2014].iloc[:, 0] > 0).sum() / 4
    
    # # mean MAM irradiance at middle (last 4 years)
    # # mean JJA irradiance at middle (last 4 years)
    # ir00 = qst.sw * np.exp(-zm * lam.iloc[:, zim])
    # ir00.index = ser
    # ir1 = ir00[(ir00.index.month > 2) & (ir00.index.month < 6) &
    #            (ir00.index.year >= 2014)].mean()
    # ir2 = ir00[(ir00.index.month > 5) & (ir00.index.month < 9) &
    #            (ir00.index.year >= 2014)].mean()

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
    # a0[x1-1, x2-1, x3-1, x4-1, 2] = anoxia3
    # a0[x1-1, x2-1, x3-1, x4-1, 3] = mo21
    # a0[x1-1, x2-1, x3-1, x4-1, 4] = mo22
    # a0[x1-1, x2-1, x3-1, x4-1, 5] = mamc * 1e3
    a0[x1-1, x2-1, x3-1, x4-1, 6] = chlJJA * 1e3
    a0[x1-1, x2-1, x3-1, x4-1, 7] = ic
    # a0[x1-1, x2-1, x3-1, x4-1, 8] = ir1
    # a0[x1-1, x2-1, x3-1, x4-1, 9] = ir2
    a0[x1-1, x2-1, x3-1, x4-1, 10] = mdepJJ
    
    


# for i, x1, x2, x3, x4, id in d.itertuples():
#     di = '../simulations/id/{:06d}'.format(id)
#     if not os.path.exists(os.path.join(di, 't.csv{:s}'.format(bz2))):
#         m[x1-1, x2-1, x3-1, x4-1, :] = True

# a = ma.masked_array(a0, mask=m)


## contour preparation
x = np.arange(n1)
y = np.arange(n2)
X, Y = np.meshgrid(x, y)


def rs(ax, thisa, cmapname, thismin, thismax, thisfmt, label1st, label2nd):
    img = ax.imshow(thisa, cmap=plt.get_cmap(cmapname), 
                    norm=matplotlib.colors.Normalize(thismin, thismax, True), 
                    origin='lower', interpolation='none')
    # if not (thisa.min() == thisa.max()):
    #     cont = ax.contour(X, Y, thisa, colors='black')
    #     ax.clabel(cont, infline=1, fontsize=8, colors='black', fmt=thisfmt)
    # ax.set_xlabel(label2nd)
    # ax.set_ylabel(label1st)
    ax.text(25.0, -5.4, label2nd, ha='center', va='center') ; 
    ax.text(-2.6, 25.0, label1st, va='center', ha='right', rotation='vertical')

def plotrs6(rsi, nr, aa, colorcode, fmt, fmt3, n) :
    '''returns 6 axes. rsi is the column in the RS plot'''
    axes = [plt.subplot2grid((6, nr), (i, rsi)) for i in range(6)]
    mi = np.nanmin(aa)
    ma = np.nanmax(aa)
    rs(axes[0], aa[:, :, 0, 0], colorcode, mi, ma, fmt, n[0], n[1])
    # rs(axes[1], aa[:, 4, :, 4], colorcode, mi, ma, fmt, n[0], n[2])
    # rs(axes[2], aa[:, 4, 4, :], colorcode, mi, ma, fmt, n[0], n[3]) 
    # rs(axes[3], aa[4, :, :, 4], colorcode, mi, ma, fmt, n[1], n[2])
    # rs(axes[4], aa[4, :, 4, :], colorcode, mi, ma, fmt, n[1], n[3])
    # rs(axes[5], aa[4, 4, :, :], colorcode, mi, ma, fmt, n[2], n[3])
    # axes[5].text(-0.5, -3.0, 'min: ' + fmt3.format(mi), 
    #              fontsize=10, ha='left', va='center')
    # axes[5].text(-0.5, -4.5, 'max: ' + fmt3.format(ma), 
    #              fontsize=10, ha='left', va='center')
    return axes


plt.clf()
fig = plt.figure()

n = ['air temp', 'wind speed', 'total P', 'DOC']

aa0 = plotrs6(0, nr, a[:, :, :, :, 0], 'Reds', '%.f', '{:.1f}', n)
aa1 = plotrs6(1, nr, a[:, :, :, :, 1], 'Reds', '%.f', '{:.1f}', n)
# aa2 = plotrs6(_, nr, a[:, :, :, :, 2], 'Blues', '%.f', '{:.1f}',n)
# aa3 = plotrs6(_, nr, a[:, :, :, :, 3], 'Purples', '%.2f', '{:.1f}',n)
# aa4 = plotrs6(_, nr, a[:, :, :, :, 4], 'Purples', '%.2f', '{:.1f}',n)
# aa5 = plotrs6(_, nr, a[:, :, :, :, 5], 'Greens', '%.f', '{:.1f}',n)
aa6 = plotrs6(2, nr, a[:, :, :, :, 6], 'Greens', '%.f', '{:.1f}',n)
aa7 = plotrs6(3, nr, a[:, :, :, :, 7], 'Blues_r', '%.f', '{:.1f}',n)
# aa8 = plotrs6(_, nr, a[:, :, :, :, 8], 'Greys_r', '%.f', '{:.1f}',n)
# aa9 = plotrs6(_, nr, a[:, :, :, :, 9], 'Greys_r', '%.2f', '{:.1f}',n)
aa10 = plotrs6(4, nr, a[:, :, :, :, 10], 'Oranges', '%.1f', '{:.1f}',n)

aa0[0].set_title('hypoxia d y-1\nhypolimnion')
aa1[0].set_title('anoxia d y-1\nhypolimnion')
# aa2[0].set_title('anoxia d y-1\nmiddle')
# aa3[0].set_title('mean [O2]\nbottom')
# aa4[0].set_title('mean [O2]\nmiddle')
# aa5[0].set_title('mean annual\nmax chl\nsurface')
aa6[0].set_title('mean JJA chl\nsurface')
aa7[0].set_title('ice cover\ndays y-1')
# aa8[0].set_title('mean MAM\nirradiance\nmiddle')
# aa9[0].set_title('mean JJA\nirradiance\nmiddle')
aa10[0].set_title('mean JJ\nmixing depth')

for ax in fig.get_axes():
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_bgcolor('black')

## adds plot labels
def addlabel(aaa, label):
    aaa.text(-0.06, -0.1, label, ha='center', va='center', weight='bold',
             size=10, transform=aaa.transAxes)
addlabel(aa0[0], 'a1')
# addlabel(aa0[1], 'a2')
# addlabel(aa0[2], 'a3')
# addlabel(aa0[3], 'a4')
# addlabel(aa0[4], 'a5')
# addlabel(aa0[5], 'a6')
addlabel(aa1[0], 'b1')
# addlabel(aa1[1], 'b2')
# addlabel(aa1[2], 'b3')
# addlabel(aa1[3], 'b4')
# addlabel(aa1[4], 'b5')
# addlabel(aa1[5], 'b6')
addlabel(aa6[0], 'c1')
# addlabel(aa6[1], 'c2')
# addlabel(aa6[2], 'c3')
# addlabel(aa6[3], 'c4')
# addlabel(aa6[4], 'c5')
# addlabel(aa6[5], 'c6')
addlabel(aa7[0], 'd1')
# addlabel(aa7[1], 'd2')
# addlabel(aa7[2], 'd3')
# addlabel(aa7[3], 'd4')
# addlabel(aa7[4], 'd5')
# addlabel(aa7[5], 'd6')
addlabel(aa10[0], 'e1')
# addlabel(aa10[1], 'e2')
# addlabel(aa10[2], 'e3')
# addlabel(aa10[3], 'e4')
# addlabel(aa10[4], 'e5')
# addlabel(aa10[5], 'e6')

fig.set_figheight(9.5)
fig.set_figwidth(9)
fig.savefig('RSver4.png', dpi=150, bbox_inches='tight')
fig.savefig('RSver4lowres.png', dpi=75, bbox_inches='tight')
 
