import array, atlas, csv, math, os, pickle, sys, utils
import ROOT

def main():
  
  ### Main definitions
  ROOT.gROOT.SetBatch()
  ###
  canvas, c_top, c_bottom = utils.create_double_pad( 'plot_emucr_2l2v' )
  ###
  root_file = ROOT.TFile( 'inputs/M2LEP_em_met_tst.root' )
  stack = utils.re_style_top( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'hs1' ) )
  stack.GetXaxis().SetTitle( '#it{E}_{T}^{miss} [GeV]' )
  stack.GetYaxis().SetTitle( 'Events / 30 GeV' )
  hists = {} 
  merging_scheme = utils.complex_merging
  for hist in stack.GetHists():
    prev_color = hist.GetFillColor()
    sample_name = None
    for key, vals in utils.original_colors_2l2v.iteritems():
      if prev_color in vals:
        sample_name = key
    '''
    if not sample_name:
      'Sample Name Not Found'
    else:
      hist.SetFillColor( utils.get_colors( sample_name ) ) 
      #hist.SetLineColor( utils.colors[ sample_name ] ) 
      hist.SetLineColor( ROOT.kBlack ) 
      hist.SetLineWidth( 1 ) 
      hist.SetTitle( utils.titles[ sample_name ] ) 
    '''
    hists[ sample_name ] = hist
  ### Getting complicated here...
  loop_over_this = hists.keys()
  to_be_removed = utils.wjets_removal
  for key in loop_over_this:
    for merging_key, merging_list in merging_scheme.iteritems():
      if key in merging_list:
        to_be_removed.add( key )
        if merging_key in hists:
          hists[ merging_key ].Add( hists[ key ] ) 
        else:
          hists[ merging_key ] = hists[ key ].Clone( 'another_clone_' + hists[ key ].GetName() )
  to_be_used = []
  for k in hists:
    hist = hists[ k ]
    hist.SetFillColor( utils.get_colors( k ) ) 
    hist.SetLineColor( ROOT.kBlack ) 
    hist.SetLineWidth( 1 ) 
    hist.SetTitle( utils.titles[ k ] ) 
    if not k in to_be_removed:
      to_be_used.append( ( k, hist.Integral() ) )
  sample_list = sorted( to_be_used,  key = lambda x: x[ 1 ] )
  sample_list_r = sorted( to_be_used,  key = lambda x: x[ 1 ], reverse = True )
  new_stack = ROOT.THStack( stack.GetName() + '_clone', '' )
  for name, integral in sample_list:
    new_stack.Add( hists[ name ] )
  data = utils.re_style_top( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'met_tst_M2LEP_em_Nominal' ), True ) )
  error = utils.re_style_top( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'h0' ) ) )
  error.SetMarkerStyle( 1 )
  error.SetFillColor( ROOT.kBlack )
  error.SetFillStyle( 3345 )
  ###
  ratio_axis = utils.re_style_bot( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'h3' ) ) 
  ratio = utils.re_style_bot( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'h3' ), True ) ) 
  ratio_axis.GetXaxis().SetTitle( '#it{E}_{T}^{miss} [GeV]' ) 
  ratio_axis.GetYaxis().SetTitle( '#frac{Data}{Prediction}' )
  syst_band = utils.re_style_bot( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'h0' ) ) )
  syst_band.SetMarkerStyle( 1 )
  syst_band.SetFillColor( ROOT.kBlack )
  syst_band.SetFillStyle( 3345 )
  ###
  c_top.cd()
  new_stack.SetMaximum( 100000000 ) 
  new_stack.SetMinimum( 0.01 ) 
  new_stack.Draw( 'hist' )
  new_stack = utils.re_style_top( new_stack ) 
  new_stack.Draw( 'hist' )
  new_stack.GetXaxis().SetTitle( '#it{E}_{T}^{miss} [GeV]' )
  new_stack.GetYaxis().SetTitle( 'Events / 30 GeV' )
  #new_stack.GetXaxis().SetRangeUser( 0, 700 )
  error.Draw( 'e2 same' )
  data.Draw( 'pe' )
  x_l1, y_l1, latex1 = utils.draw_latex( utils.lumi, True )
  latex1.DrawLatex( x_l1, y_l1 - 0.12, utils.h_to_zz_to + utils.lepp + utils.lepm + utils.nu + utils.nubar + utils.void_char + utils.inv_prime )
  latex1.DrawLatex( x_l1, y_l1 - 0.18, '#it{e#mu} Control Region' + utils.void_char )
  leg = utils.create_legend( len( sample_list_r ), 0.3, 1 )
  leg.AddEntry( data, 'Data', 'pe' ) 
  for name, integral in sample_list_r: 
    leg.AddEntry( hists[ name ], hists[ name ].GetTitle(), 'f' ) 
  leg.AddEntry( error, 'Uncertainty', 'f' ) 
  leg.Draw()
  #utils.patch_bar( 229. / 566., 234. / 566., 322. / 407., 322. / 407., True ) 
  c_top.SetLogy()
  c_bottom.cd()
  ratio_axis.Draw( 'axis' )
  ratio_axis.GetXaxis().SetRangeUser( 0, 600 )
  syst_band.Draw( 'e2 same' )
  ratio.Draw( 'pe0 same' )
  c_bottom.Update()
  for arrow in utils.get_arrows( ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax(), ratio ):
    arrow.Draw()
  Line = ROOT.TLine( ROOT.gPad.GetUxmin(), 1, ROOT.gPad.GetUxmax(), 1 )
  Line.SetLineColor( ROOT.kBlack )
  Line.SetLineWidth( 2 )
  Line.SetLineStyle( 2 )
  Line.Draw()
  utils.save( canvas )
  #canvas.SaveAs( canvas.GetName() + '.pdf' )

# # # # # # # # # # # # # # # # # # # # # # # # # 

if __name__ == '__main__':
  sys.exit( main() )
