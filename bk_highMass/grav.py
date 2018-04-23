import array, atlas, pickle, sys, utils
import ROOT

def main():
  
  ROOT.gROOT.SetBatch()

  line_width = 2

  file = ROOT.TFile( 'inputs/graphs_llvv_graviton.root' )
  exp = file.Get( 'median' )
  exp.SetLineStyle( 2 )
  exp.SetLineWidth( line_width )
  exp.SetLineColor( ROOT.kBlack )
  exp.SetMarkerColor( ROOT.kBlack )
  obs = file.Get( 'observed' )
  obs.SetLineStyle( 1 )
  obs.SetLineWidth( line_width )
  obs.SetLineColor( ROOT.kBlack )
  obs.SetMarkerColor( ROOT.kBlack )
  obs.SetMarkerSize( 0.8 )
  theory = file.Get( 'sm' )
  #for i in range( 2 ):
  #  theory.RemovePoint( 0 )
  theory.SetLineStyle( 1 )
  theory.SetLineWidth( line_width )
  theory.SetLineColor( ROOT.kRed + 1 )
  theory.SetMarkerColor( ROOT.kRed )
  band_1 = file.Get( '1sigma' )
  band_1.SetFillColor( 3 )
  band_1.SetFillStyle( 1001 )
  band_2 = file.Get( '2sigma' )
  band_2.SetFillColor( 5 )
  band_2.SetFillStyle( 1001 )
  canvas = ROOT.TCanvas( 'plot_graviton', '', 800, 600 )
  band_2.Draw( 'af' )
  #band_2.GetYaxis().SetRangeUser( 1, 100000 )
  band_2.GetYaxis().SetRangeUser( 1, 30000 )
  band_2.GetXaxis().SetTitle( '#it{m(G_{#it{KK}})} [TeV]' )
  band_2.GetYaxis().SetTitle( '95% C.L. limit on ' + utils.grav_axis + '  [fb]' )
  band_2 = utils.re_style( band_2 )
  band_1.Draw( 'f' )
  exp.Draw( 'l' )
  obs.Draw( 'pl' )
  theory.Draw( 'l' )
  band_2.GetXaxis().SetRangeUser( 600, 2 )
  box = utils.get_box( 500, 1000, 200, 500 )
  box.Draw()
  x_l1, y_l1, latex1 = utils.draw_latex( utils.lumi, False )
  latex1.DrawLatex( x_l1, y_l1 - 0.105, utils.g_to_zz_to + utils.lepp + utils.lepm + utils.nu + utils.nubar )
  latex1.DrawLatex( x_l1, y_l1 - 0.16, '#it{k/#bar{M}_{Pl}} = 1' )
  xLeg = 0.62
  yLeg = 0.89
  leg = utils.create_legend_limit( 5 ) 
  leg.AddEntry( obs,    'Observed ' + utils.cls + ' limit', 'pl' )
  leg.AddEntry( exp,    'Expected ' + utils.cls + ' limit', 'l' )
  leg.AddEntry( band_1, 'Expected #pm 1#sigma', 'f' )
  leg.AddEntry( band_2, 'Expected #pm 2#sigma', 'f' )
  leg.AddEntry( theory, utils.grav_axis, 'l' )
  leg.Draw()
  #utils.patch_bar( 240. / 566., 247. / 566., 329. / 407., 329. / 407., True ) 
  canvas.SetLogy()
  utils.save( canvas )

if __name__ == '__main__':
  sys.exit( main() )
