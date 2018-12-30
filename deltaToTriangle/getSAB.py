import sys
sys.path.append('NJOY_LEAPR/')
from generateNjoyInput import *
from makeTest09Rho import *




def getLine(f):
    return [float(num) for num in f.readline().split()]



def getSAB(alphas,betas,rho,NJOY_LEAPR,fullRedo,width,oscE=None,oscW=None):
    # alpha, beta, rho = vecs of alphas, betas, rhos
    # NJOY_LEAPR = bool : true if we want to use NJOY leapr, false if we want 
    #              to use mine
    # fullRedo : bool = do you want to generate leapr again? 
    # width of triangle. if None, then we treat it as a delta function
    if NJOY_LEAPR:
        # Run NJOY LEAPR
        name = 'Delta' if width == None else 'Contin'
        if fullRedo:
            # Generate S(a,b) using delta functions OR 
            # Generate S(a,b) by approximating delta functions as a very thin triangle
            rho = continRho if width == None else getPhononDist(width,continRho)
            generateNjoyInput(name,alphas,betas,rho,width == None)
            runNJOY(name)

        with open('NJOY_LEAPR/sabResults/sab_'+name+'.txt','r') as f:
            sab = getLine(f)
            alphaVals = getLine(f)
            betaVals  = getLine(f)
            assert(alphaVals == alphas)
            assert(betaVals == betas)
        return sab


    else:
        # Run my own LEAPR
        name = 'sab_Delta.txt' if width == None else 'sab_Contin.txt'
        if fullRedo:
            if width == None:
                assert(oscE != None and oscW != None)
                writeRho('inputVals.txt',continRho,alphas,betas,oscE,oscW)
                subprocess.run(['g++','-std=c++14','./MY_LEAPR/deltaFuncLEAPR.cpp'])
                subprocess.run(['./a.out'])
                subprocess.run(['mv','inputVals.txt','./MY_LEAPR/alphaBetaRhoInputs/'+name])
                subprocess.run(['mv','outputSAB.txt','./MY_LEAPR/sabResults/'+name])

            else:
                assert(oscE != None and oscW != None)
                writeRho('inputVals.txt',getPhononDist(width,continRho),alphas,betas,[],[])
                subprocess.run(['g++','-std=c++14','./MY_LEAPR/deltaFuncLEAPR.cpp'])
                subprocess.run(['./a.out'])
                subprocess.run(['mv','inputVals.txt','./MY_LEAPR/alphaBetaRhoInputs/'+name])
                subprocess.run(['mv','outputSAB.txt','./MY_LEAPR/sabResults/'+name])

        with open('MY_LEAPR/sabResults/'+name,'r') as f:
            sab = getLine(f)

        return sab










alphas = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7 ]
betas = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.6, 7.7, 7.8, 7.9, 8, 8.05, 8.1, 8.15, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 9, 10, 12, 14, 16, 18, 20]
continRho = [0, .0005, .001, .002, .0035, .005, .0075, .01, .013, .0165, .02,  \
  .0245, .029, .034, .0395, .045, .0506, .0562, .0622, .0686, .075, .083, .091,\
  .099, .107, .115, .1197, .1214, .1218, .1195, .1125, .1065, .1005, .09542,   \
  .09126, .0871, .0839, .0807, .07798, .07574, .0735, .07162, .06974, .06804,  \
  .06652, .065, .0634, .0618, .06022, .05866, .0571, .05586, .05462, .0535,    \
  .0525, .0515, .05042, .04934, .04822, .04706, .0459, .04478, .04366, .04288, \
  .04244, .042, 0.0]

oscE = [ 0.204,    0.4794   ] 
oscW = [ 0.166667, 0.333333 ]


fullRedo = False
width = None 
#NJOY_LEAPR = False
MY_DELTA_SAB = getSAB(alphas,betas,continRho,NJOY_LEAPR=False,fullRedo=fullRedo,width=width,oscE=oscE,oscW=oscW)
NJOY_DELTA_SAB = getSAB(alphas,betas,continRho,NJOY_LEAPR=True,fullRedo=fullRedo,width=width,oscE=oscE,oscW=oscW)




from plotSAB_help import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


A0 = 18.02
E = 0.01 
kbT = 0.025851

cnorm = colors.Normalize(vmin=0,vmax=len(alphas)+3)
scalarMap = cmx.ScalarMappable(norm=cnorm,cmap=plt.get_cmap('hot')) #hot autumn tab10
mymap = colors.LinearSegmentedColormap.from_list('funTestColors',\
        [scalarMap.to_rgba(a) for a in range(len(alphas))])
colorBar = plt.contourf([[0,0],[0,0]], alphas, cmap=mymap)
plt.clf()

#print(sabDELTA)

#plotBetaForVariousAlpha(alphas,betas,MY_DELTA_SAB,A0,E,kbT,scalarMap,'.',False)
#plotBetaForVariousAlpha(alphas,betas,NJOY_DELTA_SAB,A0,E,kbT,scalarMap,'.',True)
plotErrorBetaForVariousAlpha(alphas,betas,MY_DELTA_SAB,NJOY_DELTA_SAB,A0,E,kbT,scalarMap)


ax = plt.gca()
cb = plt.colorbar(colorBar) # using the colorbar info I got from contourf
cb.ax.set_ylabel('alpha values')
plt.title('S(a,b) values for water, generated with and without delta funcs')
#plt.title('Relative difference between S(a,b) generated with and without delta funcs')
ax.set_facecolor('xkcd:off white')
ax.set_facecolor('xkcd:light grey blue')
plt.show()





