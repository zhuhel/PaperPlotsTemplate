import array, math, os, pickle, re, sys, time, uuid
import ROOT
import collections

lumi = 36.1

'''
#zz = '#it{ZZ*}'
zz = 'ZZ' #'#it{ZZ}'
h_to_zz_to = 'H \\to ' + zz + '\\to ' #'#it{H}#rightarrow' + zz + '#rightarrow'
g_to_zz_to = 'G_{KK} \\to ' + zz + '\\to ' #'#it{H}#to' + zz + '#to'
grav_axis = '#sigma #times #it{BR}(#it{G_{KK}} #rightarrow #it{ ' + zz + '})'
void_char = '' #'#color[0]{#xi}'
inv_prime = '' #'#color[0]{\'}'
times_brs = '#rightarrow #it{H}) #times #it{BR}(#it{H} #rightarrow #it{' + zz + '})'
times_br = '\\to H) \\times BR(H \\to ' + zz + ')'
ggf = '\\sigma(gg ' + times_br
vbf = '\\sigma(qq ' + times_br
lep = '\\ell' #'#it{l}'
lepp = '\\ell^{+}\\!' #'#it{l}^{+}'
lepm = '\\ell^{-}\\!' #'#it{l}^{-}'
ep = 'e^{+}\\!'
em = 'e^{-}\\!'
mup = '\\mu^{+}\\!'
mum = '\\mu^{-}\\!'
nu = '\\nu'
nubar = '\\nu' #'\\bar{\\nu}\\!'
m4l = 'm_{4\\ell} \\: \\mathrm{[GeV]}'
m4lonly = 'm_{4\\ell}'
ggfs = '#sigma(gg ' + times_brs
vbfs = '#sigma(qq ' + times_brs
cls = '#it{CL_{S}}'
four_l = lepp + lepm + lepp + lepm 
'''

plot_tag = 'Internal' #'Preliminary'

zz = '#it{ZZ}'
h_to_zz_to = '#it{H} #rightarrow ' + zz + ' #rightarrow ' #'#it{H}#rightarrow' + zz + '#rightarrow'
g_to_zz_to = '#it{G_{#it{KK}}} #rightarrow ' + zz + ' #rightarrow ' #'#it{H}#rightarrow' + zz + '#rightarrow'
grav_axis = '#sigma #times #it{BR}(#it{G_{#it{KK}}} #rightarrow ' + zz + ')'
void_char = '' #'#color[0]{#xi}'
inv_prime = '' #'#color[0]{\'}'
times_brs = '#rightarrow #it{H}) #times #it{BR}(#it{H} #rightarrow ' + zz + ')'
lep =  '#it{l}'
lepp = '#it{l}^{+}'
lepm = '#it{l}^{-}'
ep = 'e^{+}'
em = 'e^{-}'
mup = '#mu^{+}'
mum = '#mu^{-}'
nu = '#nu'
nubar = '#bar{#nu}'
m4l = '#it{m_{#it{4}l}} [GeV]'
m4lonly = '#it{m_{#it{4}l}}'
ggfs = '#sigma(gg ' + times_brs
vbfs = '#sigma(qq ' + times_brs
cls = '#it{CL_{S}}'
four_l = lepp + lepm + lepp + lepm 
four_e = ep + em + ep + em
four_mu = mup + mum + mup + mum
two_e_two_mu = ep + em + mup + mum
two_l_two_v = lepp + lepm + nu + nu 
two_e_two_v = ep + em + nu + nu 
two_mu_two_v = mup + mum + nu + nu 
met = '#it{E_{T}^{miss}} [GeV]'
mTZZ = '#it{m_{T}^{ZZ}} [GeV]'

samples_4l = [ 'SBI', 'qqZZ', 'Others']
samples_2l2v = [ 'SBI', 'qqZZ', 'Others' ]

#ordered_color_4l = collections.OrderedDict(original_colors_4l)
#original_colors_4l['Others'] = [1180]
#original_colors_4l['qqZZ']  = [1179]
#original_colors_4l['SBI']   = [851]
original_colors_4l   = { 'Others' : [ 1180 ], 'qqZZ': [ 1179 ], 'SBI': [ 851 ] }
original_colors_2l2v = { 'Others' : [ 1181 ], 'ZZ': [ 1179 ], 'WZ': [ 1180 ], 'SBI': [ 0 ] }

