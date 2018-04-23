import array, atlas, pickle, sys, utils
import ROOT

def main():
  
  ROOT.gSystem.Load( 'libRooFit' )
  ROOT.gROOT.SetBatch()
  ROOT.gErrorIgnoreLevel = 0
  ROOT.RooMsgService.instance().setGlobalKillBelow( ROOT.RooFit.ERROR )

  mass_files = {
    200:  'inputs/mc15_13TeV.341274.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH200NW_ZZ4lep.root',
    300:  'inputs/mc15_13TeV.341275.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH300NW_ZZ4lep.root',
    400:  'inputs/mc15_13TeV.341276.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH400NW_ZZ4lep.root',
    500:  'inputs/mc15_13TeV.341277.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH500NW_ZZ4lep.root',
    600:  'inputs/mc15_13TeV.341278.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH600NW_ZZ4lep.root',
    700:  'inputs/mc15_13TeV.341279.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH700NW_ZZ4lep.root',
    800:  'inputs/mc15_13TeV.341280.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH800NW_ZZ4lep.root',
    900:  'inputs/mc15_13TeV.341281.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH900NW_ZZ4lep.root',
    1000: 'inputs/mc15_13TeV.341282.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH1000NW_ZZ4lep.root',
    1200: 'inputs/mc15_13TeV.341283.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH1200NW_ZZ4lep.root',
    1400: 'inputs/mc15_13TeV.341284.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH1400NW_ZZ4lep.root',
    #1600: '/eos/atlas/atlascerngroupdisk/phys-higgs/HSG2/H4l/2016/MiniTrees/Prod_v10/mc/Nominal/mc15_13TeV.341285.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH1600NW_ZZ4lep.root',
  }


  f = ROOT.TFile( 'inputs/workspace_36fb_NWA_WithVBF.root' )
  w = f.Get( 'combined' )
  my_mass = w.var( 'm4l' ) 
  higgs_mass = w.var( 'mH' ) 

  channels = [ '4mu', '2mu2e', '4e' ]
  colors = { '4mu': ROOT.kAzure + 6, '2mu2e': ROOT.kAzure + 3, '4e': ROOT.kSpring - 5 }
  cuts = { '4mu': ( 0, 0 ), '2mu2e': ( 2, 3 ), '4e': ( 1, 1 ) }
  lines = { '4mu': 1, '2mu2e': 2, '4e': 4 }
  markers = { '4mu': 20, '2mu2e': 21, '4e': 22 }
  titles = { '4mu': utils.mup + utils.mum + utils.mup + utils.mum, '2mu2e': utils.mup + utils.mum + utils.ep + utils.em + ' + ' + utils.ep + utils.em + utils.mup + utils.mum, '4e': utils.ep + utils.em + utils.ep + utils.em }
  all_hists = {}
  graphs = {}
  strategy = 'RMS+'
  #strategy = ''

  #out = ROOT.TFile( 'out.root', 'recreate' )

  masses = [ mass for mass in mass_files ]
  masses = sorted( masses )

  canvas = ROOT.TCanvas( 'plot_reso', '', 800, 600 )
  for ch in channels:
    all_hists[ ch ] = {}
    graphs[ ch ] = ROOT.TGraphErrors( len( mass_files ) )
    for index, mass in enumerate( masses ):
      if 'RMS' in strategy:
        File = ROOT.TFile( mass_files[ mass ] )
        Tree = File.Get( 'tree_incl_all' ) 
        all_hists[ ch ][ mass ] = ROOT.TH1F( 'hist_%s_%d' % ( ch, mass ), '', 100, 0.8 * mass , 1.2 * mass )
        #all_hists[ ch ][ mass ] = ROOT.TH1F( 'hist_%s_%d' % ( ch, mass ), '', 1500, 100, 1600 )
        all_hists[ ch ][ mass ].SetDirectory( 0 ) 
        for entry in Tree:
          if entry.pass_vtx4lCut != 1: continue
          if entry.event_type == cuts[ ch ][ 0 ] or entry.event_type == cuts[ ch ][ 1 ]:
            all_hists[ ch ][ mass ].Fill( entry.m4l_constrained_HM )#, entry.weight )
        graphs[ ch ].SetPoint( index, mass, all_hists[ ch ][ mass ].GetRMS() )
        graphs[ ch ].SetPointError( index, 0, all_hists[ ch ][ mass ].GetRMSError() )
        #print all_hists[ ch ][ mass ].GetRMS(), ' +/- ', all_hists[ ch ][ mass ].GetRMSError() 
      else:
        pdf =  w.pdf( 'ATLAS_Signal_ggF_ggF_%s_13TeV_cbga' % ch )
        higgs_mass.setVal( mass )
        data = pdf.generateBinned( ROOT.RooArgSet( my_mass ), 1000000 )
        all_hists[ ch ][ mass ] = data.createHistogram( 'm4l', 100 )
        graphs[ ch ].SetPoint( index, mass, all_hists[ ch ][ mass ].GetRMS() )
        graphs[ ch ].SetPointError( index, 0, all_hists[ ch ][ mass ].GetRMSError() )
        #print mass_val, hist.GetRMS()
        
      #out.cd()
      #all_hists[ ch ][ mass ].Write()

  funcs = {}
  for index, ch in enumerate( channels ):
    #graphs[ ch ].SetLineColor( colors[ ch ] )
    #graphs[ ch ].SetMarkerColor( colors[ ch ] )
    graphs[ ch ].SetLineColor( ROOT.kWhite ) 
    graphs[ ch ].SetMarkerColor( ROOT.kWhite )  
    graphs[ ch ].SetMarkerStyle( 1 )
    graphs[ ch ].SetLineWidth( 1 )
    funcs[ ch ] = ROOT.TF1( 'function_%s' % ch, 'pol2', 200, 1400 )
    funcs[ ch ].SetLineColor( colors[ ch ] )
    funcs[ ch ].SetLineWidth( 3 )
    funcs[ ch ].SetLineStyle( lines[ ch ] )
    #out.cd()
    #graphs[ ch ].Write()
    if index == 0:
      graphs[ ch ].Draw( 'apec' )
      graphs[ ch ].Fit( 'function_%s' % ch )
      graphs[ ch ].GetXaxis().SetTitle( '#it{m_{H}} [GeV]' )
      graphs[ ch ].GetYaxis().SetTitle( 'RMS of ' + utils.m4lonly + ' distribution [GeV]' ) 
      graphs[ ch ].GetXaxis().SetRangeUser( 200, 1400 )
      graphs[ ch ].GetYaxis().SetRangeUser( 0, 70 )
      graphs[ ch ] = utils.re_style( graphs[ ch ] )
    else:
      graphs[ ch ].Fit( 'function_%s' % ch )
      graphs[ ch ].Draw( 'pec' )
    
  if '+' in strategy:
    for index, ch in enumerate( channels ):
      if index == 0:
        graphs[ ch ].Draw( 'ap' )
        funcs[ ch ].Draw( 'l same' )
      else:
        funcs[ ch ].Draw( 'l same' )

  x_l1, y_l1, latex1 = utils.draw_latex( None, False )
  latex1.DrawLatex( x_l1, y_l1 - 0.105, utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + utils.lepm )
  xLeg = x_l1
  yLeg = y_l1 - 0.2
  leg = ROOT.TLegend( xLeg, yLeg - 0.24, xLeg + 0.3, yLeg )
  leg.SetFillStyle( 0 )
  leg.SetBorderSize( 0 )
  leg.SetTextFont( 42 )
  leg.SetTextSize( 0.036 )
  for index, ch in enumerate( channels ):
    leg.AddEntry( funcs[ ch ], titles[ ch ], 'l' )
  leg.Draw()
  utils.save( canvas )
  #out.Close()

if __name__ == '__main__':
  sys.exit( main() )
