#!/usr/bin/env python

import sys, glob, os
from ROOT import TFile, TH1, TH1F, TIter, TKey, Double, TObject, TTree
from ROOT import gStyle,gDirectory,TFile,TF1,TPaveText
from math import fabs, sqrt, pow, log10
import time, datetime
from array import array

def merge_hist(inhist_0="", inhist_list=[], m_hname=""):

  print 'merge_hist: ===== info === '
  print 'final merged hist: ', inhist_0
  print 'source hist      : ', inhist_list

  #if os.path.isfile(inhist_0):
  #  tfin_0=TFile.Open(inhist_0, "UPDATE")
  #else:
  tfin_0=TFile.Open(inhist_0, "RECREATE")

  hist_dict_var = {}
  hist_dict_nom = {}
  for ih, fhist in enumerate(inhist_list):
    print "Look at file: ", fhist
    tfin=TFile.Open(fhist, "READ")

    ## loop inputs
    list_hist=tfin.GetListOfKeys()
    next=TIter(tfin.GetListOfKeys())
    for key in list_hist:
      obj=key.ReadObj()
      if obj.IsA().InheritsFrom(TH1.Class()):
        hname=obj.GetName()

        hist=obj.Clone()
        hist.SetDirectory(0)
        dbin14=[0, 75, 100, 120, 130, 150, 180, 200, 225, 255, 290, 325, 370, 440, 540, 680, 1200, 2000]
        if m_hname=='m4l': hist= hist.Rebin(17, hname, array('d',dbin14))
        #if m_hname=='m4l': hist.Rebin(17, hname, dbin14)
        elif m_hname=='MEM': hist.Rebin(2)

        ## check hist type
        cat, sys, var='', '', ''
        if '-' in hname:
          cat=hname.split('-')[-2] # histogram name (m4l/MEM) with different channel
          var=hname.split('-')[1]  # variation name
          sys=hname.split('-')[-1] # up/down
        else:
          cat='_'.join(hname.split('_')[1:])
          var='Nominal'

        #if hist.GetBinContent(250)==0: print cat, var, sys

        #print "Looking at=> ", cat, var, sys
        if var=='Nominal': 
           if cat not in hist_dict_nom.keys(): 
              hist_dict_nom[cat]=hist
              hist_dict_nom[cat].SetDirectory(0)
           else: 
              hist_dict_nom[cat].Add(hist)
        else:
           if cat not in hist_dict_var.keys(): hist_dict_var[cat]={}
           if var not in hist_dict_var[cat].keys(): hist_dict_var[cat][var]={}
           if sys not in hist_dict_var[cat][var].keys():
              hist_dict_var[cat][var][sys]=hist
              hist_dict_var[cat][var][sys].SetDirectory(0)
           else: hist_dict_var[cat][var][sys].Add(hist)
    tfin.Close()

  hist_dict_ratio = {}
  for cat in hist_dict_var.keys():
     Nbin = hist_dict_nom[cat].GetNbinsX()
     print "Nbin: ", Nbin

     ## Define histogram to save error ratio in different cat
     hname="%s_%s" % (m_hname, cat)
     hist=hist_dict_nom[cat].Clone(hname)
     hist.Reset()
     hist.SetDirectory(tfin_0)
     if cat not in hist_dict_ratio.keys(): hist_dict_ratio[cat]=hist

     ## Then loop bin by bin to calculate the ratio in each bin and save into hists
     for ibin in range(Nbin):
        y_nom = hist_dict_nom[cat].GetBinContent(ibin+1)
        sum_ratio = 0
        for var in hist_dict_var[cat].keys():
           if var=='HOQCD_scale_gg_syst': continue
           max_error = -999.
           for sys in hist_dict_var[cat][var].keys():
              delta_error = fabs(hist_dict_var[cat][var][sys].GetBinContent(ibin+1)-y_nom)
              if max_error<delta_error: max_error = delta_error

           if y_nom==0 or y_nom==max_error: ratio = 0
           else:        ratio = max_error/y_nom
           #if ibin>=58 and cat=='Incl_incl_M4lAll_13TeV' and ratio>=0.9 or ratio<-0.9:
           #   print "Bin: ", ibin, "y_nom: ", y_nom, "sys: ", "max_error: ", max_error, "Ratio: ", ratio, "var: ", var
           sum_ratio += pow(ratio,2)
        sqrt_ratio = sqrt(sum_ratio)
        #if cat=='Incl_incl_M4lAll_13TeV': print "Sum_ratio: ", sum_ratio
        hist_dict_ratio[cat].SetBinContent(ibin+1,sqrt_ratio)

  tfin_0.cd()
  for cat in hist_dict_var.keys():
        hist_dict_ratio[cat].Write()

  tfin_0.Close()
 
if __name__ == "__main__":

  m_hname = "MEM"
  #m_hname = "m4l"
  inhist_list=[]
  samples=["Sh222qqZZ", "Others", "Sh222ggSBI1NLOSBIderiv", "VBFSBI"]
  #samples=["Sh222ggSBI1NLOSBIderiv", "VBFSBI"]
  for samp in samples:
     inhist = "nominal_"+samp+"_"+m_hname+"_hist.root"
     inhist_list.append(inhist)

  outhist = m_hname+"_syst_ratio.root"
  #outhist = "test.root"
  merge_hist(outhist, inhist_list, m_hname) 
