import array, atlas, pickle, sys, utils
import ROOT

def main():
  
  ROOT.gSystem.Load( 'libRooFit' )
  ROOT.gROOT.SetBatch()
  ROOT.gErrorIgnoreLevel = 0
  ROOT.RooMsgService.instance().setGlobalKillBelow( ROOT.RooFit.ERROR )

  f = ROOT.TFile( 'inputs/workspace_36fb_NWA_WithVBF.root' )
  w = f.Get( 'combined' )

  n_points = 10
  min_mass = 300
  max_mass = 900
  step = ( max_mass - min_mass ) / float( n_points )
  colors = utils.init_colors( n_points + 1 )


  files = {
    300: 'inputs/mc15_13TeV.341275.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH300NW_ZZ4lep.root',
    600: 'inputs/mc15_13TeV.341278.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH600NW_ZZ4lep.root',
    900: 'inputs/mc15_13TeV.341281.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH900NW_ZZ4lep.root',
  }

  channels = [ '2mu2e' ] #[ '4mu', '2mu2e', '4e' ]
  titles = { '4mu': '4#it{#mu}', '2mu2e': utils.mup + utils.mum + utils.ep + utils.em + ' + ' + utils.ep + utils.em + utils.mup + utils.mum, '4e': '4#it{e}' }
  cuts = { '4mu': ( 0, 0 ), '2mu2e': ( 2, 3 ), '4e': ( 1, 1 ) }
  #utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + '\'' + utils.lepm + '\''

  for ch in channels:

    hist = {}
    canvas = ROOT.TCanvas( 'plot_shape_%s' % ch, '', 800, 600 )

    for the_mass in files: 
      hist[ the_mass ] = ROOT.TH1F( 'hist%d%s' % ( the_mass, ch ), '', 160, 200, 1000 )
      hist[ the_mass ].SetDirectory( 0 )
      temp_file = ROOT.TFile( files[ the_mass ] )
      temp_tree = temp_file.Get( 'tree_incl_all' )
      for entry in temp_tree:
        if entry.pass_vtx4lCut != 1: continue
        if entry.event_type == cuts[ ch ][ 0 ] or entry.event_type == cuts[ ch ][ 1 ]:
          hist[ the_mass ].Fill( entry.m4l_constrained_HM, entry.weight )

    mass = w.var( 'm4l' ) 
    higgs_mass = w.var( 'mH' ) 
    Frame = utils.re_style( mass.frame() )

    data = {}
    for index in range( n_points + 1 ):
      mass_val = min_mass + index * step
      higgs_mass.setVal( mass_val )
      if mass_val in files:
        hist[ mass_val ].Scale( 1. / hist[ mass_val ].Integral(), 'width' )
        data[ mass_val ] = ROOT.RooDataHist( 'data%d' % mass_val, '', ROOT.RooArgList( mass ), ROOT.RooFit.Import( hist[ mass_val ] ) )
        data[ mass_val ].plotOn( Frame, ROOT.RooFit.LineColor( colors[ index ] ), ROOT.RooFit.MarkerColor( colors[ index ] ) )

    pdf =  w.pdf( 'ATLAS_Signal_ggF_ggF_%s_13TeV_cbga' % ch )
    for index in range( n_points + 1 ):
      mass_val = min_mass + index * step
      higgs_mass.setVal( mass_val )
      #if index % 5 == 0:
      #  pdf.plotOn( Frame, ROOT.RooFit.LineColor( colors[ index ] ), ROOT.RooFit.LineWidth( 2 ), ROOT.RooFit.Precision( 0.0001 ) )
      #else:
      pdf.plotOn( Frame, ROOT.RooFit.LineColor( colors[ index ] ), ROOT.RooFit.LineWidth( 2 ), ROOT.RooFit.Precision( 0.0001 ), ROOT.RooFit.LineStyle( 2 ) )

    norm_values = {}
    for index in range( n_points + 1 ):
      mass_val = min_mass + index * step
      higgs_mass.setVal( mass_val )
      norm_values[ mass_val ] = pdf.getValV( ROOT.RooArgSet( mass ) ) 

    Frame.Draw()
    Frame.GetXaxis().SetRangeUser( 200, 1000 )
    Frame.GetXaxis().SetTitle( utils.m4l )
    Frame.GetYaxis().SetTitle( 'Arbitrary Units' )
    Frame.GetYaxis().SetRangeUser( 0.0004, 0.6 )
    x_l1, y_l1, latex1 = utils.draw_latex( None, False )
    latex1.DrawLatex( x_l1, y_l1 - 0.105, titles[ ch ] )
    xLeg = 0.6
    yLeg = 0.89
    leg = ROOT.TLegend( xLeg, yLeg - 0.18, xLeg + 0.3, yLeg )
    leg.SetFillStyle( 0 )
    leg.SetBorderSize( 0 )
    leg.SetTextFont( 42 )
    leg.SetTextSize( 0.032 )
    Marker = ROOT.TH1F( 'Marker', 'I am a fake histogram', 100, 0, 100 )
    Marker.SetMarkerColor( ROOT.kGray + 2 )
    Line = ROOT.TH1F( 'Line', 'I am a fake histogram', 100, 0, 100 )
    Line.SetLineColor( ROOT.kGray + 2 )
    Line.SetLineStyle( 2 )
    leg.AddEntry( Marker, 'Simulation', 'p' )
    leg.AddEntry( Line, 'Parametrization', 'l' )
    leg.Draw()
    canvas.SetLogy()
    utils.save( canvas )

if __name__ == '__main__':
  sys.exit( main() )
