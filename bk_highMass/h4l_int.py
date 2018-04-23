import array, atlas, pickle, sys, utils
from itertools import product
import ROOT

def main():
  
  ROOT.gROOT.SetBatch()
  ROOT.TGaxis.SetMaxDigits( 5 )

  file = ROOT.TFile( 'inputs/interference_functions.root' )
  masses = [ 400, 600, 800 ]
  widths = [ 0.01, 0.05, 0.1 ]
  l_width = 3
  tot, sig, Hh, HB = None, None, None, None
  #for big_bad_index in range( 100 ):
  canvas, pad, pads = utils.create_special_canvas( 'plot_interference_example' )
  tot_hist, sig_hist, Hh_hist, HB_hist = {}, {}, {}, {}
  for index, ( mass, width ) in enumerate( product( masses, widths ) ):
    pads[ index + 1 ].cd()
    tot = file.Get( 'tot___m%d___w%d' % ( mass, width * 100 ) ) 
    sig = file.Get( 'sig___m%d___w%d' % ( mass, width * 100 ) ) 
    Hh = file.Get( 'Hh___m%d___w%d' % ( mass, width * 100 ) ) 
    HB = file.Get( 'HB___m%d___w%d' % ( mass, width * 100 ) ) 
    x_min, x_max = utils.get_extremes( mass, width ) #utils.get_min_max_shift( mass, width )
    mw_str = '_hist___m%d___w%d' % ( mass, width * 100 )
    tot_hist[ 'tot' + mw_str ]  = ROOT.TH1F( 'tot' + mw_str, '', 1000, x_min, x_max )
    tot_hist[ 'tot' + mw_str ].Add( tot, 1. )
    integral = tot_hist[ 'tot' + mw_str ].Integral()
    tot_hist[ 'tot' + mw_str ].Scale( 1. / integral )
    sig_hist[ 'sig' + mw_str ] = ROOT.TH1F( 'sig' + mw_str, '', 1000, x_min, x_max )
    sig_hist[ 'sig' + mw_str ].Add( sig, 1. / integral )
    Hh_hist[ 'Hh' + mw_str ] = ROOT.TH1F( 'Hh' + mw_str, '', 1000, x_min, x_max )
    Hh_hist[ 'Hh' + mw_str ].Add( Hh, 1. / integral )
    HB_hist[ 'HB' + mw_str ] = ROOT.TH1F( 'HB' + mw_str, '', 1000, x_min, x_max )
    HB_hist[ 'HB' + mw_str ].Add( HB, 1. / integral )
    #print integral
    #integral = 1.
    y_min, y_max = utils.get_min_max( tot_hist[ 'tot' + mw_str ], sig_hist[ 'sig' + mw_str ], Hh_hist[ 'Hh' + mw_str ], HB_hist[ 'HB' + mw_str ] )
    #y_min, y_max = -0.0015, 0.0075
    tot_hist[ 'tot' + mw_str ].SetMinimum( y_min )
    tot_hist[ 'tot' + mw_str ].SetMaximum( y_max )
    tot_hist[ 'tot' + mw_str ].Draw( 'c' )
    tot_hist[ 'tot' + mw_str ].GetXaxis().SetLabelSize( 10 )
    tot_hist[ 'tot' + mw_str ].GetYaxis().SetLabelSize( 10 )
    tot_hist[ 'tot' + mw_str ].SetLineWidth( l_width )
    sig_hist[ 'sig' + mw_str ].SetLineColor( ROOT.kOrange + 10 )
    sig_hist[ 'sig' + mw_str ].SetLineStyle( 2 )
    sig_hist[ 'sig' + mw_str ].SetLineWidth( l_width )
    sig_hist[ 'sig' + mw_str ].Draw( 'c same' )
    Hh_hist[ 'Hh' + mw_str ].SetLineColor( ROOT.kGreen + 1 )
    Hh_hist[ 'Hh' + mw_str ].SetLineStyle( 4 )
    Hh_hist[ 'Hh' + mw_str ].SetLineWidth( l_width )
    Hh_hist[ 'Hh' + mw_str ].Draw( 'c same' )
    HB_hist[ 'HB' + mw_str ].SetLineColor( ROOT.kBlue )
    HB_hist[ 'HB' + mw_str ].SetLineStyle( 3 )
    HB_hist[ 'HB' + mw_str ].SetLineWidth( l_width )
    HB_hist[ 'HB' + mw_str ].Draw( 'c same' )
    tot_hist[ 'tot' + mw_str ].Draw( 'c same' )
    l = utils.draw_small_latex( mass, width )
  canvas.cd()
  x_l1, y_l1, latex1 = utils.draw_special_latex()
  latex1.DrawLatex( x_l1, y_l1 - 0.045, utils.plot_tag )
  l2 = utils.draw_x_axis_latex( 'Particle-level ' + utils.m4l ) #it{m_{4l}} [GeV]' )
  l3 = utils.draw_y_axis_latex( '1/N #upoint dN/d#it{m}_{4#it{l}} [GeV^{-1}]' )
  leg = utils.create_special_legend()
  leg.AddEntry( tot_hist[ 'tot' + mw_str ], 'Signal + Interference', 'l' )
  leg.AddEntry( sig_hist[ 'sig' + mw_str ], 'Signal only', 'l' )
  leg.AddEntry( Hh_hist[ 'Hh' + mw_str ], '#it{H-h} Interference', 'l' )
  leg.AddEntry( HB_hist[ 'HB' + mw_str ], '#it{H-B} Interference', 'l' )
  leg.Draw()
  utils.save( canvas )
  ROOT.TGaxis.SetMaxDigits( 4 )

if __name__ == '__main__':
  sys.exit( main() )
