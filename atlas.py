import ROOT

class atlas( ROOT.TStyle ):

  def __init__( self, name = "atlas", title = "ATLAS style object" ):
    ROOT.TStyle.__init__( self, name, title )
    self.SetName( name )
    self.SetTitle( title )
    self.configure()
    return

  def configure( self ):
    self.Info( "configure", "Configuring default ATLAS style" )
    icol = 0
    self.SetFrameBorderMode( 0 )
    self.SetFrameFillColor( icol )
    self.SetFrameFillStyle( 0 )
    self.SetCanvasBorderMode( 0 )
    self.SetPadBorderMode( 0 )
    self.SetPadColor( icol )
    self.SetCanvasColor( icol )
    self.SetStatColor( icol )
    self.SetPaperSize( 20, 26 )
    self.SetPadTopMargin( 0.05 )
    self.SetPadRightMargin( 0.09 )
    self.SetPadBottomMargin( 0.16 )
    self.SetPadLeftMargin( 0.16 )
    self.SetTitleXOffset(1.1);
    self.SetTitleYOffset(1.4);
    font_type = 43
    font_size = 20 
    label_size = 22 
    self.SetTextFont( font_type )
    self.SetTextSize( font_size )
    self.SetLabelFont( font_type, "x" )
    self.SetLabelSize( label_size, "x" )
    self.SetTitleFont( font_type, "x" )
    self.SetTitleSize( label_size, "x" )
    self.SetLabelFont( font_type, "y" )
    self.SetLabelSize( label_size, "y" )
    self.SetTitleFont( font_type, "y" )
    self.SetTitleSize( label_size, "y" )
    self.SetLabelFont( font_type, "z" )
    self.SetLabelSize( font_size, "z" )
    self.SetTitleFont( font_type, "z" )
    self.SetTitleSize( font_size, "z" )
    self.SetMarkerStyle( 20 )
    self.SetMarkerSize( 1.2 )
    self.SetLineStyleString( 2, "[12 12]" )
    self.SetEndErrorSize(0.)
    #self.SetErrorX(0)
    self.SetOptTitle( 0 )
    self.SetOptStat( 0 )
    self.SetOptFit( 0 )
    self.SetPadTickX( 1 )
    self.SetPadTickY( 1 )
    return

style = atlas()
ROOT.SetOwnership( style, False )
ROOT.gROOT.SetStyle( style.GetName() )
ROOT.gROOT.ForceStyle()
ROOT.TGaxis.SetMaxDigits( 4 )