titles = { 'Others': 'Other backgrounds', 'SBI': 'gg+VBF#rightarrow(H*#rightarrow)ZZ(SM)', 'qqZZ': 'qq#rightarrowZZ', 'ZZ': 'ZZ', 'WZ': 'WZ' } 

single_merging = { 'ZZfull': [ 'ZZ', 'ZZewk' ] }
complex_merging = { 'ZZfull': [ 'ZZ', 'ZZewk' ], 'other': [ 'ttV', 'Top', 'Wjets' ] }

wjets_removal = set( [ 'Wjets' ] )

# # # # # # # # # # # # # # # # # # # # # # # # # 

def get_colors( name ):
  colors = { 
    'SBI': ROOT.kWhite,
    'qqZZ': ROOT.TColor.GetColor( '#CB0B09' ),
    'ZZ': ROOT.TColor.GetColor( '#CB0B09' ),
    'WZ': ROOT.TColor.GetColor( '#64c7f6' ),
    'Others': ROOT.TColor.GetColor( '#417508' )
  }
  return colors[ name ]

# # # # # # # # # # # # # # # # # # # # # # # # # 

def re_style_top( h ):
  h.GetXaxis().SetLabelOffset( 999 )
  return re_style( h, 22, 22, 150, 1.6, False )  

# # # # # # # # # # # # # # # # # # # # # # # # # 

def re_style_bot( h, minY = 0.18, maxY = 1.82 ):
  h.GetXaxis().SetLabelOffset( 0.005 )
  h.GetYaxis().SetNdivisions( 5, 3, 0 )
  h.SetMaximum( maxY )
  h.SetMinimum( minY )
  return re_style( h, 22, 22, 3.5, 1.6, True )  

# # # # # # # # # # # # # # # # # # # # # # # # # 

def re_style( h, label_size = 26, title_size = 26, title_offset_x = 1.6, title_offset_y = 1.6, center_title_y = False ):
  h.GetXaxis().SetLabelFont( 43 )
  h.GetXaxis().SetTitleFont( 43 )
  h.GetXaxis().SetLabelSize( label_size )
  h.GetXaxis().SetTitleSize( title_size )
  h.GetXaxis().SetTitleOffset( title_offset_x )
  h.GetYaxis().SetLabelFont( 43 )
  h.GetYaxis().SetTitleFont( 43 )
  h.GetYaxis().SetLabelSize( label_size )
  h.GetYaxis().SetTitleSize( title_size )
  h.GetYaxis().SetTitleOffset( title_offset_y )
  h.GetYaxis().CenterTitle( center_title_y )
  return h

# # # # # # # # # # # # # # # # # # # # # # # # # 

def cont_style( h, label_size = 22, title_size = 22, title_offset_x = 1.6, title_offset_y = 1.6, center_title_y = False ):
  h.GetXaxis().SetLabelFont( 43 )
  h.GetXaxis().SetTitleFont( 43 )
  h.GetXaxis().SetLabelSize( label_size )
  h.GetXaxis().SetTitleSize( title_size )
  h.GetXaxis().SetTitleOffset( title_offset_x )
  h.GetYaxis().SetLabelFont( 43 )
  h.GetYaxis().SetTitleFont( 43 )
  h.GetYaxis().SetLabelSize( label_size )
  h.GetYaxis().SetTitleSize( title_size )
  h.GetYaxis().SetTitleOffset( title_offset_y )
  h.GetYaxis().CenterTitle( center_title_y )
  h.SetLineWidth( 2 )
  return h

# # # # # # # # # # # # # # # # # # # # # # # # # 

def get_box( xm, xM, ym, yM ):
  box = ROOT.TBox( xm, ym, xM, yM )
  box.SetFillColor( ROOT.kWhite )
  #box.SetFillColor( ROOT.kRed )
  box.SetFillStyle( 1001 )
  box.SetLineWidth( 1 )
  box.SetLineColor( ROOT.kBlack )
  return box

# # # # # # # # # # # # # # # # # # # # # # # # # 

