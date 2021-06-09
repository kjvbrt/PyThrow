from .Utils import random_string, create_dir, make_ratio


class RatioPlot:
    def __init__(self, plot_name: str):
        from ROOT import TLegend
        from ROOT import kBlack, kBlue, kRed, kGreen, kOrange, kViolet, kPink
        from ROOT import kCyan

        self.colors = [kBlack, kBlue, kRed+1, kGreen+3, kOrange+4, kViolet-6,
                       kOrange-3, kGreen, kPink, kCyan, kBlue+3, kCyan+3]
        self.markers = [20, 21, 22, 23, 24, 25, 26]
        self.objects = []
        self.ratio_objects = []
        self.tick_length = 0.02
        self.ratio_label = 'Ratio  '
        self.notes = []

        self.legend = TLegend(.6, .6, .95, .95)
        self.legend.SetFillStyle(0)
        self.legend.SetBorderSize(0)
        self.legend.SetTextFont(43)
        self.legend.SetTextSize(12)

        self.plot_name = plot_name

    def add_hist(self,
                 inhist,
                 draw_option: str = 'PE',
                 draw_function: bool = False) -> None:
        from ROOT import TF1

        hist = inhist.Clone(inhist.GetName() + '_' + random_string())
        hist.DrawOption = draw_option
        if len(self.objects) != 0:
            hist.DrawOption += 'same'

        n_objects = len(self.objects)
        hist.SetLineWidth(2)
        hist.SetLineColor(self.colors[n_objects % len(self.colors)])
        hist.SetMarkerSize(.5)
        hist.SetMarkerColor(self.colors[n_objects % len(self.colors)])
        hist.SetMarkerStyle(self.markers[n_objects % len(self.markers)])

        hist.GetXaxis().SetLabelFont(43)
        hist.GetXaxis().SetLabelSize(12)
        hist.GetXaxis().SetTitleFont(43)
        hist.GetXaxis().SetTitleSize(12)
        hist.GetXaxis().SetTitleOffset(999)
        # hist.GetXaxis().SetTickLength(0.)
        hist.GetXaxis().SetLabelOffset(999)
        hist.GetXaxis().SetLabelSize(0)

        hist.GetYaxis().SetLabelFont(43)
        hist.GetYaxis().SetLabelSize(12)
        hist.GetYaxis().SetTitleFont(43)
        hist.GetYaxis().SetTitleSize(12)
        hist.GetYaxis().SetTitleOffset(2.1)
        hist.GetYaxis().SetTickLength(self.tick_length)

        self.legend.AddEntry(hist, hist.GetTitle(), hist.DrawOption + 'L')
        hist.SetTitle('')

        if draw_function:
            for func in hist.GetListOfFunctions():
                func.SetBit(TF1.kNotDraw)

        self.objects.append(hist)

    def add_ratio_hist(self, inhist, draw_option: str = 'PE') -> None:
        from ROOT import TF1
        hist = inhist.Clone(inhist.GetName() + '_' + random_string())
        hist.DrawOption = draw_option
        if len(self.ratio_objects) != 0:
            hist.DrawOption += 'same'

        n_objects = len(self.ratio_objects) + 1
        hist.SetLineWidth(2)
        hist.SetLineColor(self.colors[n_objects % len(self.colors)])
        hist.SetMarkerSize(.5)
        hist.SetMarkerColor(self.colors[n_objects % len(self.colors)])
        hist.SetMarkerStyle(self.markers[n_objects % len(self.markers)])

        hist.GetXaxis().SetLabelFont(43)
        hist.GetXaxis().SetLabelSize(12)
        hist.GetXaxis().SetTitleFont(43)
        hist.GetXaxis().SetTitleSize(12)
        hist.GetXaxis().SetTitleOffset(3.8)
        hist.GetXaxis().SetTickLength(self.tick_length * 2.5)

        hist.GetYaxis().SetLabelFont(43)
        hist.GetYaxis().SetLabelSize(12)
        hist.GetYaxis().SetTitleFont(43)
        hist.GetYaxis().SetTitleSize(12)
        hist.GetYaxis().SetTitleOffset(2.1)
        hist.GetYaxis().SetTickLength(self.tick_length)

        hist.SetTitle('')

        for func in hist.GetListOfFunctions():
            func.SetBit(TF1.kNotDraw)

        self.ratio_objects.append(hist)

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def make_ratio(self, obj1, obj2) -> None:
        obj = make_ratio(obj1, obj2)
        obj.GetYaxis().SetTitle(self.ratio_label)
        self.add_ratio_hist(obj)

    def set_ratio_label(self, ratio_label: str) -> None:
        for obj in self.ratio_objects:
            obj.GetYaxis().SetTitle(ratio_label + '  ')

    def set_x_range(self, x_min: int, x_max: int) -> None:
        for obj in self.objects:
            obj.GetXaxis().SetRangeUser(x_min, x_max)
        for obj in self.ratio_objects:
            obj.GetXaxis().SetRangeUser(x_min, x_max)

    def set_y_min(self, y_min: int) -> None:
        for obj in self.objects:
            obj.SetMinimum(y_min)

    def set_y_max(self, y_max: int) -> None:
        for obj in self.objects:
            obj.SetMaximum(y_max)

    def set_ratio_min(self, ratio_min: int) -> None:
        for obj in self.ratio_objects:
            obj.SetMinimum(ratio_min)

    def set_ratio_max(self, ratio_max: int) -> None:
        for obj in self.ratio_objects:
            obj.SetMaximum(ratio_max)

    def draw(self) -> None:
        from os import path
        from ROOT import TCanvas, TPad, gStyle

        canvas = TCanvas("canvas", "Canvas", 350, 450)
        pad1 = TPad("pad1", "Pad 1", 0., .3, 1., 1.)
        pad2 = TPad("pad2", "Pad 2", 0., 0., 1., .32)
        pad1.SetBottomMargin(.027)
        pad1.SetRightMargin(.05)
        pad1.SetTopMargin(.05)
        pad1.SetLeftMargin(.12)
        pad2.SetFillStyle(0)
        pad2.SetTopMargin(.00001)
        pad2.SetBottomMargin(.24)
        pad2.SetRightMargin(.05)
        pad2.SetLeftMargin(.12)

        gStyle.SetOptStat(0)
        pad1.SetTicks(1, 1)
        pad2.SetTicks(1, 1)
        pad1.Draw()
        pad2.Draw()

        pad1.cd()

        for obj in self.objects:
            # hist.SetMinimum(self.y_min)
            # hist.SetMaximum(self.y_max)

            obj.Draw(obj.DrawOption)

        for note in self.notes:
            self.legend.AddEntry('', note, '')
        self.legend.Draw()

        pad2.cd()

        for obj in self.ratio_objects:
            # hist.SetMinimum(self.ratio_min)
            # hist.SetMaximum(self.ratio_max)

            obj.Draw(obj.DrawOption)

        create_dir(path.dirname(self.plot_name))
        canvas.Print(self.plot_name + '.pdf')
