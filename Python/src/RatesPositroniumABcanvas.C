#ifdef __CLING__
#pragma cling optimize(0)
#endif
void RatesPositroniumABcanvas()
{
//=========Macro generated from canvas: scalerRate-Angle/Rates for scintillators A and B; Angle (deg); Rate (Hz)
//=========  (Sat May 27 15:36:57 2023) by ROOT version 6.26/10
   TCanvas *scalerRate-Angle = new TCanvas("scalerRate-Angle", "Rates for scintillators A and B; Angle (deg); Rate (Hz)",50,53,700,500);
   scalerRate-Angle->SetHighLightColor(2);
   scalerRate-Angle->Range(-128,-125,1152,1125);
   scalerRate-Angle->SetFillColor(0);
   scalerRate-Angle->SetBorderMode(0);
   scalerRate-Angle->SetBorderSize(2);
   scalerRate-Angle->SetFrameBorderMode(0);
   
   Double_t Rates-Angle-scalerB_fx1001[17] = {
   31,
   27,
   23,
   19,
   15,
   11,
   7,
   3,
   -1,
   -5,
   -9,
   -13,
   -17,
   -21,
   -25,
   -29,
   -33};
   Double_t Rates-Angle-scalerB_fy1001[17] = {
   211.3783,
   210.8778,
   209.9667,
   211.0976,
   209.7194,
   212.23,
   210.8125,
   213.6556,
   213.075,
   212.0556,
   211.1917,
   210.8933,
   210.9167,
   212.069,
   211.3542,
   208.0179,
   217.505};
   Double_t Rates-Angle-scalerB_fex1001[17] = {
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1};
   Double_t Rates-Angle-scalerB_fey1001[17] = {
   0.5935463,
   0.6249115,
   0.6613853,
   0.7089523,
   0.7632523,
   0.8410906,
   0.9372222,
   1.089484,
   1.332526,
   1.085397,
   0.9380646,
   0.8384377,
   0.7654277,
   0.7105817,
   0.663567,
   0.6094756,
   0.6020866};
   TGraphErrors *gre = new TGraphErrors(17,Rates-Angle-scalerB_fx1001,Rates-Angle-scalerB_fy1001,Rates-Angle-scalerB_fex1001,Rates-Angle-scalerB_fey1001);
   gre->SetName("Rates-Angle-scalerB");
   gre->SetTitle("Rates of #gamma-#gamma coincidences, scint. B");
   gre->SetFillStyle(1000);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#ff9900");
   gre->SetMarkerColor(ci);
   
   TH1F *Graph_RatesmIAnglemIscalerB1001 = new TH1F("Graph_RatesmIAnglemIscalerB1001","Rates of #gamma-#gamma coincidences, scint. B",100,-40.6,38.6);
   Graph_RatesmIAnglemIscalerB1001->SetMinimum(206.3385);
   Graph_RatesmIAnglemIscalerB1001->SetMaximum(219.177);
   Graph_RatesmIAnglemIscalerB1001->SetDirectory(0);
   Graph_RatesmIAnglemIscalerB1001->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_RatesmIAnglemIscalerB1001->SetLineColor(ci);
   Graph_RatesmIAnglemIscalerB1001->GetXaxis()->SetTitle(" Angle (deg)");
   Graph_RatesmIAnglemIscalerB1001->GetXaxis()->SetLabelFont(42);
   Graph_RatesmIAnglemIscalerB1001->GetXaxis()->SetTitleOffset(1);
   Graph_RatesmIAnglemIscalerB1001->GetXaxis()->SetTitleFont(42);
   Graph_RatesmIAnglemIscalerB1001->GetYaxis()->SetTitle(" Rate [Hz]");
   Graph_RatesmIAnglemIscalerB1001->GetYaxis()->SetLabelFont(42);
   Graph_RatesmIAnglemIscalerB1001->GetYaxis()->SetTitleFont(42);
   Graph_RatesmIAnglemIscalerB1001->GetZaxis()->SetLabelFont(42);
   Graph_RatesmIAnglemIscalerB1001->GetZaxis()->SetTitleOffset(1);
   Graph_RatesmIAnglemIscalerB1001->GetZaxis()->SetTitleFont(42);
   gre->SetHistogram(Graph_Rates-Angle-scalerB1001);
   
   gre->Draw("ap");
   
   TLegend *leg = new TLegend(0,0,0,0,NULL,"brNDC");
   leg->SetBorderSize(1);
   leg->SetTextSize(0.035);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
   TLegendEntry *entry=leg->AddEntry("Rates-Angle-scalerA","Rates of coincidence for scintillator A","lf");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry=leg->AddEntry("Rates-Angle-scalerB","Rates of coincidence for scintillator B","lf");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   leg->Draw();
   scalerRate-Angle->Modified();
   scalerRate-Angle->cd();
   scalerRate-Angle->SetSelected(scalerRate-Angle);
}
