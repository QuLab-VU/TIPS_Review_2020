function varargout = Combenefit(varargin)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
% 
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
%
% ----------- Combenefit
% This routine specify the commands of each one of the Combenefit GUI
% interface's objects
%
%      Combenefit MATLAB code for Combenefit.fig
%      Combenefit, by itself, creates a new Combenefit or raises the existing
%      singleton*.
%
%      H = Combenefit returns the handle to a new Combenefit or the handle to
%      the existing singleton*.
%
%      Combenefit('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in Combenefit.M with the given input arguments.
%
%      Combenefit('Property','Value',...) creates a new Combenefit or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Combenefit_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Combenefit_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Combenefit

% Last Modified by GUIDE v2.5 10-Sep-2014 14:20:28

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Combenefit_OpeningFcn, ...
                   'gui_OutputFcn',  @Combenefit_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before Combenefit is made visible.
function Combenefit_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Combenefit (see VARARGIN)

% Read in a reza's color logo image.
% Prepare the full file name.

% folder = pwd;
folder = getcurrentdir;

baseFileName = 'LOGO_COMBENEFIT.png';

% Get the full filename, with path prepended.
fullFileName = fullfile(folder, baseFileName);
% Check for existence. Warn user if not found.
if ~exist(fullFileName, 'file')
    % Didn't find it there. Check the search path for it.
    fullFileName = baseFileName; % No path this time.
    if ~exist(fullFileName, 'file')
        % Still didn't find it. Alert user.
        errorMessage = sprintf('Error: %s does not exist.', fullFileName);
        uiwait(warndlg(errorMessage));
    end
else
    % Read it in from disk.
    rgbImage = imread(fullFileName);    % Display the original color image.
    axes(handles.axesImage);
    imshow(rgbImage, []);
%     title('TITLE', 'FontSize', 20);   
end

% FOR FUTURE VERSION
set(handles.CE_CHK,'Enable','off');
set(handles.CE_CHK,'Value',0);

set(handles.LOEWE_CHK,'Value',1);

% FOR FUTURE VERSION
set(handles.SMOOTH_CHK,'Enable','off');
set(handles.SMOOTH_CHK,'Value',0);
  
set(handles.ce_curves_chk,'Value',1)
set(handles.dr_surf_matrix_plot,'Value',1)

set(handles.syn_matrix_plot,'Value',1)

set(handles.save_batch_CHK,'Enable','off');
set(handles.save_batch_CHK,'Value',0);

set(handles.Test_chk,'Value',1);

set(handles.DISP_PROGR,'String','<<');

set(handles.DISP_PROGR, 'enable', 'inactive');

setappdata(handles.SEL_DIR_BUTT,'clicked',0);

% set(handles.DISP_DIR, 'enable', 'off')
set(handles.DISP_DIR, 'enable', 'inactive')

setappdata(hObject, 'IgnoreCloseAll', 1)

% Choose default command line output for Combenefit
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% % UIWAIT makes Combenefit wait for user response (see UIRESUME)
% uiwait;
% uiresume(handles.Run_Analysis_button);

% --- Outputs from this function are returned to the command line.
function varargout = Combenefit_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes when figure1 is resized.
function figure1_ResizeFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in CE_CHK.
function CE_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to CE_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of CE_CHK


% --- Executes on button press in LOEWE_CHK.
function LOEWE_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to LOEWE_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of LOEWE_CHK


% --- Executes on button press in BLISS_CHK.
function BLISS_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to BLISS_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of BLISS_CHK


% --- Executes on button press in HSA_CHK.
function HSA_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to HSA_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of HSA_CHK


% --- Executes on button press in ce_curves_chk.
function ce_curves_chk_Callback(hObject, eventdata, handles)
% hObject    handle to ce_curves_chk (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of ce_curves_chk


% --- Executes on button press in data_chk.
function data_chk_Callback(hObject, eventdata, handles)
% hObject    handle to data_chk (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of data_chk


% --- Executes on button press in refmod_chk.
function refmod_chk_Callback(hObject, eventdata, handles)
% hObject    handle to refmod_chk (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of refmod_chk


% --- Executes on button press in model_surf_plot.
function model_surf_plot_Callback(hObject, eventdata, handles)
% hObject    handle to model_surf_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of model_surf_plot


% --- Executes on button press in model_contour_plot.
function model_contour_plot_Callback(hObject, eventdata, handles)
% hObject    handle to model_contour_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of model_contour_plot


function DISP_DIR_Callback(hObject, eventdata, handles)
% hObject    handle to DISP_DIR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

handles.DISP_DIR = get(hObject,'String');
% Hints: get(hObject,'String') returns contents of DISP_DIR as text
%        str2double(get(hObject,'String')) returns contents of DISP_DIR as a double


% --- Executes during object creation, after setting all properties.
function DISP_DIR_CreateFcn(hObject, eventdata, handles)
% hObject    handle to DISP_DIR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in Run_Analysis_button.
function Run_Analysis_button_Callback(hObject, eventdata, handles)
% hObject    handle to Run_Analysis_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

  % Display progress
  set(handles.DISP_PROGR,'String','<< Checking options')
  
  dir_here = pwd;
  % Check directory
  directory_name = get(handles.SEL_DIR_BUTT,'UserData');

  % CHECK REQUESTED MODELS
  SA = get(handles.CE_CHK,'Value');
  LO = get(handles.LOEWE_CHK,'Value');
  BL = get(handles.BLISS_CHK,'Value');
  HS = get(handles.HSA_CHK,'Value');

  % CHECK IF ONE MODEL SELECTED AT LEAST AND IF A FOLDER HAS BEEN CHOSEN
  if(~(SA || LO || BL || HS))
    warndlg('You need to choose at least one model!');
    return;
  elseif (isempty(directory_name)|| ~directory_name(1));
     warndlg('You need to select a project folder!');
    return;
  else
 
  % Information on models
  Models = [SA,LO,BL,HS];

  % Check if batch analysis required
  BATCH = get(handles.BOX_BATCH,'Value');
 
  % --- Additional outputs ----
  
  % Check if plotting Dose response curves
  DRcurves_chk = get(handles.ce_curves_chk,'Value');
   
  % Check which plots for dose response surfaces
  DRsurf_matr = get(handles.dr_surf_matrix_plot,'Value');
  DRsurf_surf = get(handles.dr_surf_surf_plot,'Value');
  DRsurf_cont = get(handles.dr_surf_contour_plot,'Value');
  DRsurf_slic = get(handles.dr_surf_slices_plot,'Value');
  DR_surfaces_types = [DRsurf_matr, DRsurf_surf, DRsurf_cont, DRsurf_slic];
  
  % Check which plots for models
  Model_matr = get(handles.model_matrix_plot,'Value');
  Model_surf = get(handles.model_surf_plot,'Value');
  Model_cont = get(handles.model_contour_plot,'Value');
  Model_pl_types = [Model_matr,Model_surf,Model_cont];
  
  % Check which plots for synergy distribution
  Syn_matr = get(handles.syn_matrix_plot,'Value');
  Syn_surf = get(handles.syn_surf_plot,'Value');
  Syn_cont = get(handles.syn_contour_plot,'Value');
  Syn_on_dr_surf = get(handles.syn_on_dr_plot,'Value');    
  Syn_pl_types = [Syn_matr,Syn_surf,Syn_cont,Syn_on_dr_surf];
  % At least one type of plot should be selected for synergy distributions
  if(~any(Syn_pl_types) && ~BATCH)
    warndlg('You need at least one graphical output for "Synergy distribution". Please select at least one output.');
    return;
  end
 
  % Check if saving all plots
  saveda = get(handles.save_CHK,'Value');
  
  % Check T-Test
  T_Test_chk = get(handles.Test_chk,'Value');
  
  % Check smoothing
  Smoothing = get(handles.SMOOTH_CHK,'value');
  
  RunOpt = struct('Models', Models,...
                     'T_Test_chk', T_Test_chk,  'Smoothing', Smoothing, 'Save',saveda, ... 
                     'DRcurves_chk',DRcurves_chk,'DR_surfaces_types', DR_surfaces_types,...
                     'Model_pl_types',Model_pl_types, 'Syn_pl_types',...
                      Syn_pl_types);
  
                  
  % These variable is only used for Batch analysis.
     miss_data = 0;
     ndir = 1;
     
  if ~BATCH

    % SINGLE ANALYSIS
    if (getappdata(handles.SEL_DIR_BUTT,'clicked'))
    % Display progress
      set(handles.DISP_PROGR,'String','<< Single analysis: Loading Data');
      
      set(handles.Run_Analysis_button,'UserData',IMPORT_DATA(directory_name));
      setappdata(handles.SEL_DIR_BUTT,'clicked',0);
    end
    ExpDat = get(handles.Run_Analysis_button,'UserData');
        
    % Metrics cutoff - no cutoff at the moment   
    ExpDat.minSyn = 0.0;
    ExpDat.minAnt = 0.0;
  
%     if(ExpDat.Stop)
%       setappdata(handles.SEL_DIR_BUTT,'clicked',1);
%       return    
%     end
  
    QA = Check_Data_Quality_REP(ExpDat)
    if(~QA)
      warndlg('Data seems to be of poor quality. Please check.');
    end
    
    if(Smoothing)
      ExpDat = Spleen_smooth_ExpData(ExpDat);
    end 
    
    set(handles.DISP_PROGR,'String',['<< Processing: ' ExpDat.Title]);
    drawnow ;
    [metrics,  ParamsD1, ParamsD2] = RUN_ESTIMATION_GUI_2(ExpDat,RunOpt,handles.DISP_PROGR);
   
    Write_metrics_on_table(metrics, directory_name, dir_here,saveda);
   
  else
    set(0,'DefaultFigureVisible','off')
    % Display progress
    set(handles.DISP_PROGR,'String','>> Batch analysis: Loading Data.');
    
    % BATCH ANALYSIS      
    cd(directory_name)
     
    listing = dir;      
    isub = [listing(:).isdir];      
    Folder_cases = {listing(isub).name}';      
    Folder_cases(ismember(Folder_cases,{'.','..'})) = [];
    
    cd(dir_here);      
    ndir = size(Folder_cases,1);
    setappdata(handles.SEL_DIR_BUTT,'clicked',0);
    miss_data = 0;
    nmiss = 0;
    
    QA=zeros(ndir,1);
    for idir=1:ndir
      directory_name_child = strcat(directory_name,'/',Folder_cases{idir});
      set(handles.Run_Analysis_button,'UserData',IMPORT_DATA(directory_name_child));
      ExpDat = get(handles.Run_Analysis_button,'UserData');
%       ExpDat.D1max_chk = D1max_chk;
%       ExpDat.D2max_chk = D2max_chk;
%       ExpDat.D1max = D1max;
%       ExpDat.D2max = D2max;

     % Metrics cutoff - no cutoff at the moment  
      ExpDat.minSyn = 0.0;
      ExpDat.minAnt = 0.0;
  
      if(ExpDat.Stop)
          
        warndlg(['Combenefit did not find .xls files with '...
          'experimental data, or the data contains NaN cells,'...
          'in folder ', Folder_cases{idir},'. Skipping to next folder.']);
        close all;
        miss_data = 1;
        nmiss = nmiss+1;
        QA(idir) = 0;
      else
        % Checking data quality
        QA(idir) =  Check_Data_Quality_REP(ExpDat)       

      if(Smoothing)
        ExpDat = Spleen_smooth_ExpData(ExpDat);
      end 
        
        set(handles.DISP_PROGR,'String',['<< Processing: ' ExpDat.Title]);
        drawnow ;
        [metrics,  ParamsD1, ParamsD2] = RUN_ESTIMATION_GUI_2(ExpDat,RunOpt,handles.DISP_PROGR);
             
        Write_metrics_on_table(metrics, directory_name_child, dir_here,saveda);
             
        close all;
         
        MaxSyn(idir,1:4) = metrics(1,1:4);
        SynVol(idir,1:4) = metrics(2,1:4);
        WeiSynVol(idir,1:4) = metrics(3,1:4);
        SynSpread(idir,1:4) = metrics(4,1:4);
        C1Syn(idir,1:4) = metrics(5,1:4);
        C2Syn(idir,1:4) = metrics(6,1:4);
        MaxAnt(idir,1:4) = metrics(7,1:4);
        AntVol(idir,1:4) = metrics(8,1:4);
        WeiAntVol(idir,1:4) = metrics(9,1:4);
        AntSpread(idir,1:4) = metrics(10,1:4);
        C1Ant(idir,1:4) = metrics(11,1:4);
        C2Ant(idir,1:4) = metrics(12,1:4);    
        TotVol(idir,1:4) = metrics(13,1:4);
        TotWeiVol(idir,1:4) = metrics(14,1:4);    
        Agent1_params(idir,1:3) = ParamsD1;
        Agent2_params(idir,1:3) = ParamsD2;
        
        Drugs{idir,1} = ExpDat.Agent1;
        Drugs{idir,2} = ExpDat.Agent2;
        Drugs{idir,3} = ExpDat.Dose_ag1(end);
        Drugs{idir,4} = ExpDat.Dose_ag2(end);
        Combi{idir,1} = ExpDat.Title;
         
      end
        
      % Naming rows and eliminating double names
      % Name_Combi = Folder_cases{idir};
      Name_Combi = strcat(ExpDat.Agent2,' vs. ', ExpDat.Agent1);
      if(idir>1)
        iname = 2;
          while(any(strcmp(Name_Combi, RowNames)))
            Name_Combi= strcat(Name_Combi,[' ', num2str(iname)]);
            iname = iname+1;
          end
      end
%       RowNames{idir} = [Folder_cases{idir},' ',Name_Combi];
      RowNames{idir} = Folder_cases{idir};
    
      set(0,'DefaultFigureVisible','on')
   
    end
   
    if( exist('metrics','var'))
        
        % If last combi was not analysed, metrics, drugs and combi have not been filled.
        % Here we fill metrics with zeros for table size consistency and also Drugs and Combi identity
        if(ExpDat.Stop)
            MaxSyn(idir,1:4) = zeros(1,4);
            SynVol(idir,1:4) = zeros(1,4);
            WeiSynVol(idir,1:4) = zeros(1,4);
            SynSpread(idir,1:4) = zeros(1,4);
            C1Syn(idir,1:4) = zeros(1,4);
            C2Syn(idir,1:4) = zeros(1,4);
            MaxAnt(idir,1:4) = zeros(1,4);
            AntVol(idir,1:4) = zeros(1,4);
            WeiAntVol(idir,1:4) = zeros(1,4);
            AntSpread(idir,1:4) = zeros(1,4);
            C1Ant(idir,1:4) = zeros(1,4);
            C2Ant(idir,1:4) = zeros(1,4);    
            TotVol(idir,1:4) = zeros(1,4);
            TotWeiVol(idir,1:4) = zeros(1,4);    
            Agent1_params(idir,1:3) = zeros(1,3);
            Agent2_params(idir,1:3) = zeros(1,3);
        
           Drugs{idir,1} = ExpDat.Agent1;
           Drugs{idir,2} = ExpDat.Agent2;
           Drugs{idir,3} = ExpDat.Dose_ag1(end);
           Drugs{idir,4} = ExpDat.Dose_ag2(end);
           Combi{idir,1} = ExpDat.Title;
        end
        
        % IN THE FUTURE, ALL METRICS ON A UNIQUE TABLE??
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,MaxSyn,'SYN_MAX',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,SynVol,'SYN_SUM',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,WeiSynVol,'SYN_SUM_WEIGHTED',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,SynSpread, 'SYN_SPREAD',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,TotVol,'SYN_AVERAGE_C1',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,TotVol,'SYN_AVERAGE_C2',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,MaxAnt, 'ANT_MAX_FOLD_NAMES',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,AntVol, 'ANT_SUM',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,WeiAntVol, 'ANT_SUM_WEIGHTED',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,AntSpread, 'ANT_SPREAD',Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,C1Ant, 'ANT_AVERAGE_C1', Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,C2Ant, 'ANT_AVERAGE_C2', Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,TotVol, 'SUM_SYN_ANT', Drugs, Combi, directory_name, dir_here)
        Write_metrics_on_table_batch_long(RowNames, QA,Agent1_params,Agent2_params,TotWeiVol, 'SUM_SYN_ANT_WEIGHTED', Drugs, Combi, directory_name, dir_here)

% % Other older options/formats        
% %       Write_metrics_on_table_batch_DREAM(QA,Agent1_params,Agent2_params,TotVol,'SUM_SYN_ANT',Drugs, Combi, directory_name, dir_here)
% %       Write_metrics_on_table_batch(TotVol, 'SUM_SYN_ANT_FOLD_NAMES', RowNames, directory_name, dir_here);
% %       Write_params_on_table_batch(Agent1_params, 'AGENT1_D-R_PARAMS', RowNames, directory_name, dir_here);
% %       Write_params_on_table_batch(Agent2_params, 'AGENT2_D-R_PARAMS', RowNames, directory_name, dir_here);
     
    end
     
    

  end
  
  if (saveda || BATCH)
    % WE MAKE A REPORT ON THE ANALYSIS IF THIS IS SAVED OR IF IT WAS A
    % BATCH ANALYSIS
      
    %software version
    soft_version  = 'Combenefit 2.021.';
    %Creating information
    tit_repo = ['Report Analysis ', date,'.txt'];
    full_tit_rep = char(strcat(directory_name,'/',tit_repo));   
    % Open file for report
    fid = fopen(full_tit_rep, 'wt'); 
    
    % SOFTWARE VERSION AND ANALYSIS INFORMATION
    if BATCH
      if(nmiss<ndir)
        rep_mesg = ['This BATCH analysis has been performed on ', date,' with ',soft_version];
        if(miss_data)
          rep_mesg = [rep_mesg,' There were no data files in some of the subfolders.'];
        elseif(ndir==0)
          rep_mesg = ['The batch analyis could not be performed. There were no subfolders.'];
        end
      else
        rep_mesg = ['The BATCH analysis could not be performed because none of the subfolders contained the appropriate files.'];  
      end
      fprintf(fid, '%s', rep_mesg);
    else
      rep_mesg = ['This analysis has been performed on ', date,' with ',soft_version];
      fprintf(fid, '%s', rep_mesg);
    end  
    
    % ADDITIONAL PARAMETERS INFORMATION
    if( ~BATCH || nmiss<ndir)
      switch RunOpt.Smoothing
         case 2
           fprintf(fid, '\n') ;  
           rep_mesg = ['Smoothing was applied.'];
           fprintf(fid, '%s', rep_mesg);
       end    
%       if(any(RunOpt.Dmax_chk))
%         if(RunOpt.Dmax_val(1)<1e50)
%           fprintf(fid, '\n');  
%           rep_mesg = ['A maximum dose of ',num2str(RunOpt.Dmax_val(1)),' ',...
%               ExpDat.Unit1, ' has been applied for ', ExpDat.Agent1, '.' ];
%           fprintf(fid, '%s', rep_mesg);
%         end
%         if(RunOpt.Dmax_val(2)<1e50)
%            fprintf(fid, '\n');
%           rep_mesg = ['A maximum dose of ',num2str(RunOpt.Dmax_val(2)),' ',...
%               ExpDat.Unit2, ' has been applied for ', ExpDat.Agent2, '.' ];
%           fprintf(fid, '%s', rep_mesg);
%         end
%       end
    end
    
    fclose(fid);
  end
  
   set(handles.DISP_PROGR,'String','<< FINISHED. Select folder for new analysis. Reselect same if data was modified.');
  
end


% --- Executes on button press in save_CHK.
function save_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to save_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
act   = get(handles.save_CHK,'Value');
batch = get(handles.BOX_BATCH,'Value');
if(batch)
  if(act)
    set(handles.save_batch_CHK,'Value',0); 
  else
    set(handles.save_batch_CHK,'Value',1); 
  end
end


% Hint: get(hObject,'Value') returns toggle state of save_CHK

% --- Executes on button press in ALL_Models_CHK.
function ALL_Models_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to ALL_Models_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

act = get(handles.ALL_Models_CHK,'Value');
if(act)
     
%   set(handles.CE_CHK,'Value',1)
  
  set(handles.LOEWE_CHK,'Value',1)
  set(handles.BLISS_CHK,'Value',1)
  set(handles.HSA_CHK,'Value',1)
else
  set(handles.LOEWE_CHK,'Value',0)
  set(handles.BLISS_CHK,'Value',0)
  set(handles.HSA_CHK,'Value',0)
end

% Hint: get(hObject,'Value') returns toggle state of ALL_Models_CHK


% --- Executes on button press in ADD_OUT_CHK.
function ADD_OUT_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to ADD_OUT_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

act = get(handles.ADD_OUT_CHK,'Value');
if(act)
  set(handles.ce_curves_chk,'Value',1)
  set(handles.dr_surf_matrix_plot,'Value',1)
  set(handles.dr_surf_surf_plot,'Value',1)
  set(handles.dr_surf_contour_plot,'Value',1)
  set(handles.dr_surf_slices_plot,'Value',1)  
  set(handles.model_matrix_plot,'Value',1)
  set(handles.model_surf_plot,'Value',1)
  set(handles.model_contour_plot,'Value',1)
  set(handles.syn_matrix_plot,'Value',1)
  set(handles.syn_surf_plot,'Value',1)
  set(handles.syn_contour_plot,'Value',1)
  set(handles.syn_on_dr_plot,'Value',1)
elseif(~act)
  set(handles.ce_curves_chk,'Value',0)
  set(handles.dr_surf_matrix_plot,'Value',0)
  set(handles.dr_surf_surf_plot,'Value',0)
  set(handles.dr_surf_contour_plot,'Value',0)
  set(handles.dr_surf_slices_plot,'Value',0)  
  set(handles.model_matrix_plot,'Value',0)
  set(handles.model_surf_plot,'Value',0)
  set(handles.model_contour_plot,'Value',0)
  set(handles.syn_surf_plot,'Value',0)
  set(handles.syn_contour_plot,'Value',0)
  set(handles.syn_on_dr_plot,'Value',0)
end

% Hint: get(hObject,'Value') returns toggle state of ADD_OUT_CHK


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over CE_CHK.
function CE_CHK_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to CE_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in SEL_DIR_BUTT.
function SEL_DIR_BUTT_Callback(hObject, eventdata, handles)
% hObject    handle to SEL_DIR_BUTT (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

dir_here = pwd;
% cd ..
folder_name_prev = get(handles.SEL_DIR_BUTT,'UserData');
if(isempty(folder_name_prev))
    start_path = pwd;
else
    start_path = fileparts(folder_name_prev);
end
  folder_name = uigetdir(start_path, 'SELECT YOUR COMBINATIONS PROJECT DIRECTORY');
% cd(dir_here);

if(folder_name==0)
  if(isempty(folder_name_prev))  
    folder_name = [];
  else
    folder_name = folder_name_prev;
  end
end

%Ideally we want to display only the name of the directory that should
%reflects the project name
rest_display_title=folder_name;
icount=0;
while(~isempty(rest_display_title) && icount<20)
    icount=icount+1;
    [display_title,rest_display_title]=strtok(rest_display_title, '\');
end
% If something went wrong we settle for full name
if(icount>=20)
    display_title = folder_name;    
end

setappdata(handles.SEL_DIR_BUTT,'clicked',1);

if (~isempty(folder_name))
  if(folder_name(1))
    set(handles.SEL_DIR_BUTT,'UserData',folder_name);
    set(handles.DISP_DIR,'String',display_title);
    set(handles.DISP_PROGR,'String','<< Project Folder selected.');
  else
    set(handles.SEL_DIR_BUTT,'UserData',folder_name);
    set(handles.DISP_DIR,'String','Current Project'); 
    set(handles.DISP_PROGR,'String','<< Please select a specific folder containing your files');
  end
end


% --- Executes on button press in Clear_figs.
function Clear_figs_Callback(hObject, eventdata, handles)
% hObject    handle to Clear_figs (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
  close all

function currentDir = getcurrentdir
  if isdeployed % Stand-alone mode.
    [status, result] = system('path');
    currentDir = char(regexpi(result, 'Path=(.*?);', 'tokens', 'once'));
  else % MATLAB mode.
    currentDir = pwd;
end

% --- Executes on button press in License_button.
function License_button_Callback(hObject, eventdata, handles)
% hObject    handle to License_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

License_Message = sprintf([...
'------------------->-------------------> COMBENEFIT ===================>>\n'...
'\n'...
'Version 2.021\n'...
'64-bit (win64)\n'...
'December 2015\n'...
'\n'...
'The MIT License (MIT) \n'...
'\n'...
'Copyright (c) 2015 Giovanni Di Veroli \n'...
'\n'...
'Permission is hereby granted, free of charge, to any person obtaining a copy '...
'of this software and associated documentation files (the "Software"), to deal '...
'in the Software without restriction, including without limitation the rights '...
'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell '...
'copies of the Software, and to permit persons to whom the Software is '...
'furnished to do so, subject to the following conditions:\n'...
'\n'...
'The above copyright notice and this permission notice shall be included in '...
'all copies or substantial portions of the Software.\n'...
'\n'...
'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '...
'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '...
'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE '...
'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '...
'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, '...
'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN '...
'THE SOFTWARE.'...
]);

h = msgbox(License_Message,'About Combenefit');
set(h,'Color','k');
g=get(h,'Children');
set(g(1),'BackgroundColor',[0 0.8 1],'ForegroundColor','k','FontWeight','bold','FontSize',10,'FontAngle','italic');
l=get(g(2),'Children');
set(l,'BackgroundColor','k');
% set(l,'Color',[1 0.6 0.784]);
set(l,'Color',[0.953 0.87 0.733]);

% --- Executes on button press in BOX_BATCH.
function BOX_BATCH_Callback(hObject, eventdata, handles)
% hObject    handle to BOX_BATCH (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
act = get(handles.BOX_BATCH,'Value');
if(act)
  set(handles.save_batch_CHK,'Enable','on');
  set(handles.save_batch_CHK,'Value',1);
  set(handles.save_CHK,'Value',0);
  
  % Plots are removed when batch is selected for faster analysis
  myhandles = guidata(gcbo);
  set(handles.ADD_OUT_CHK,'Value',0);
  ADD_OUT_CHK_Callback(get(handles.ADD_OUT_CHK),[],myhandles)
else
  set(handles.save_batch_CHK,'Enable','off');
  set(handles.save_batch_CHK,'Value',0);
end


% Hint: get(hObject,'Value') returns toggle state of BOX_BATCH

% --- Executes on button press in save_batch_CHK.
function save_batch_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to save_batch_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

act = get(handles.save_batch_CHK,'Value');
batch = get(handles.BOX_BATCH,'Value');
if(batch)
  if(~act)
    set(handles.save_CHK,'Value',1);
  else
    set(handles.save_CHK,'Value',0);    
  end
end

% Hint: get(hObject,'Value') returns toggle state of save_batch_CHK


% --- Executes on selection change in SMOOTH_menu.
function SMOOTH_menu_Callback(hObject, eventdata, handles)
% hObject    handle to SMOOTH_menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns SMOOTH_menu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from SMOOTH_menu


% --- Executes during object creation, after setting all properties.
function SMOOTH_menu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to SMOOTH_menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in dr_surf_surf_plot.
function dr_surf_surf_plot_Callback(hObject, eventdata, handles)
% hObject    handle to dr_surf_surf_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of dr_surf_surf_plot


% --- Executes on button press in dr_surf_contour_plot.
function dr_surf_contour_plot_Callback(hObject, eventdata, handles)
% hObject    handle to dr_surf_contour_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of dr_surf_contour_plot


% --- Executes on button press in dr_surf_slices_plot.
function dr_surf_slices_plot_Callback(hObject, eventdata, handles)
% hObject    handle to dr_surf_slices_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of dr_surf_slices_plot


% --- Executes on button press in syn_surf_plot.
function syn_surf_plot_Callback(hObject, eventdata, handles)
% hObject    handle to syn_surf_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of syn_surf_plot


% --- Executes on button press in syn_contour_plot.
function syn_contour_plot_Callback(hObject, eventdata, handles)
% hObject    handle to syn_contour_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of syn_contour_plot

% --- Executes on button press in syn_on_dr_plot.
function syn_on_dr_plot_Callback(hObject, eventdata, handles)
% hObject    handle to syn_on_dr_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of syn_on_dr_plot


% --- Executes on button press in Test_chk.
function Test_chk_Callback(hObject, eventdata, handles)
% hObject    handle to Test_chk (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

act   = get(handles.Test_chk,'Value');
SMO = get(handles.SMOOTH_CHK,'Value');
if(act & SMO)
    set(handles.SMOOTH_CHK,'Value',0);
    warndlg('Smoothing is not applied when statistical significance is tested.');
end

% Hint: get(hObject,'Value') returns toggle state of Test_chk

% --- Executes on button press in syn_matrix_plot.
function syn_matrix_plot_Callback(hObject, eventdata, handles)
% hObject    handle to syn_matrix_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of syn_matrix_plot


% --- Executes on button press in model_matrix_plot.
function model_matrix_plot_Callback(hObject, eventdata, handles)
% hObject    handle to model_matrix_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of model_matrix_plot


% --- Executes on button press in dr_surf_matrix_plot.
function dr_surf_matrix_plot_Callback(hObject, eventdata, handles)
% hObject    handle to dr_surf_matrix_plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of dr_surf_matrix_plot



function DISP_PROGR_Callback(hObject, eventdata, handles)
% hObject    handle to DISP_PROGR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of DISP_PROGR as text
%        str2double(get(hObject,'String')) returns contents of DISP_PROGR as a double


% --- Executes during object creation, after setting all properties.
function DISP_PROGR_CreateFcn(hObject, eventdata, handles)
% hObject    handle to DISP_PROGR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in SMOOTH_CHK.
function SMOOTH_CHK_Callback(hObject, eventdata, handles)
% hObject    handle to SMOOTH_CHK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

act   = get(handles.SMOOTH_CHK,'Value');
Test = get(handles.Test_chk,'Value');
if(act & Test)
    set(handles.Test_chk,'Value',0);
    warndlg('Statistical significance is not tested when smoothing is applied.');
end

% Hint: get(hObject,'Value') returns toggle state of SMOOTH_CHK
