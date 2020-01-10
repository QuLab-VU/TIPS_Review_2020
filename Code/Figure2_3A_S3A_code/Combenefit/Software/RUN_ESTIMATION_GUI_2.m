function [metrics,  ParamsD1, ParamsD2]= RUN_ESTIMATION_GUI_2(ExpDat,RunOpt,handlesDISP_PROGR)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
 
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
% THE SOFTWARE.
%
% ------------------------ RUN_ESTIMATION_GUI -----------------------------
% This routine is called by the GUI with the appropriate inputs and 
% performs synergy estimation/displays graphical outputs as per requirements

disp(char(strcat(' ****************** Processing ',ExpDat.Folder,' ******************')));  
disp(char(strcat(' *********** Combination is: ',ExpDat.Title,' ************')));  

metrics = zeros(14,4);

% CREATE_FOLDER(ExpDat,RunOpt.Save,0);
  CREATE_FOLDER(ExpDat,RunOpt.Save,1);


[ParamsD1, ParamsD2,  opt1,  opt2] = FIT_SINGLE_AGENTS_CE_CURVES(ExpDat,RunOpt.Save);
if(RunOpt.DRcurves_chk)
     set(handlesDISP_PROGR,'String','<< Displaying single dose-response curves');
     PLOT_CE(ParamsD1, ExpDat, 1, RunOpt.Save);
     PLOT_CE(ParamsD2, ExpDat, 2, RunOpt.Save); 
end
 
% 2. Plot Experimental Data
if(any(RunOpt.DR_surfaces_types))
  set(handlesDISP_PROGR,'String','<< Displaying combination dose-response surface');
%   CREATE_FOLDER(ExpDat,RunOpt.Save,1);
  CREATE_DATA_OR_MODEL_PLOTS(ExpDat, RunOpt, 1);
 
end

% 3. SAN model (future version)

% 4. Loewe
if(RunOpt.Models(2))
  set(handlesDISP_PROGR,'String','<< Loewe analysis');

  LoeweModel = Calculate_Model(ParamsD1,ParamsD2, ExpDat,1);
  LoeweEstim = Estimate_Syn_Ant(LoeweModel,ExpDat);
  
  LoeweModel.Folder = CREATE_FOLDER(LoeweModel,RunOpt.Save,2);
  LoeweEstim.Folder = LoeweModel.Folder;
  
  if(any(RunOpt.Model_pl_types))
     CREATE_DATA_OR_MODEL_PLOTS(LoeweModel, RunOpt, 4)  
  end 
  
  CREATE_SYNERGY_PLOTS(ExpDat,LoeweEstim, RunOpt, 4)
  
  metrics(:,2)=CollectMetrics(LoeweEstim);
  
end

% 5. Bliss
if(RunOpt.Models(3))
  set(handlesDISP_PROGR,'String','<< Bliss analysis');

  BlissModel = Calculate_Model(ParamsD1,ParamsD2, ExpDat,2);    
  BlissEstim = Estimate_Syn_Ant(BlissModel,ExpDat);

  BlissModel.Folder = CREATE_FOLDER(BlissModel,RunOpt.Save,3);
  BlissEstim.Folder = BlissModel.Folder;
  
  if(any(RunOpt.Model_pl_types))      
     CREATE_DATA_OR_MODEL_PLOTS(BlissModel, RunOpt, 5)  
  end
  
  CREATE_SYNERGY_PLOTS(ExpDat,BlissEstim, RunOpt, 5)
  
  metrics(:,3)=CollectMetrics(BlissEstim);
  
end

% 6. HSA
if(RunOpt.Models(4))
  set(handlesDISP_PROGR,'String','<< HSA analysis');

  HsaModel = Calculate_Model(ParamsD1,ParamsD2, ExpDat,3);    
  HsaEstim = Estimate_Syn_Ant(HsaModel,ExpDat);
    
  HsaModel.Folder = CREATE_FOLDER(HsaModel,RunOpt.Save,4);
  HsaEstim.Folder = HsaModel.Folder;
  
  if(any(RunOpt.Model_pl_types))     
     CREATE_DATA_OR_MODEL_PLOTS(HsaModel, RunOpt, 6)
  end
  
%   CREATE_SYNERGY_PLOTS(HsaEstim,RunOpt, 6)
  CREATE_SYNERGY_PLOTS(ExpDat,HsaEstim,RunOpt, 6)
  
  metrics(:,4)=CollectMetrics(HsaEstim);

end        


  
end