def draw_latex( lumi, is_double, offset_x = 0, offset_y = 0 ):
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextFont( 43 )
  latex.SetTextSize( 22 )
  if not is_double:
    latex.SetTextSize( 26 )
  latex.SetTextColor( 1 )
  latex.SetTextAlign( 12 )
  additional = ' '
  if not lumi:
    additional = ' Simulation '
  internal = '#bf{#it{ATLAS}}%s%s' % ( additional, plot_tag ) 
  sqrts = '#sqrt{s} = 13 TeV' 
  if lumi:
    sqrts += ', %.1f fb^{-1}' % lumi
  else:
    sqrts += '#color[0]{,fb^{-1}}'
  xLat = 0.19 + offset_x
  yLat = 0.9 + offset_y
  latex.DrawLatex( xLat, yLat, internal )
  latex.SetTextSize( 18 )
  if not is_double:
    latex.SetTextSize( 22 )
  offset = 0.05
  if is_double:
    offset = 0.062
  latex.DrawLatex( xLat, yLat - offset, sqrts ) 
  latex.SetTextSize( 17 )
  if not is_double:
    latex.SetTextSize( 22 )
  return xLat, yLat, latex

# # # # # # # # # # # # # # # # # # # # # # # # # 

def draw_x_axis_latex( text ):
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextFont( 43 )
  latex.SetTextSize( 20 )
  latex.SetTextColor( 1 )
  latex.SetTextAlign( 22 )
  xLat = 0.5
  yLat = 0.03
  latex.DrawLatex( xLat, yLat, text )
  return xLat, yLat, latex

# # # # # # # # # # # # # # # # # # # # # # # # # 

def draw_y_axis_latex( text ):
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextFont( 43 )
  latex.SetTextSize( 20 )
  latex.SetTextColor( 1 )
  latex.SetTextAlign( 22 )
  xLat = 0.03
  yLat = 0.5
  latex.SetTextAngle( 90 )
  latex.DrawLatex( xLat, yLat, text )
  return xLat, yLat, latex

# # # # # # # # # # # # # # # # # # # # # # # # # 

def draw_special_latex():
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextFont( 43 )
  latex.SetTextSize( 21 )
  latex.SetTextColor( 1 )
  latex.SetTextAlign( 12 )
  additional = ' Simulation '
  internal = '#bf{#it{ATLAS}}%s #scale[0.8]{#sqrt{s} = 13 TeV}' % additional
  xLat = 0.05
  yLat = 0.95
  latex.DrawLatex( xLat, yLat, internal )
  return xLat, yLat, latex

# # # # # # # # # # # # # # # # # # # # # # # # # 

def draw_small_latex( m, w ):
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextFont( 43 )
  latex.SetTextSize( 11 )
  latex.SetTextColor( 1 )
  latex.SetTextAlign( 12 )
  xLat = 0.24
  yLat = 0.85
  latex.DrawLatex( xLat, yLat, '#it{m_{H}}=%d GeV' % m )
  latex.SetTextAlign( 32 )
  latex.DrawLatex( 0.94, yLat, '#it{#Gamma_{H}}=%d%%#times#it{m_{H}}' % ( w * 100 ) )
  return latex

# # # # # # # # # # # # # # # # # # # # # # # # # 

def create_double_pad( name ):
  canvas = ROOT.TCanvas( name, '', 600, 600 )
  #canvas.SetFillStyle( 4000 )
  the_low_margin = 0.3 
  c_top = ROOT.TPad( 'c_top', '', 0.0, the_low_margin, 1.0, 1.0 )
  c_top.SetTopMargin( 0.05 )
  c_top.SetBottomMargin( 0.02 )
  #c_top.SetFillStyle( 4000 )
  c_top.SetFillColor( 0 )
  #c_top.SetFrameFillStyle( 4000 )
  c_top.SetFrameFillColor( 0 )
  c_top.Draw()
  c_bottom = ROOT.TPad( 'c_bottom', '', 0.0, 0.0, 1.0, the_low_margin )
  c_bottom.SetTopMargin( 0.00 )
  c_bottom.SetBottomMargin( 0.35 )
  #c_bottom.SetFillStyle( 4000 )
  c_bottom.SetFillColor( 0 )
  #c_bottom.SetFrameFillStyle( 4000 )
  c_bottom.SetFrameFillColor( 0 )
  c_bottom.Draw()
  return canvas, c_top, c_bottom

