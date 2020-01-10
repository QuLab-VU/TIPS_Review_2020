function CREATE_DATA_OR_MODEL_PLOTS(ModelDat,RunOpt,modelcase)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

     if(modelcase==1)
         
       if(RunOpt.DR_surfaces_types(1))
         MatrixPlot(ModelDat,RunOpt.Save,modelcase) 
       end
       if(RunOpt.DR_surfaces_types(3))
        ContourPlot(ModelDat,RunOpt.Save,modelcase)
       end  
       if(RunOpt.DR_surfaces_types(2))
         SurfacePlot(ModelDat,RunOpt.Save,modelcase)
       end
       if(RunOpt.DR_surfaces_types(4))
         DR_curve_shift_Plot(ModelDat,RunOpt.Save)
       end
       
     else
         
       if(RunOpt.Model_pl_types(1))
         MatrixPlot(ModelDat,RunOpt.Save,modelcase) 
       end
       if(RunOpt.Model_pl_types(3))
        ContourPlot(ModelDat,RunOpt.Save,modelcase)
       end  
       if(RunOpt.Model_pl_types(2))
         SurfacePlot(ModelDat,RunOpt.Save,modelcase)
       end 
       
     end
end
