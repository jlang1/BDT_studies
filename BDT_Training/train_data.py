import ROOT
import numpy as np
from array import array





ROOT.TMVA.Tools.Instance()
# read Files
fSig=ROOT.TFile.Open("signal.root","read") # Electron input 
fBkg=ROOT.TFile.Open("background.root","read")     # Proton input


outfileName="BDT_Train.root"
outputFile=ROOT.TFile(outfileName,"RECREATE")
factory=ROOT.TMVA.Factory( outfileName,outputFile,":".join(["!V","!Silent","Color","DrawProgressBar","AnalysisType=Classification"]) )

factory.AddVariable("v0",'F')
factory.AddVariable("v1",'F')
factory.AddVariable("v2",'F')
factory.AddVariable("v3",'F')



# FillFactory
def FillFactory (s):
   print "--- FillFactory              : Filling " + str(s)
  # TStopwatch sw
  # sw.Start()
   issig = 0
   if     ( str(s)=="Signal" ):     issig = 1
   else: 
    if( str(s)=="Background" ): issig = 0
    else:                       return 0

   random = ROOT.TRandom3()

   # input trees		

   if(issig): t = fSig.Get("tree")
   else:      t = fBkg.Get("tree")

   nentries = range(int(t.GetEntries()))
   
   
   print len(nentries)
   maxNTrain = int(len(nentries)/3)
   maxNTest =  int(2*len(nentries)/3)
   ntrain = 0
   ntest = 0
   

   
   
   for iev in nentries:    
      t.GetEntry(iev)

      v=[t.v0,t.v1,t.v2,t.v3]
      
         
      norm=1
      weight=1
      
          
      inp=ROOT.vector('double')()
      for i in range(len(v)):                      
         inp.push_back( v[i] )
      factor = float(norm*weight)
      
      
 
      
      if( ntrain<maxNTrain ): r = random.Uniform(0,1)
      else: r = 0.2
      
      if( ntest>maxNTest ): continue

      if     ( r>0.33 ): 
	factory.AddEvent( str(s), ROOT.TMVA.Types.kTraining, inp, factor )
	ntrain+=1
      else: 
	if( r<0.33 ): 
	  factory.AddEvent( str(s), ROOT.TMVA.Types.kTesting,  inp, factor )
	  ntest+=1

  # sw.Stop();
   print "--- FillFactory              : Train    " + str(ntrain)
   print "--- FillFactory              : Test     " + str(ntest)


   return ntrain
  




if( FillFactory("Signal")<10 ):     print "Number of signal trianing events is low!"
if( FillFactory("Background")<10 ): print "Number of beckground trianing events is low!"

mycuts=ROOT.TCut("1")
mycutb=ROOT.TCut("1")


factory.PrepareTrainingAndTestTree(mycuts,mycutb,":".join(["nTrain_Signal=0","nTest_Signal=0","nTrain_Background=0","nTest_Background=0","SplitMode=Random","NormMode=EqualNumEvents","V","VerboseLevel=Info"]))


# copt="!H:V:NTrees=100:nEventsMin=10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:BoostType=AdaBoost"

factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTMC",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=20","BoostType=Grad"]) )

factory.BookMethod(ROOT.TMVA.Types.kBDT, "ADA",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "150Trees",":".join(["!H","V","NTrees=150","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "125Trees",":".join(["!H","V","NTrees=125","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "75Trees",":".join(["!H","V","NTrees=75","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "50Trees",":".join(["!H","V","NTrees=50","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "D4",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=4","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "D5",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=5","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "D2",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=2","SeparationType=GiniIndex","nCuts=20","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "CUTS_25",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=25","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "CUTS_30",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=30","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "CUTS_15",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=15","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "CUTS_10",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=10","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "CUTS_5",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=5","BoostType=AdaBoost"]) )
#factory.BookMethod(ROOT.TMVA.Types.kBDT, "CUTS_3",":".join(["!H","V","NTrees=100","nEventsMin=10","MaxDepth=3","SeparationType=GiniIndex","nCuts=3","BoostType=AdaBoost"]) )

factory.BookMethod(ROOT.TMVA.Types.kBDT, "C3D2T50",":".join(["!H","V","NTrees=50","nEventsMin=10","MaxDepth=2","SeparationType=GiniIndex","nCuts=3","BoostType=Grad"]) )
factory.BookMethod(ROOT.TMVA.Types.kBDT, "ADAC3D2T75",":".join(["!H","V","NTrees=75","nEventsMin=10","MaxDepth=2","SeparationType=GiniIndex","nCuts=3","BoostType=AdaBoost"]) )
factory.BookMethod(ROOT.TMVA.Types.kBDT, "ADAC3D2T50",":".join(["!H","V","NTrees=50","nEventsMin=10","MaxDepth=2","SeparationType=GiniIndex","nCuts=3","BoostType=AdaBoost"]) )


# train methods
factory.TrainAllMethods()

# test methods
factory.TestAllMethods()

# evaluate methods
factory.EvaluateAllMethods()

# Save the output
outputFile.Close()

print "==> Wrote root file: " + str(outputFile.GetName())
print "==> TMVAClassification is done!"      







