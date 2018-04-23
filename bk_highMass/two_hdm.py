import array, atlas, pickle, sys, utils
import ROOT

def main():
  
  ROOT.gROOT.SetBatch()

  limits = [ 
    ( 'ExclusionContours_2HDMTypeI_tanb_vs_cba.root',  '#bf{2HDM Type I, #it{m_{H}} = 200 GeV}',      1,   10, 26, -0.9, 0.9, 'cos(#beta-#alpha)',    utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + utils.lepm, None ),  
    ( 'ExclusionContours_2HDMTypeII_tanb_vs_cba.root', '#bf{2HDM Type II, #it{m_{H}} = 200 GeV}',     1,   10, 26, -0.9, 0.9, 'cos(#beta-#alpha)',    utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + utils.lepm, None ),  
    ( 'ExclusionContours_2HDMTypeI_tanb_vs_mH.root',   '#bf{2HDM Type I, cos(#beta-#alpha) = -0.1}',  0.5, 18, 80,     200,  400, '#it{m_{H}} [GeV]', utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + utils.lepm + ' + ' + utils.lepp + utils.lepm + utils.nu + utils.nubar, ( 320, 324, 31 ) ),  
    ( 'ExclusionContours_2HDMTypeII_tanb_vs_mH.root',  '#bf{2HDM Type II, cos(#beta-#alpha) = -0.1}', 0.5, 10, 35,     200,  400, '#it{m_{H}} [GeV]', utils.h_to_zz_to + utils.lepp + utils.lepm + utils.lepp + utils.lepm + ' + ' + utils.lepp + utils.lepm + utils.nu + utils.nubar, ( 320, 324, 15.6 ) ),  
  ]

  for file_name, mod_type, minY, maxY, max_maxY, minX, maxX, x_title, channel, patch_vals in limits:
    file = ROOT.TFile( 'inputs/' + file_name )
    first_base_hist = file.Get( 'h_med' ) 
    base_hist = ROOT.TH2F( first_base_hist.GetName() + '_extended', ';%s;tan#beta' % x_title, first_base_hist.GetXaxis().GetNbins(), first_base_hist.GetXaxis().GetXmin(), first_base_hist.GetXaxis().GetXmax(), 100 * first_base_hist.GetYaxis().GetNbins(), first_base_hist.GetYaxis().GetXmin(), 1000 )
    obs_name = 'obs'
    if 'tanb_vs_mH' in file_name:
      obs_name = 'obsc'
    types = [ 
      utils.graph_info( 'n2sig', file, 5, 1, 1001 ),
      utils.graph_info( 'n1sig', file, 3, 1, 1001 ),
      utils.graph_info( 'p1sig', file, 5, 1, 1001 ),
      utils.graph_info( 'p2sig', file, ROOT.kWhite, 1, 1001 ),
      #utils.graph_info( 'med', file, ROOT.kWhite, 1001 ), 
      utils.graph_info( 'medc', file, ROOT.kAzure + 2, 2 ), 
      utils.graph_info( 'obsf', file, ROOT.kOrange + 10, 1, 3844 ),
      utils.graph_info( obs_name, file, ROOT.kBlack, 1 ),
    ]
    graphs = {}
    single_graphs = {}
    for item in types:
      for index in range( item.number ):
        full_name = 'h_%s_contour_%d' % ( item.name, index )
        graphs[ full_name ] = ( utils.add_points( file.Get( full_name ), [] ), item )
        single_graphs[ item.name ] = graphs[ full_name ]
    canvas = ROOT.TCanvas( 'plot_' + file_name.replace( '.root', '' ), '', 600, 600 )
    base_hist.Draw( 'axis' )
    order = [ 'n2sig', 'n1sig', 'p1sig', 'p2sig', 'med', 'medc', 'obsf', obs_name ]
    for key1 in order:
      for key2, ( g, g_info ) in graphs.iteritems():
        if key1 in key2:
          g.SetLineColor( g_info.color )
          g.SetLineStyle( g_info.line )
          g.SetLineWidth( 2 )
          option = 'c'
          if g_info.fill:
            g.SetFillColor( g_info.color )
            g.SetFillStyle( g_info.fill )
            g.SetLineStyle( 1 )
            g.SetLineColor( ROOT.kBlack )
            option = 'fc'
            #if 'sig' in g_info.name:
            #  option = '3'
          g.Draw( option )
    base_hist.GetXaxis().SetRangeUser( minX, maxX )
    base_hist.GetYaxis().SetRangeUser( minY, max_maxY ) #utils.get_bound( minY, maxY ) )
    canvas.Update()
    the_box = utils.get_box( ROOT.gPad.GetUxmin(), ROOT.gPad.GetUxmax(), maxY, ROOT.gPad.GetUymax() )
    base_hist.Draw( 'axis same' )
    the_box.Draw( 'l' )
    x_l1, y_l1, latex1 = utils.draw_latex( utils.lumi, False )
    latex1.DrawLatex( x_l1, y_l1 - 0.105, channel )
    latex1.SetTextSize( 20 )
    #latex1.DrawLatex( x_l1, y_l1 - 0.16, '2HDM Type I, #it{m_{H}}=200 GeV' )
    latex1.SetTextAlign( 22 )
    latex1.DrawLatex( 0.535, y_l1 - 0.16, mod_type )
    xLeg = 0.62
    yLeg = 0.89
    leg = utils.create_legend_2hdm( 3 ) 
    leg.AddEntry( single_graphs[ obs_name ][ 0 ], 'Observed', 'l' )
    leg.AddEntry( single_graphs[ 'n1sig' ][ 0 ], '#pm1#sigma band', 'f' )
    leg.AddEntry( single_graphs[ 'medc' ][ 0 ], 'Expected', 'l' )
    leg.AddEntry( single_graphs[ 'n2sig' ][ 0 ], '#pm2#sigma band', 'f' )
    leg.AddEntry( None, '', '' )
    leg.AddEntry( single_graphs[ 'obsf' ][ 0 ], 'Excluded', 'f' )
    leg.Draw()
    #if patch_vals:
    #  p_x1, p_x2, p_y = patch_vals 
    #  utils.patch_bar( p_x1, p_x2, p_y, p_y ) 
    canvas.SetLogy()
    utils.save( canvas )

if __name__ == '__main__':
  sys.exit( main() )
