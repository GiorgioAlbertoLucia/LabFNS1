#
#   Macro with fundamental classes and functions to adjust plots in ROOT
#

from ROOT import TCanvas, TLegend, TFile
import yaml

from StyleFormatter import SetGlobalStyle

class CustomizedPlot:
    '''
    Load and customize plot in a .root file. Options can be set in a YAML configuration file

    Attributes
    ----------
        config : yaml object to import from a .yml configuration file
        canvas (TCanvas): ROOT canvas where the plot will be loaded
        pad (TPad): pad of the canvas
        legend (TLegend): legend to the 
    '''

    def __init__(self, configFilePath):
        with open(configFilePath, 'r') as configFile:
            self.config = yaml.safe_load(configFile)

        self.canvas = TCanvas('canvas', self.config['canvas']['title'], self.config['canvas']['width'],self. config['canvas']['height'])
        self.pad = self.canvas.cd()

        # set general pad options
        self.pad.SetFillColor(self.config['pad']['color'])
        self.pad.SetBorderMode(self.config['pad']['border_mode'])
        self.pad.SetBorderSize(self.config['pad']['border_size'])
        self.pad.SetLeftMargin(self.config['pad']['left_margin'])
        self.pad.SetRightMargin(self.config['pad']['right_margin'])
        self.pad.SetTopMargin(self.config['pad']['top_margin'])
        self.pad.SetBottomMargin(self.config['pad']['bottom_margin'])

        # create a legend and set general legend options
        if self.config['legend']['isTrue']:
            self.legend = TLegend(self.config['legend']['xmin'], self.config['legend']['ymin'], self.config['legend']['xmax'], self.config['legend']['ymax'])
            self.legend.SetBorderSize(self.config['legend']['border_size'])
            self.legend.SetFillColor(self.config['legend']['fill_color'])
            self.legend.SetFillStyle(self.config['legend']['bg_color'])
            #self.legend.SetTextSize(self.config['legend']['text_size'])
            #self.legend.SetTextFont(self.config['legend']['text_font'])

    def setHist(self, hist, **kwargs):
        '''
        Sets the properties of a histogram.

        Parameters
        ----------
            hist (TH1): Histogram object to customize
            **kwargs: Keyword arguments corrisponding to the proprties to be set. Available keywargs are
                - line_color: TColor   
                - line_style: int   
                - line_width: float
                - fill_color: TColor
                - fill_style: int
                - marker_color: TColor       
                - marker_style: int
                - title: str
                - x_title: str
                - x_title_size: float
                - x_title_offset: float
                - y_title: str
                - y_title_size: float
                - y_title_offset: float
                - draw_options: str
        
        If draw_options is set, the histogram will be drawn on the canvas with given options
        '''

        for key, value in kwargs.items():
            if   key == 'line_color':       hist.SetLineColor(value)
            elif key == 'line_style':       hist.SetLineStyle(value)
            elif key == 'line_width':       hist.SetLineWidth(value)

            elif key == 'fill_color':       hist.SetFillColor(value)
            elif key == 'fill_style':       hist.SetFillStyle(value)

            elif key == 'marker_color':     hist.SetMarkerColor(value)
            elif key == 'marker_style':     hist.SetMarkerStyle(value)

            elif key == 'x_title':          hist.GetXaxis().SetTitle(value)
            elif key == 'x_title_size':     hist.GetXaxis().SetTitleSize(value)
            elif key == 'x_title_offset':   hist.GetXaxis().SetTitleOffset(value)
            elif key == 'y_title':          hist.GetYaxis().SetTitle(value)
            elif key == 'y_title_size':     hist.GetYaxis().SetTitleSize(value)
            elif key == 'y_title_offset':   hist.GetYaxis().SetTitleOffset(value)

            elif key == 'draw_options':     
                # draw object on canvas
                self.canvas.cd()
                hist.Draw(f'{value} same')
                
                # if a legend is present, add a voice to the label
                if self.config['legend']['isTrue']:  self.legend.AddEntry(hist, hist.GetTitle(), value)

                self.canvas.Update()

    def setGraph(self, graph, **kwargs):
        '''
        Sets the properties of a graph.

        Parameters
        ----------
            graph (TGraph): Graph object to customize
            **kwargs: Keyword arguments corrisponding to the proprties to be set. Available keywargs are
                - line_color: TColor   
                - line_style: int   
                - line_width: float
                - fill_color: TColor
                - fill_style: int
                - marker_color: TColor       
                - marker_style: int
                - x_title: str
                - x_title_size: float
                - x_title_offset: float
                - y_title: str
                - y_title_size: float
                - y_title_offset: float
                - draw_options: str
        
        If draw_options is set, the histogram will be drawn on the canvas with given options
        
        Returns: None
        '''

        for key, value in kwargs.items():
            if   key == 'line_color':       graph.SetLineColor(value)
            elif key == 'line_style':       graph.SetLineStyle(value)
            elif key == 'line_width':       graph.SetLineWidth(value)

            elif key == 'fill_color':       graph.SetFillColor(value)
            elif key == 'fill_style':       graph.SetFillStyle(value)

            elif key == 'marker_color':     graph.SetMarkerColor(value)
            elif key == 'marker_style':     graph.SetMarkerStyle(value)

            elif key == 'x_title':          graph.GetXaxis().SetTitle(value)
            elif key == 'x_title_size':     graph.GetXaxis().SetTitleSize(value)
            elif key == 'x_title_offset':   graph.GetXaxis().SetTitleOffset(value)
            elif key == 'y_title':          graph.GetYaxis().SetTitle(value)
            elif key == 'y_title_size':     graph.GetYaxis().SetTitleSize(value)
            elif key == 'y_title_offset':   graph.GetYaxis().SetTitleOffset(value)

            elif key == 'draw_options':  
                # draw object on the canvas
                self.canvas.cd()
                graph.Draw(f'{value} same')
                
                # if a legend is present, add a voice to the label
                if self.config['legend']['isTrue']:  self.legend.AddEntry(graph, graph.GetTitle(), value)

                self.canvas.Update()

    def setCanvas(self, **kwargs):
        '''
        Sets the properties of the canvas.

        Parameters
        ----------
            **kwargs: Keyword arguments corrisponding to the proprties to be set. Available keywargs are
                - title: str
                - grid: bool
                - logx: bool
                - logy: bool
                - xmin: float
                - ymin: float
                - xmax: float
                - ymax: float
        '''
        if kwargs.keys() >= {'xmin', 'ymin', 'xmax', 'ymax'}:   self.canvas.cd().DrawFrame(kwargs['xmin'], kwargs['ymin'], kwargs['xmax'], kwargs['ymax'])

        for key, value in kwargs.items():
            if key == 'title':     self.canvas.SetTitle(value)
            if key == 'grid':      
                if value:    self.canvas.SetGrid()
            if key == 'logx':      
                if value:    self.canvas.SetLogx()
            if key == 'logy':      
                if value:    self.canvas.SetLogy()
            
    def save(self, filename):
        '''
        Saves the canvas to a file.

        Parameters
        ----------
            filename (str): Name of the file to save to

        Returns: None
        '''    

        self.canvas.SaveAs(filename)

