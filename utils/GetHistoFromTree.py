'''
Script for producing histograms from TTrees
'''

from ROOT import TFile, TTree, gPad # pylint: disable=import-error,no-name-in-module



TreeFileName=   ['Tree.root','Tree.root','Tree.root','Tree.root','Tree.root','Tree.root','Tree.root','Tree.root','Tree.root','Tree.root','Tree.root','Tree.root']
TreeName=       ['fTreeGen' ,'fTreeGen','fTreeGen','fTreeGen','fTreeGen','fTreeGen' ,'fTreeRec','fTreeRec','fTreeRec','fTreeRec','fTreeGen','fTreeGen']
BranchName=['Config.multiplicity','Config.z','GenHits_1.z','GenHits_1.phi','GenHits_2.z','GenHits_2.phi',
            'RecHits_1.z','RecHits_1.phi','RecHits_2.z','RecHits_2.phi','Config.eta']
Selections=['','','','','','','','','','','','','','']

OutFileDir='Graphs.root'

############################################


outfile=TFile(OutFileDir,'recreate')
outfile.Close()

for idx, (treefile, name, branch, selection) in enumerate(zip(TreeFileName,TreeName,BranchName,Selections)):
    infile = TFile(treefile)
    tree = infile.Get(name)
    
    tree.Draw(branch,selection)

    histo=gPad.GetPrimitive("htemp")
    histo.SetDirectory(0)

    histo.SetName(TreeName[idx]+'_'+BranchName[idx])
    infile.Close()
    
    outfile=TFile(OutFileDir,'update')
    histo.Write(TreeName[idx]+'_'+BranchName[idx])
    outfile.Close()
