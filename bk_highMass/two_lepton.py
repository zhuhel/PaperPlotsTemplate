import array, atlas, csv, math, os, pickle, sys, utils
import ROOT

def main():
  
  ### Main definitions
  ROOT.gROOT.SetBatch()
  ###
  make_plot( 'BJETVETO_ee_mT.root', 'ee', utils.h_to_zz_to + utils.ep + utils.em + utils.nu + utils.nubar + utils.inv_prime,  3000 )
  make_plot( 'BJETVETO_mm_mT.root', 'mm', utils.h_to_zz_to + utils.mup + utils.mum + utils.nu + utils.nubar + utils.inv_prime, 3000 )

def make_plot( file_name, cat, title, maxYtop, minY = 0.18, maxY = 1.82 ):
  ###
  canvas, c_top, c_bottom = utils.create_double_pad( 'plot_sr_' + cat + 'vv' )
  ###
  root_file = ROOT.TFile( 'inputs/' + file_name )
  stack = utils.re_style_top( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'hs1' ) )
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
  to_be_removed = set()#utils.wjets_removal
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
      penalty = 0
      if k == 'Wjets':
        penalty = -1
      to_be_used.append( ( k, hist.Integral() + penalty ) )
  sample_list = sorted( to_be_used,  key = lambda x: x[ 1 ] )
  sample_list_r = sorted( to_be_used,  key = lambda x: x[ 1 ], reverse = True )
  new_stack = ROOT.THStack( stack.GetName() + '_clone', '' )
  for name, integral in sample_list:
    new_stack.Add( hists[ name ] )
  data = utils.re_style_top( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'mT_' + cat + '_Nominal' ), True ) )
  utils.print_contents( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'mT_' + cat + '_Nominal' ) )
  error = utils.re_style_top( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'h0' ) ) )
  error.SetMarkerStyle( 1 )
  error.SetFillColor( ROOT.kBlack )
  error.SetFillStyle( 3345 )
  ###
  ratio_axis = utils.re_style_bot( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'h3' ), minY, maxY ) 
  ratio = utils.re_style_bot( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'h3' ), True ), minY, maxY ) 
  ratio_axis.GetXaxis().SetTitle( '#it{m}_{T}^{' + utils.zz + '} [GeV]' ) 
  ratio_axis.GetYaxis().SetTitle( '#frac{Data}{Prediction}' )
  syst_band = utils.re_style_bot( utils.th1_to_tgraph( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'h0' ) ) )
  for index in range( syst_band.GetN() ):
    X, Y = ROOT.Double( 0. ), ROOT.Double( 0. )
    syst_band.GetPoint( index, X, Y )
  syst_band.SetMarkerStyle( 1 )
  syst_band.SetFillColor( ROOT.kBlack )
  syst_band.SetFillStyle( 3345 )
  syst_band.GetXaxis().SetTitle( '#it{m}_{T}^{' + utils.zz + '} [GeV]' ) 
  syst_band.GetYaxis().SetTitle( '#frac{Data}{Prediction}' )
  ###
  c_top.cd()
  new_stack.SetMinimum( 0.002 ) 
  new_stack.Draw( 'hist' )
  new_stack = utils.re_style_top( new_stack ) 
  new_stack.Draw( 'hist' )
  new_stack.GetXaxis().SetTitle( '#it{m}_{T}^{' + utils.zz + '} [GeV]' )
  new_stack.GetYaxis().SetTitle( 'Events / %d GeV' % int( stack.GetXaxis().GetBinWidth( 1 ) ) )
  new_stack.SetMaximum( maxYtop )
  new_stack.GetXaxis().SetRangeUser( 250, 1500 )
  error.Draw( '2 same' )
  data.Draw( 'pe' )
  x_l1, y_l1, latex1 = utils.draw_latex( utils.lumi, True )
  latex1.DrawLatex( x_l1, y_l1 - 0.12, title + utils.void_char )
  latex1.DrawLatex( x_l1, y_l1 - 0.18, '' )
  leg = utils.create_legend( len( sample_list_r ), 0.3, 1 )
  leg.AddEntry( data, 'Data', 'pe' ) 
  for name, integral in sample_list_r: 
    leg.AddEntry( hists[ name ], hists[ name ].GetTitle(), 'f' ) 
  leg.AddEntry( error, 'Uncertainty', 'f' ) 
  leg.Draw()
  mod_x, mod_y = 0, 0
  if cat == 'ee':
    mod_x, mod_y = 4, -2
  #utils.patch_bar( ( 228. + mod_x ) / 566., ( 233. + mod_x ) / 566., ( 324. + mod_y ) / 407., ( 324. + mod_y ) / 407., True ) 
  c_top.SetLogy()
  c_bottom.cd()
  ratio_axis.Draw( 'axis' )
  ratio_axis.GetXaxis().SetRangeUser( 250, 1500 )
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

# # # # # # # # # # # # # # # # # # # # # # # # # 

if __name__ == '__main__':
  sys.exit( main() )
