def random_string(size: int = 12) -> str:
    from random import choice
    from string import ascii_lowercase, digits

    chars = ascii_lowercase + digits

    return ''.join(choice(chars) for _ in range(size))


class RatioPlot:
    def __init__(self, plot_name: str):
        from ROOT import TLegend
        from ROOT import kBlack, kBlue, kRed, kGreen, kOrange, kViolet, kPink
        from ROOT import kCyan

        self.colors = [kBlack, kBlue, kRed+1, kGreen+3, kOrange+4, kViolet-6,
                       kOrange-3, kGreen, kPink, kCyan, kBlue+3, kCyan+3]
        self.markers = [20, 21, 22, 23, 24, 25, 26]
        self.hists = []
        self.ratio_hists = []
        self.tick_length = 0.02

        self.legend = TLegend(.4, .6, .98, .92)
        self.plot_name = plot_name

    def n_objects(self) -> int:
        return len(self.hists)

    def n_ratio_objects(self) -> int:
        return len(self.ratio_hists)

    def add_hist(self, inhist, draw_option='PE') -> None:
        hist = inhist.Clone(inhist.GetName() + '_' + random_string())
        hist.DrawOption = draw_option

        n_objects = self.n_objects()
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
        hist.SetTitle = ''

        self.hists.append(hist)

    def add_ratio_hist(self, inhist, draw_option: str = 'PE') -> None:
        hist = inhist.Clone(inhist.GetName() + '_' + random_string())
        hist.DrawOption = draw_option

        n_objects = self.n_ratio_objects() + 1
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

        self.ratio_hists.append(hist)

    def draw(self) -> None:
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
        objects_drawn = 0

        for hist in self.hists:
            # hist.SetMinimum(self.y_min)
            # hist.SetMaximum(self.y_max)

            if objects_drawn != 0:
                hist.DrawOption += 'same'

            hist.Draw(hist.DrawOption)

            objects_drawn += 1

        pad2.cd()
        objects_drawn = 0

        for hist in self.ratio_hists:
            # hist.SetMinimum(self.ratio_min)
            # hist.SetMaximum(self.ratio_max)

            if objects_drawn != 0:
                hist.DrawOption += 'same'

            hist.Draw(hist.DrawOption)

            objects_drawn += 1

        canvas.Print(self.plot_name + '.pdf')