# # # # # # # # # # # # # # # # # # # # # # # # # 

def create_special_canvas( name ):
  canvas = ROOT.TCanvas( name, '', 600, 600 )
  #canvas.SetFillStyle( 4000 )
  pad = ROOT.TPad( 'the_pad', '', 0.05, 0.05, 1.0, 0.9 )
  pad.SetTopMargin( 0.0 )
  pad.SetBottomMargin( 0.0 )
  pad.SetFillStyle( 0 )
  #pad.SetFillColor( 0 )
  pad.SetFrameFillStyle( 0 )
  #pad.SetFrameFillColor( 0 )
  pad.Draw()
  pad.Divide( 3, 3 )
  pads = {}
  for i in range( 1, 10 ):
    pads[ i ] = pad.cd( i )
    pads[ i ].SetTopMargin( 0.05 )
    pads[ i ].SetRightMargin( 0.04 )
    pads[ i ].SetBottomMargin( 0.1 )
    pads[ i ].SetLeftMargin( 0.2 )
  return canvas, pad, pads

# # # # # # # # # # # # # # # # # # # # # # # # # 

def is_data( g ):
  ans = []
  for index in range( g.GetN() ):
    X, Y = ROOT.Double( 0. ), ROOT.Double( 0. )
    g.GetPoint( index, X, Y )
    ans.append( Y.is_integer() )
  return all( ans )

# # # # # # # # # # # # # # # # # # # # # # # # # 

def create_legend( num, width = 0.4, cols = 2 ):
  xLeg = 0.48 #was 0.5
  yLeg = 0.92
  #leg = ROOT.TLegend( xLeg, yLeg - 0.045 * ( num + 2 ), xLeg + width, yLeg )
  leg = ROOT.TLegend( xLeg, yLeg - 0.055 * ( num + 3 ), xLeg + width, yLeg )
  leg.SetFillStyle( 0 )
  leg.SetBorderSize( 0 )
  leg.SetTextFont( 43 )
  leg.SetTextSize( 16 )
  leg.SetNColumns( cols )
  return leg

# # # # # # # # # # # # # # # # # # # # # # # # # 

def create_legend_2hdm( num ):
  xLeg = 0.55
  yLeg = 0.93
  leg = ROOT.TLegend( xLeg, yLeg - 0.032 * ( num + 2 ), xLeg + 0.37, yLeg )
  leg.SetFillStyle( 0 )
  leg.SetBorderSize( 0 )
  leg.SetTextFont( 43 )
  leg.SetTextSize( 18 )
  leg.SetNColumns( 2 )
  return leg

# # # # # # # # # # # # # # # # # # # # # # # # # 

def create_single_legend( num, width = 0.3 ):
  xLeg = 0.6
  yLeg = 0.9
  leg = ROOT.TLegend( xLeg, yLeg - 0.06 * ( num ), xLeg + width, yLeg )
  leg.SetFillStyle( 0 )
  leg.SetBorderSize( 0 )
  leg.SetTextFont( 43 )
  leg.SetTextSize( 13 )
  return leg

# # # # # # # # # # # # # # # # # # # # # # # # # 

def create_special_legend():
  xLeg = 0.5
  yLeg = 0.99
  leg = ROOT.TLegend( xLeg, 0.91, xLeg + 0.48, yLeg )
  leg.SetFillStyle( 0 )
  leg.SetBorderSize( 0 )
  leg.SetTextFont( 43 )
  leg.SetTextSize( 13 )
  leg.SetNColumns( 2 )
  return leg

# # # # # # # # # # # # # # # # # # # # # # # # # 

def create_legend_limit( num, offset_x = 0, offset_y = 0 ):
  xLeg = 0.57 + offset_x
  yLeg = 0.9 + offset_y
  width = 0.25
  leg = ROOT.TLegend( xLeg, yLeg - 0.06 * ( num ), xLeg + width, yLeg )
  leg.SetFillStyle( 0 )
  leg.SetBorderSize( 0 )
  leg.SetTextFont( 43 )
  leg.SetTextSize( 18 )
  return leg

# # # # # # # # # # # # # # # # # # # # # # # # # 

