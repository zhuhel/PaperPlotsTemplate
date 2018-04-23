import array, atlas, csv, math, os, pickle, sys, utils_old
import ROOT

def main():
  
  ### Main definitions
  ROOT.gROOT.SetBatch()

  #make_plot( 'm4l_VBF_4l.root',   'VBF-enriched', utils_old.h_to_zz_to + utils_old.four_l + utils_old.inv_prime,     400, ) #0.02, 2.98 )
  make_plot( 'm4l_ggF_4l.root',   'ggF-enriched', utils_old.h_to_zz_to + utils_old.four_l + utils_old.inv_prime,     100000, 0.0, 3.2 )
  #make_plot( 'm4l_ggF_2l2l.root', 'ggF-enriched', utils_old.h_to_zz_to + utils_old.lepp + utils_old.lepm + utils_old.lepp + '\\prime' + utils_old.lepm + '\\prime', 10000 )
  #make_plot( 'm4l_ggF_2l2l.root', 'ggF-enriched', utils_old.h_to_zz_to + utils_old.lepp + utils_old.lepm + utils_old.lepp + '\'' + utils_old.lepm + '\'', 10000 )
  #make_plot( 'm4l_ggF_4e.root',   'ggF-enriched', utils_old.h_to_zz_to + utils_old.ep + utils_old.em + utils_old.ep + utils_old.em + utils_old.inv_prime,     5000 )
  #make_plot( 'm4l_ggF_4mu.root',  'ggF-enriched', utils_old.h_to_zz_to + utils_old.mup + utils_old.mum + utils_old.mup + utils_old.mum + utils_old.inv_prime,   5000 )

def make_plot( file_name, cat, title, maxYtop, minY = 0.02, maxY = 1.98 ):
#def make_plot( file_name, cat, title, maxYtop, minY = 0.18, maxY = 1.82 ):
#def make_plot( file_name, cat, title, maxYtop, minY = 0., maxY = 3.4 ):
  ###
  canvas, c_top, c_bottom = utils_old.create_double_pad( 'plot_%s' % file_name.replace( '.root', '' ) )
  ###
  root_file = ROOT.TFile( 'inputs/' + file_name )
  stack = utils_old.re_style_top( root_file.Get( 'ratio' ).GetPrimitive( 'p1_ratio' ).GetPrimitive( 'combined' ) )
  hists = {}
  merging_scheme = {} #utils_old.complex_merging
  for hist in stack.GetHists():
    prev_color = hist.GetFillColor()
    sample_name = None
    for key, vals in utils_old.original_colors_4l.iteritems():
      if prev_color in vals:
        sample_name = key
    '''
    if not sample_name:
      'Sample Name Not Found'
    else:
      hist.SetFillColor( utils_old.get_colors( sample_name ) ) 
      #hist.SetLineColor( utils_old.colors[ sample_name ] ) 
      hist.SetLineColor( ROOT.kBlack ) 
      hist.SetLineWidth( 1 ) 
      hist.SetTitle( utils_old.titles[ sample_name ] ) 
    '''
    hists[ sample_name ] = hist
  ### Getting complicated here...
  loop_over_this = hists.keys()
  to_be_removed = set()
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
    hist.SetFillColor( utils_old.get_colors( k ) ) 
    hist.SetLineColor( ROOT.kBlack ) 
    hist.SetLineWidth( 1 ) 
    hist.SetTitle( utils_old.titles[ k ] ) 
    if not k in to_be_removed:
      penalty = 0
      if k == 'Red':
        penalty = -1
      to_be_used.append( ( k, hist.Integral() + penalty ) )
  sample_list = sorted( to_be_used,  key = lambda x: x[ 1 ] )
  sample_list_r = sorted( to_be_used,  key = lambda x: x[ 1 ], reverse = True )
  new_stack = ROOT.THStack( stack.GetName() + '_clone', '' )
  for name, integral in sample_list:
    new_stack.Add( hists[ name ] )
  data, error = None, None
  for element in root_file.Get( 'ratio' ).GetPrimitive( 'p1_ratio' ).GetListOfPrimitives():
    print element
    if element.GetName() == 'Graph':
      if not utils_old.is_data( element ):
        error = utils_old.re_style_top( element ) 
        error.SetMarkerStyle( 1 )
        error.SetFillColor( ROOT.kBlack )
        error.SetFillStyle( 3345 )
      else:
        data = utils_old.re_style_top( element ) 
  ###
  ratio = utils_old.re_style_bot( root_file.Get( 'ratio' ).GetPrimitive( 'p2_ratio' ).GetPrimitive( 'dataRatio' ) )
  syst_band = utils_old.re_style_bot( root_file.Get( 'ratio' ).GetPrimitive( 'p2_ratio' ).GetPrimitive( 'sysGraphRatio' ), minY, maxY )
  syst_band.SetMarkerStyle( 1 )
  syst_band.SetFillColor( ROOT.kBlack )
  syst_band.SetFillStyle( 3345 )
  #syst_band.GetXaxis().SetTitle( utils_old.m4l ) #'#it{m}_{4l} [GeV]' )
  #syst_band.GetYaxis().SetTitle( '#frac{Data}{Prediction}' )
  ###
  c_top.cd()
  new_stack.SetMinimum( 0.003 ) 
  new_stack.Draw( 'hist' )
  new_stack = utils_old.re_style_top( new_stack ) 
  new_stack.Draw( 'hist' )
  #new_stack.GetXaxis().SetRangeUser( 250, 1500 )
  new_stack.GetXaxis().SetTitle( utils_old.m4l ) #'#it{m}_{4l} [GeV]' )
  new_stack.GetYaxis().SetTitle( 'Events / %d GeV' % int( stack.GetXaxis().GetBinWidth( 1 ) ) )
  new_stack.SetMaximum( maxYtop )
  error.Draw( 'e2' )
  data.Draw( 'p same' )
  x_l1, y_l1, latex1 = utils_old.draw_latex( utils_old.lumi, True )
  latex1.DrawLatex( x_l1, y_l1 - 0.12, title + utils_old.void_char )
  latex1.DrawLatex( x_l1, y_l1 - 0.18, cat + utils_old.void_char )
  leg = utils_old.create_legend( len( sample_list_r ), 0.3, 1 )
  leg.AddEntry( data, 'Data', 'pe' ) 
  for name, integral in sample_list_r: 
    leg.AddEntry( hists[ name ], hists[ name ].GetTitle(), 'f' ) 
  leg.AddEntry( error, 'Uncertainty', 'f' ) 
  #leg.AddEntry( None, '', '' ) 
  #leg.AddEntry( None, '#color[0]{' + utils_old.titles[ 'emu' ] + '}', '' ) 
  leg.Draw()
  c_top.Update()
  minX, maxX = ROOT.gPad.GetUxmin(), ROOT.gPad.GetUxmax()
  c_top.SetLogy()
  c_bottom.cd()
  syst_band.Draw( 'ae2' )
  syst_band.GetXaxis().SetRangeUser( minX, maxX )
  ratio.Draw( 'pe0 same' )
  c_bottom.Update()
  for arrow in utils_old.get_arrows( ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax(), ratio ):
    arrow.Draw()
  Line = ROOT.TLine( ROOT.gPad.GetUxmin(), 1, ROOT.gPad.GetUxmax(), 1 )
  Line.SetLineColor( ROOT.kBlack )
  Line.SetLineWidth( 2 )
  Line.SetLineStyle( 2 )
  Line.Draw()
  utils_old.save( canvas )

# # # # # # # # # # # # # # # # # # # # # # # # # 

if __name__ == '__main__':
  sys.exit( main() )
