import array, atlas, csv, math, os, pickle, sys, utils
import ROOT
import collections

def main():
  
  ### Main definitions
  ROOT.gROOT.SetBatch()
  isLog = 0

  make_plot( 'BJETVETO_eemm_met_tst_1.2.root',   '', utils.h_to_zz_to + utils.two_l_two_v + utils.inv_prime, 180, 1000, 0.02, 1.98, isLog )
  make_plot( 'BJETVETO_ee_met_tst_1.2.root',   '', utils.h_to_zz_to + utils.two_e_two_v + utils.inv_prime, 180, 1000, 0.02, 1.98, isLog )
  make_plot( 'BJETVETO_mm_met_tst_1.2.root',   '', utils.h_to_zz_to + utils.two_mu_two_v + utils.inv_prime, 180, 1000, 0.02, 1.98, isLog )
  make_plot( 'BJETVETO_eemm_mT_ZZ_1.2.root',   '', utils.h_to_zz_to + utils.two_l_two_v + utils.inv_prime, 300, 1200, 0.02, 1.98, isLog )
  make_plot( 'BJETVETO_ee_mT_ZZ_1.2.root',   '', utils.h_to_zz_to + utils.two_e_two_v + utils.inv_prime, 300, 1200, 0.02, 1.98, isLog )
  make_plot( 'BJETVETO_mm_mT_ZZ_1.2.root',   '', utils.h_to_zz_to + utils.two_mu_two_v + utils.inv_prime, 300, 1200, 0.02, 1.98, isLog )

