import ROOT
from array import array
import numpy as np




numDataPoints=int(input("wie viele Datenpunkte? "))

random=ROOT.TRandom3()
  
for i in range(2):
  if (i==0):
    outs="signal_corr.root"
    ofiles=ROOT.TFile(outs,"RECREATE")
  else:
    outb="background_corr.root"
    ofileb=ROOT.TFile(outb,"RECREATE")

  v1=array('f',[0])
  v2=array('f',[0])
  v3=array('f',[0])
  v4=array('f',[0])
  #v5=array('f',[0])
  #v6=array('f',[0])
  #v7=array('f',[0])
  #v8=array('f',[0])
  #v9=array('f',[0])
  #v10=array('f',[0])
  
  v=[v1,v2,v3,v4]#,v5,v6,v7,v8,v9,v10]
  
  
  tree=ROOT.TTree("tree","Train N-Tuple")
  
  for j in range(len(v)):
    branchname="v"+str(j)
    ft=branchname + "/F"
    tree.Branch(branchname,v[j],ft)
    
  if (i==0):
    for k in range (numDataPoints):
      v[0][0]=2*(1+pow(np.sin(random.Gaus(9.,0.5)-random.Uniform(0,0.2)),3))+random.Uniform(-0.4,0.5)
      v[1][0]=(4-np.exp(random.Gaus(1,0.5)))*np.sin(random.Uniform(-np.pi+1,np.pi-1))
      v[2][0]=(random.Gaus(2,1)+random.Gaus(0.6,0.5))
      v[3][0]=(np.exp(random.Uniform(0.5,0.75)+random.Gaus(0.1,0.01)))    
      tree.Fill()
  else:
    for k in range (numDataPoints):
      v[0][0]=2*(1+pow(np.sin(random.Gaus(9.,0.5)+random.Uniform(0,0.2)),3))+random.Uniform(-0.5,0.4)
      v[1][0]=(4-np.exp(random.Gaus(1,0.5)))*np.sin(random.Uniform(-np.pi-1,np.pi+1))
      v[2][0]=random.Gaus(2,1)-random.Gaus(0.5,0.5)
      v[3][0]=np.exp(random.Uniform(0.5,0.75)-random.Gaus(0.1,0.01))
      tree.Fill()
  if (i==0):
    ofiles.Write()
    ofiles.Close()
  else:
    ofileb.Write()
    ofileb.Close()
  
