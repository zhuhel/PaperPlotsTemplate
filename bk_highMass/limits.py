import array, atlas, pickle, sys, utils
import ROOT

def main():
  
  ROOT.gROOT.SetBatch()

  line_width = 3

  limits = [ 
    ( 'res_NWA_ggF.root', utils.ggfs, 'ggF production' ),  
    ( 'res_NWA_VBF.root', utils.vbfs, 'VBF production' ),  
    ( 'llvv_LWA_wH1.root', utils.ggfs,  'LWA, #it{#Gamma_{H}} = 0.01 #times #it{m_{H}}' ),  
    ( 'llvv_LWA_wH5.root', utils.ggfs,  'LWA, #it{#Gamma_{H}} = 0.05 #times #it{m_{H}}' ),  
    ( 'llvv_LWA_wH10.root', utils.ggfs,  'LWA, #it{#Gamma_{H}} = 0.1 #times #it{m_{H}}' ),  
  ]
  
  for file_name, y_axis_title, prod_mode in limits:
    file = ROOT.TFile( 'inputs/' + file_name )
    exp_4l = file.Get( 'canvas2' ).GetPrimitive( 'Graph4' )
    exp_4l.SetLineStyle( 7 )
    exp_4l.SetLineWidth( line_width )
    exp_4l.SetLineColor( ROOT.kAzure + 2 )
    exp_4l.SetMarkerColor( ROOT.kAzure + 2 )
    exp_2l2v = file.Get( 'canvas2' ).GetPrimitive( 'Graph6' )
    exp_2l2v.SetLineStyle( 3 )
    exp_2l2v.SetLineWidth( line_width + 1 )
    exp_2l2v.SetLineColor( ROOT.kOrange + 10 )
    exp_2l2v.SetMarkerColor( ROOT.kOrange + 10 )
    exp_comb = file.Get( 'canvas2' ).GetPrimitive( 'Graph2' )
    exp_comb.SetLineStyle( 2 )
    exp_comb.SetLineWidth( line_width )
    exp_comb.SetLineColor( ROOT.kBlack )
    exp_comb.SetMarkerColor( ROOT.kBlack )
    obs_comb = file.Get( 'canvas2' ).GetPrimitive( 'Graph3' )
    obs_comb.SetLineStyle( 1 )
    obs_comb.SetLineWidth( line_width )
    obs_comb.SetLineColor( ROOT.kBlack )
    obs_comb.SetMarkerColor( ROOT.kBlack )
    obs_comb.SetMarkerSize( 1 )
    band_1 = file.Get( 'canvas2' ).GetPrimitive( 'Graph1' )
    band_1.SetFillColor( 3 )
    band_2 = file.Get( 'canvas2' ).GetPrimitive( 'Graph0' )
    band_2.SetFillColor( 5 )
    canvas = ROOT.TCanvas( 'plot_' + file_name.replace( '.root', '' ), '', 800, 600 )
    band_2.Draw( 'a3' )
    if 'LWA' in prod_mode:
      band_2.GetXaxis().SetRangeUser( 400, 1000 )
      band_2.GetYaxis().SetRangeUser( 0.005, 1.5 )
    else:
      band_2.GetXaxis().SetRangeUser( 200, 1200 )
      band_2.GetYaxis().SetRangeUser( 0.005, 10 )
    band_2.GetXaxis().SetTitle( '#it{m_{H}} [GeV]' )
    band_2.GetYaxis().SetTitle( '95% C.L. limit on ' + y_axis_title + ' [pb]' )
    band_2 = utils.re_style( band_2 )
    band_1.Draw( '3' )
    exp_4l.Draw( 'l' )
    exp_2l2v.Draw( 'l' )
    exp_comb.Draw( 'l' )
    obs_comb.Draw( 'pl' )
    x_l1, y_l1, latex1 = utils.draw_latex( utils.lumi, False )
    latex1.DrawLatex( x_l1, y_l1 - 0.105, utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + utils.lepm + ' + ' + utils.lepp + utils.lepm + utils.nu + utils.nubar )
    latex1.DrawLatex( x_l1, y_l1 - 0.16, prod_mode )
    xLeg = 0.62
    yLeg = 0.89
    leg = utils.create_legend_limit( 6 ) 
    utils.print_details( obs_comb )
    leg.AddEntry( obs_comb, 'Observed ' + utils.cls + ' limit', 'pl' )
    leg.AddEntry( exp_comb, 'Expected ' + utils.cls + ' limit', 'l' )
    leg.AddEntry( band_1,   'Expected #pm 1#sigma', 'f' )
    leg.AddEntry( band_2,   'Expected #pm 2#sigma', 'f' )
    leg.AddEntry( exp_4l,   'Expected ' + utils.cls + ' limit (' + utils.lepp + utils.lepm + utils.lepp + utils.lepm + ')', 'l' )
    leg.AddEntry( exp_2l2v, 'Expected ' + utils.cls + ' limit (' + utils.lepp + utils.lepm + utils.nu + utils.nubar + ')', 'l' )
    #leg.AddEntry( exp_4l,   'Expected ' + utils.cls + ' limit', 'l' )
    #leg.AddEntry( exp_2l2v, 'Expected ' + utils.cls + ' limit', 'l' )
    leg.Draw()
    ROOT.gPad.RedrawAxis()
    #utils.patch_bar( 292. / 566., 298. / 566., 327. / 407., 327. / 407., True ) 
    canvas.SetLogy()
    utils.save( canvas )

if __name__ == '__main__':
  sys.exit( main() )