def make_plot( file_name, cat, title, minX = -999., maxX = -1., minY = 0.02, maxY = 1.98, isLog = 1 ):
  print "isLog:", isLog
  ###
  canvas, c_top, c_bottom = utils.create_double_pad( 'plot_%s' % file_name.replace( '.root', '' ) )
  ###
  root_file = ROOT.TFile( 'input_offshell/' + file_name )
  ch_file = file_name.split('_')[1]
  val_file = file_name.split('_')[2]+'_'+file_name.split('_')[3]
  stack = utils.re_style_top( root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetPrimitive( 'hs1' ) )
  hists = {}
  merging_scheme = {} #utils.complex_merging
  for hist in stack.GetHists():
    prev_color = hist.GetFillColor()
    #print hist, prev_color
    sample_name = None
    for key, vals in utils.original_colors_2l2v.iteritems():
      #print key, vals
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
  ### get those no stack histograms in pad1
  data, error, sbi, sbi5 = None, None, None, None
  for element in root_file.Get( 'c1' ).GetPrimitive( 'pad1' ).GetListOfPrimitives():
    #print element
    if element.GetName() == 'stat_sys_band_'+val_file+'_BJETVETO_'+ch_file:
      error = utils.re_style_top( element ) 
      error.SetMarkerStyle( 1 )
      error.SetFillColor( ROOT.kBlack )
      error.SetFillStyle( 3345 )
    elif element.GetName() == 'data_'+val_file+'_BJETVETO_'+ch_file+'_Nominal':
      data = utils.re_style_top( element ) 
    elif element.GetName() == 'SBI5_'+val_file+'_NLOIBJETVETO_'+ch_file+'_Nominal':
      sbi5 = utils.re_style_top( element ) 
      sbi5.SetMarkerColor(0)
      sbi5.SetMarkerStyle(0)
      sbi5.SetMarkerSize(0)
      sbi5.SetLineColor(616)
      sbi5.SetLineStyle(2)
    elif element.GetName() == 'SBI_'+val_file+'_NLOIBJETVETO_'+ch_file+'_Nominal':
      sbi = element
      prev_color = sbi.GetFillColor()
      #print sbi, prev_color
      sample_name = None
      for key, vals in utils.original_colors_2l2v.iteritems():
        if prev_color in vals:
          sample_name = key
      for k in hists:
        hist = hists[ k ]
        sbi.Add(hist, -1)
      hists[ sample_name ] = sbi

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
  to_be_used = [ ('ZZ', 3), ('Others', 1), ('WZ', 2), ('SBI', 4) ]
  for k in hists:
    hist = hists[ k ]
    hist.SetFillColor( utils.get_colors( k ) ) 
    if k=='SBI': hist.SetLineColor( ROOT.kBlue ) 
    else: hist.SetLineColor( ROOT.kBlack ) 
    hist.SetLineWidth( 1 ) 
    hist.SetTitle( utils.titles[ k ] ) 
  #  if not k in to_be_removed:
  #    penalty = 0
  #    to_be_used.append( ( k, hist.Integral() + penalty ) )
  print "to_be_used:", to_be_used
  sample_list = sorted( to_be_used,  key = lambda x: x[ 1 ] )
  sample_list_r = sorted( to_be_used,  key = lambda x: x[ 1 ], reverse = True )
  new_stack = ROOT.THStack( stack.GetName() + '_clone', '' )
  for name, integral in sample_list:
    #print name, integral
    new_stack.Add( hists[ name ] )
  ###
  ratio = utils.re_style_bot( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'ratio_bkg_data_'+val_file+'_BJETVETO_'+ch_file+'_Nominal' ) )
  syst_band = utils.re_style_bot( root_file.Get( 'c1' ).GetPrimitive( 'pad2' ).GetPrimitive( 'ratio_sys_band_'+val_file+'_BJETVETO_'+ch_file ), minY, maxY )
  syst_band.SetMarkerStyle( 1 )
  syst_band.SetFillColor( ROOT.kBlack )
  syst_band.SetFillStyle( 3345 )
  if val_file=='met_tst': syst_band.GetXaxis().SetTitle( utils.met ) 
  elif val_file=='mT_ZZ': syst_band.GetXaxis().SetTitle( utils.mTZZ ) 
  syst_band.GetYaxis().SetTitle( '#frac{Data}{Prediction}' )
  ###
  if minX==-999. or maxX==-1.: minX, maxX = ROOT.gPad.GetUxmin(), ROOT.gPad.GetUxmax()
  print "minX =", minX, "maxX =", maxX
  c_top.cd()
  new_stack.SetMinimum( 0.003 ) 
  new_stack.Draw( 'hist' )
  new_stack = utils.re_style_top( new_stack ) 
  new_stack.Draw( 'hist' )
  new_stack.GetXaxis().SetRangeUser( minX, maxX )
  #new_stack.GetXaxis().SetTitle( utils.m4l ) 
  new_stack.GetYaxis().SetTitle( 'Events / %d GeV' % stack.GetXaxis().GetBinWidth( 1 ) )
  #new_stack.GetYaxis().SetTitle( 'Events / %s' % stack.GetXaxis().GetBinWidth( 1 ) )
  if isLog==1: Yscale=1000
  else: Yscale=1.6
  new_stack.SetMaximum( data.GetMaximum()*Yscale )
  error.Draw( 'e2 same' )
  sbi5.Draw( 'hist same' )
  data.Draw( 'p same' )
  x_l1, y_l1, latex1 = utils.draw_latex( utils.lumi, True )
  latex1.DrawLatex( x_l1, y_l1 - 0.12, title + utils.void_char )
  latex1.DrawLatex( x_l1, y_l1 - 0.18, cat + utils.void_char )
  leg = utils.create_legend( len( sample_list_r ), 0.3, 1 )
  leg.AddEntry( data, 'Data', 'pe' ) 
  leg.AddEntry( sbi5, 'gg+VBF#rightarrow(H*#rightarrow)ZZ(#mu_{off-shell}=5)', 'l' ) 
  for name, integral in sample_list_r: 
    leg.AddEntry( hists[ name ], hists[ name ].GetTitle(), 'f' ) 
  leg.AddEntry( error, 'Uncertainty', 'f' ) 
  #leg.AddEntry( None, '', '' ) 
  #leg.AddEntry( None, '#color[0]{' + utils.titles[ 'emu' ] + '}', '' ) 
  leg.Draw()
  c_top.Update()
  if isLog==1: c_top.SetLogy()
  c_bottom.cd()
  syst_band.Draw( 'e2' )
  syst_band.GetXaxis().SetRangeUser( minX, maxX )
  ratio.Draw( 'pe0 same' )
  c_bottom.Update()
  #for arrow in utils.get_arrows( ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax(), ratio ): arrow.Draw()
  Line = ROOT.TLine( ROOT.gPad.GetUxmin(), 1, ROOT.gPad.GetUxmax(), 1 )
  Line.SetLineColor( ROOT.kBlack )
  Line.SetLineWidth( 2 )
  Line.SetLineStyle( 2 )
  Line.Draw()
  print "isLog:", isLog
  utils.save( canvas, isLog )

# # # # # # # # # # # # # # # # # # # # # # # # # 

if __name__ == '__main__':
  sys.exit( main() )