def get_arrows( min_y, max_y, h ):
  arrows = []
  if h.ClassName() == 'TH1F':
    for Index in range( 1, h.GetNbinsX() + 1 ):
      x = h.GetXaxis().GetBinCenter( Index )
      y = h.GetBinContent( Index )
      if y > max_y:
        arrows.append( ROOT.TArrow( x, ( max_y - 1 ) / 1.5 + 1, x, ( max_y - 1 ) / 1.01 + 1, 0.02, '|>' ) )
      elif y < min_y and not y == 0:
        arrows.append( ROOT.TArrow( x, 1 - ( 1 - min_y ) / 1.5, x, 1 - ( 1 - min_y ) / 1.01, 0.02, '|>' ) )
  else:
    x, y = ROOT.Double( 0. ), ROOT.Double( 0. )
    for Index in range( h.GetN() ):
      h.GetPoint( Index, x, y )
      h_er = h.GetErrorYhigh( Index )
      l_er = h.GetErrorYlow( Index )
      if ( y - l_er ) > max_y:
        arrows.append( ROOT.TArrow( x, ( max_y - 1 ) / 1.5 + 1, x, ( max_y - 1 ) / 1.01 + 1, 0.02, '|>' ) )
      elif ( y + h_er ) < min_y and not y == 0:
        arrows.append( ROOT.TArrow( x, 1 - ( 1 - min_y ) / 1.5, x, 1 - ( 1 - min_y ) / 1.01, 0.02, '|>' ) )
  for arrow in arrows:
    arrow.SetFillColor( ROOT.kRed + 1 )
    arrow.SetLineColor( ROOT.kRed + 1 )
    arrow.SetLineWidth( 2 )
    ROOT.SetOwnership( arrow, False )
  return arrows 

# # # # # # # # # # # # # # # # # # # # # # # # # 

def save( c, isLog ):
  add = ''
  if 'Prelim' in plot_tag:
    add = '_prel'
  if isLog==1:
    add += '_log'
  else:
    add += '_linear'
  c.SaveAs( c.GetName() + add + '.pdf' )
  c.SaveAs( c.GetName() + add + '.png' )
  c.SaveAs( c.GetName() + add + '.eps' )

# # # # # # # # # # # # # # # # # # # # # # # # # 

def init_colors( n ):
  stop = array.array( 'd', [ 0.0, 0.5, 1.0 ] )
  #r    = array.array( 'd', [ 0.0, 1.0, 1.0, 0.0 ] )
  #g    = array.array( 'd', [ 0.0, 0.0, 1.0, 0.4 ] )
  #b    = array.array( 'd', [ 0.7, 0.0, 0.0, 0.0 ] )
  r    = array.array( 'd', [ 0.5, 1.0, 1.0 ] )
  g    = array.array( 'd', [ 0.0, 0.0, 0.5 ] )
  b    = array.array( 'd', [ 0.3, 0.0, 0.0 ] )
  first_color = ROOT.TColor.CreateGradientColorTable( len( stop ), stop, r, g, b, n )
  result = [ first_color + i  for i in range( n ) ]
  return result

# # # # # # # # # # # # # # # # # # # # # # # # # 

def make_ratio( n, d ):
  res = re_style_bot( n.Clone( 'res' ), 0.68, 1.32 )
  res.Divide( d )
  return res

# # # # # # # # # # # # # # # # # # # # # # # # # 

def get_min_max( *objects ):
  res_min, res_max = 10000000, -10000000
  for o in objects:
    res_min = min( res_min, o.GetMinimum() )  
    res_max = max( res_max, o.GetMaximum() )  
  return - res_max * 1.3 / 4., res_max * 1.3

# # # # # # # # # # # # # # # # # # # # # # # # # 

def get_min_max_shift( mass, width ):
  r = 20.
  shift = 2.5 * width
  res = math.ceil( ( mass * shift ) / r ) * r
  return mass - res, mass + res

# # # # # # # # # # # # # # # # # # # # # # # # # 

def get_extremes( mass, width, index = 0 ):
  
  vals = {
    400: { 0.01: 15 + index, 0.05: 64 + index, 0.1: 160 + index }, 
    600: { 0.01: 32 + index, 0.05: 114 + index, 0.1: 170 + index }, 
    800: { 0.01: 35 + index, 0.05: 160 + index, 0.1: 254 + index }, 
  }
  return mass - vals[ mass ][ width ], mass + vals[ mass ][ width ]
  '''
  if width == 0.01:
    f = 0.05
  if width == 0.05:
    f = 0.2
  if width == 0.1:
    f = 0.4
  return ( 1 - f ) * mass, ( 1 + f ) * mass
  '''

