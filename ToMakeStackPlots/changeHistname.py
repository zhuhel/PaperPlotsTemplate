#!/usr/bin/python

import sys

from ROOT import gStyle,gDirectory,TCanvas,TPad,TFile,TH1F,TF1,TLegend,TPaveText
from math import sqrt, pow
import os.path

def merge_sbi5(outfname="", mvar=""):
   
   list_sbi5=["Others", "Sh222qqZZ", "Sh222ggSBI5NLOSBIderiv", "VBFSBI5"]
   chs=["2mu2e", "4e", "4mu", "incl"]
   
   hist_dict={}
   fout=TFile(outfname, "recreate")
   scale=1.0
   sggZZ=1.2
   for samp in list_sbi5:
      if samp=="Sh222ggSBI5NLOSBIderiv": scale=sggZZ
      filename="nominal_"+samp+"_"+mvar+"_hist.root"
      print "Merging the sample=> ", filename
      tfin=TFile.Open(filename)
      for ch in chs:
         hname=mvar+"_Incl_"+ch+"_M4lAll_13TeV"
         hin=tfin.Get(hname)
         if not hin:
           print 'Error=> could not find hist %s in %s' %( hname, filename)
         if ch not in hist_dict.keys(): 
            hist_dict[ch]=hin.Clone()
            hist_dict[ch].SetDirectory(fout)
         else: hist_dict[ch].Add(hin, scale)

   fout.cd()
   for ch in chs:
      hist_dict[ch].Write()
   fout.Close()


def change_histname(mvar=""):

   samples=["data", "Sh222qqZZ", "Others", "Sh222ggSBI1NLOSBIderiv", "VBFSBI", "SBI5all"]
   #samples=["data"]
   chs=["2mu2e", "4e", "4mu", "incl"]

   for samp in samples:
      filename="nominal_"+samp+"_"+mvar+"_hist.root"
      print "Looking at=> ", filename
      tfin=TFile.Open(filename)
      fout=TFile("dup_"+filename, "recreate")
      for ch in chs:
         hname=mvar+"_Incl_"+ch+"_M4lAll_13TeV"
         hin=tfin.Get(hname)
         if not hin:
           print 'Error=> could not find hist %s in %s' %( hname, filename)

         hout=hin.Clone()
         outname=samp+"_"+hname
         hout.SetName(outname)
         hout.SetTitle(outname)
         hout.Write()
      fout.Close()
   return 1

if __name__=="__main__":

   mvar="MEM"
   #mvar="m4l"
   outfname="nominal_SBI5all_"+mvar+"_hist.root"

   if os.path.isfile(outfname):
      print "File %s exist! Skip merging SBI5 files" %(outfname)
   else:
      merge_sbi5(outfname, mvar)
   change_histname(mvar)
