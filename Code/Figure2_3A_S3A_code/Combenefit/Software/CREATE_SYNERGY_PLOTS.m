function CREATE_SYNERGY_PLOTS(ExpDat,SynEstimDat,RunOpt, modelcase)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

     if(RunOpt.Syn_pl_types(1))
       MatrixPlotSynergy(SynEstimDat,RunOpt,modelcase) 
     end
     if(RunOpt.Syn_pl_types(3))
      ContourPlotSynergy(SynEstimDat,RunOpt.Save,modelcase)
     end  
     if(RunOpt.Syn_pl_types(2))
       SurfacePlotSynergy(SynEstimDat,RunOpt.Save,modelcase)
     end 
     if(RunOpt.Syn_pl_types(4))
       DRSurfSynergyPlot(ExpDat,SynEstimDat,RunOpt.Save,modelcase)
     end
end