def multiplePlotsSingleCanvas(generalConfigPath, configPath):
    '''
    Load different graphs on the same canvas, adjust settings and save the result in a .root file.
    Various configuration for individual graphs will be loaded from a yaml file. Similarly, general 
    canvas and legend settings will be loaded from a different yaml configuration file.

    (config file should have the structure of utils/config_multiplot.yml)

    Parameters
    ----------
        generalConfigPath (str): general configuration yaml file
        configPath (str): configuration file for single graphs

    Returns: None
    '''

    custom_plot = CustomizedPlot(generalConfigPath)

    # load all necessary information from yaml file
    with open(configPath, 'r') as configFile:
        config = yaml.load(configFile, yaml.FullLoader)

    finPaths = config['finPaths']
    objNames = config['objNames']
    objTypes = config['ROOTobject']

    foutPaths = config['foutPaths']       # only one output file
    outFormats = config['outFormats']

    lineColors = config['lineColors']
    lineWidths = config['lineWidths']
    lineStyles = config['lineStyles']
    fillColors = config['fillColors']
    fillStyles = config['fillStyles']
    markerColors = config['markerColors']
    markerStyles = config['markerStyles']
    xTitles = config['xTitles']
    xTitleSizes = config['xTitleSizes']
    xTitleOffset = config['xTitleOffset']
    yTitles = config['yTitles']
    yTitleSizes = config['yTitleSizes']
    yTitleOffset = config['yTitleOffset']
    drawOptions = config['drawOptions']

    canvasTitles = config['canvasTitles']
    axisTitles = config['axisTitles']   # [x_title, y_title]
    axisLimits = config['axisLimits']   # [xmin, ymin, xmax, ymax]

    SetGlobalStyle(padleftmargin=0.18, padbottommargin=0.14, optstat=0)


    for finPath, objName, objType, foutPath, outFormat, lineColor, lineWidth, lineStyle, fillColor, fillStyle, markerColor, markerStyle, xTitle, xTitleSize, yTitle, yTitleSize, drawOption, canvasTitle, axisLimit in zip(finPaths, objNames, objTypes, foutPaths, outFormats, lineColors, lineWidths, lineStyles, fillColors, fillStyles, markerColors, markerStyles, xTitles, xTitleSizes, yTitles, yTitleSizes, drawOptions, canvasTitles, axisLimits):
    
        custom_plot.setCanvas(title=canvasTitle, xmin=axisLimit[0], ymin=axisLimit[1], xmax=axisLimit[2], ymax=axisLimit[3])

        inFile = TFile.Open(finPath)
        obj = inFile.Get(objName)
        obj.SetMinimum(1.)

        if 'TH1' in objType:    custom_plot.setHist(obj, line_color=lineColor, line_style=lineStyle, line_width=lineWidth, fill_color=fillColor, 
                                                    fill_style=fillStyle, marker_color=markerColor, marker_style=markerStyle, x_title=xTitle, 
                                                    x_title_size=xTitleSize, x_title_offset=xTitleOffset, y_title=yTitle, y_title_size=yTitleSize, 
                                                    y_title_offset=yTitleOffset, draw_options=drawOption)
        if 'TGraph' in objType: custom_plot.setGraph(obj, line_color=lineColor, line_style=lineStyle, line_width=lineWidth, fill_color=fillColor, 
                                                    fill_style=fillStyle, marker_color=markerColor, marker_style=markerStyle, x_title=xTitle, 
                                                    x_title_size=xTitleSize, x_title_offset=xTitleOffset, y_title=yTitle, y_title_size=yTitleSize, 
                                                    y_title_offset=yTitleOffset, draw_options=drawOption)

    
    for outformat in outFormats:    custom_plot.save(f'{foutPath}.{outformat}')
    input('Press enter to continue')
    

    
# Run the multiplePlotsSingleCanvas function directily from this macro    
if __name__ == '__main__':

    generalConfigPath = 'Python/utils/config_plotter.yml'
    configPath = 'Python/utils/config_multiplot.yml'
    multiplePlotsSingleCanvas(generalConfigPath, configPath)    