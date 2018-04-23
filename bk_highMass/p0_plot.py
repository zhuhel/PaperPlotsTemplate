import array, atlas, pickle, sys, utils
import ROOT

def main():
  
  ROOT.gROOT.SetBatch()

  line_width = 2

  file = ROOT.TFile( 'inputs/p0_NWA_graphs.root' )
  p0_4l = file.Get( 'p0_4l' ) 
  p0_4l.SetLineStyle( 7 )
  p0_4l.SetLineWidth( line_width )
  p0_4l.SetLineColor( ROOT.kAzure + 2 )
  p0_4l.SetMarkerColor( ROOT.kAzure + 2 )
  p0_2l2v = file.Get( 'p0_llvv' )
  p0_2l2v.SetLineStyle( 3 )
  p0_2l2v.SetLineWidth( line_width )
  p0_2l2v.SetLineColor( ROOT.kOrange + 10 )
  p0_2l2v.SetMarkerColor( ROOT.kOrange + 10 )
  p0_comb = file.Get( 'p0_comb' )
  p0_comb.SetLineStyle( 1 )
  p0_comb.SetLineWidth( line_width )
  p0_comb.SetLineColor( ROOT.kBlack )
  p0_comb.SetMarkerColor( ROOT.kBlack )
  canvas = ROOT.TCanvas( 'plot_p0', '', 800, 600 )
  p0_4l.Draw( 'ac' )
  minX, maxX = 200, 1200
  p0_4l.GetXaxis().SetRangeUser( minX, maxX )
  p0_4l.GetYaxis().SetRangeUser( 0.000001, 1.5 )
  p0_4l.GetXaxis().SetTitle( '#it{m_{H}} [GeV]' )
  p0_4l.GetYaxis().SetTitle( 'Local #it{p}_{0}' )
  p0_4l = utils.re_style( p0_4l )
  #lines_y = [ 0.5, 0.1586553, 0.02275013, 0.001349898 ]
  lines_y = [ 0.1586553, 0.02275013, 0.001349898, 0.000063342484 * .5 ]
  loc_line = {}
  loc_tex = {}
  for index, line_y in enumerate( lines_y ):
    loc_line[ index ] = ROOT.TLine( minX, line_y, maxX, line_y )
    loc_line[ index ].SetLineColor( 15 )
    loc_line[ index ].SetLineStyle( 5 )
    loc_line[ index ].SetLineWidth( 2 )
    loc_line[ index ].Draw()
    loc_tex[ index ] = ROOT.TLatex( maxX * 1.01, line_y, '%d#sigma' % ( index + 1 ) )
    loc_tex[ index ].SetTextColor(15)
    loc_tex[ index ].SetTextFont(42)
    loc_tex[ index ].SetTextSize(0.03)
    loc_tex[ index ].SetTextAlign(12)
    loc_tex[ index ].Draw()
  p0_2l2v.Draw( 'c' )
  p0_comb.Draw( 'c' )
  x_l1, y_l1, latex1 = utils.draw_latex( utils.lumi, False, 0.05, -0.46 )
  latex1.DrawLatex( x_l1, y_l1 - 0.115, utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + utils.lepm + ' + ' + utils.lepp + utils.lepm + utils.nu + utils.nubar )
  latex1.DrawLatex( x_l1, y_l1 - 0.17, 'NWA' )
  latex1.SetTextSize( 17 )
  latex1.DrawLatex( 0.6, 0.68, 'Global significance for' )
  latex1.DrawLatex( 0.6, 0.63, 'largest excess (' + utils.lepp + utils.lepm + utils.lepp + utils.lepm + '): 2.2#sigma' )
  xLeg = 0.62
  yLeg = 0.89
  leg = utils.create_legend_limit( 3, 0.1, -0.48 ) 
  leg.AddEntry( p0_4l, utils.lepp + utils.lepm + utils.lepp + utils.lepm, 'l' )
  leg.AddEntry( p0_2l2v, utils.lepp + utils.lepm + utils.nu + utils.nubar, 'l' )
  leg.AddEntry( p0_comb, 'Combined', 'l' )
  leg.Draw()
  #utils.patch_bar( 321. / 566., 326. / 566., 140. / 407., 140. / 407., True ) 
  #utils.patch_bar( 443. / 566., 448. / 566., 137. / 407., 137. / 407., True ) 
  canvas.SetLogy()
  utils.save( canvas )

if __name__ == '__main__':
  sys.exit( main() )