# # # # # # # # # # # # # # # # # # # # # # # # # 

class graph_info:

  def __init__ ( self, name, file, color, line, fill = None ):
    num_re = re.compile( '.*contour_(\d+).*' )
    self.name = name
    for k in file.GetListOfKeys():
      if name in k.GetName():
        num_match = num_re.match( k.GetName() )
        if num_match:
          self.number = int( num_match.group( 1 ) ) + 1
    self.color = color
    self.line = line
    self.fill = fill

# # # # # # # # # # # # # # # # # # # # # # # # # 

def add_points( g, l ):
  '''
  X, Y = ROOT.Double(), ROOT.Double()
  for i in range( g.GetN() ):
    g.GetPoint( i, X, Y )
    print 'bef -> ', i, X, Y
  for x, y in l:
    g.SetPoint( g.GetN(), x, y )
  for i in range( g.GetN() ):
    g.GetPoint( i, X, Y )
    print 'aft -> ', i, X, Y
  '''
  return g

# # # # # # # # # # # # # # # # # # # # # # # # # 

def get_bound( m, M ):
  lm = math.log10( m )
  lM = math.log10( M )
  l_new = ( lM - lm ) * 1.5
  return math.pow( 10, l_new ) 

# # # # # # # # # # # # # # # # # # # # # # # # # 

def re_shape_tail( h, get_ratio = False ):
  r = ROOT.TH1F( h.GetName() + '_r_' + str( uuid.uuid4() ), h.GetTitle(), 20, 0, 600 )
  r.Sumw2()
  last_error = 0.
  for index in range( 30 ):
    if index < 20:
      r.SetBinContent( index + 1, h.GetBinContent( index + 1 ) ) 
      r.SetBinError( index + 1, h.GetBinError( index + 1 ) ) 
    else:
      r.AddBinContent( 20, h.GetBinContent( index + 1 ) ) 
      last_error += math.pow( h.GetBinError( index + 1 ), 2 )
  r.SetBinError( 20, math.sqrt( last_error ) )
  if get_ratio:
    return r, r.GetBinError( 20 ) / r.GetBinContent( 20 )
  else:
    return r

# # # # # # # # # # # # # # # # # # # # # # # # # 

def change_last_bin( h, r ):
  #print
  #print r
  #print h.GetBinContent( 20 )
  #print h.GetBinError( 20 )
  h.SetBinError( 20, r )
  return h

# # # # # # # # # # # # # # # # # # # # # # # # # 

def patch_bar( x1, x2, y1, y2, is_ndc = False ):
  a = ROOT.TLine()
  a.SetLineWidth( 1 )
  if not is_ndc:
    a.DrawLine( x1, y1, x2, y2 )
  else:
    a.DrawLineNDC( x1, y1, x2, y2 )

# # # # # # # # # # # # # # # # # # # # # # # # # 

def th1_to_tgraph( h, remove_x = False ):
  #for i in range( h.GetNbinsX() + 1 ):
  #  print 'hist', i, h.GetBinContent( i ), '+/-', h.GetBinError( i )
  res = ROOT.TGraphAsymmErrors( h )
  if remove_x:
    for index in range( res.GetN() ):
      res.SetPointEXlow( index, 0 )
      res.SetPointEXhigh( index, 0 )
  return res

# # # # # # # # # # # # # # # # # # # # # # # # # 

def print_contents( h ):
  tot = 0.
  for index in range( 1, h.GetNbinsX() + 1 ):
    w = h.GetXaxis().GetBinWidth( index )
    y = h.GetBinContent( index )
    print '(w,y) ---> ', w, y
    tot += y * w / 50.
  print '(tot) ---> ', tot

# # # # # # # # # # # # # # # # # # # # # # # # # 

def print_details( g ):
  for index in range( g.GetN() ):
    X, Y = ROOT.Double( 0. ), ROOT.Double( 0. )
    g.GetPoint( index, X, Y )
    print 'Inspecting limit: (X,y) ---> ', X, Y
