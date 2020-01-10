 function [ Data_Info ] = IMPORT_DATA(DataFolder)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

% Function that imports data from excel files and check several potential issues       

 stop_run    = 0;          
 CombeFolder = pwd;
 cd(DataFolder);

 XLS_File = dir('*.xls');
    
 if(isempty(XLS_File))
    warndlg(['Combenefit did not find the .xls files with the '...
             'experimental data in this folder. Please check that the '...
             'folder name is correct and that your files end in .xls ('...
             'a .xls template is available on our website). '...
             'If you meant to do a batch analysis, please ensure that ' ...
             'the corresponding case is checked.']);     
    stop_run = 1;
 end
       
    
 for i=1:length(XLS_File);

   fileToRead1 = strcat(DataFolder,'/',XLS_File(i,1).name);
   [data, textdata, raw] = xlsread(fileToRead1);
        
    incr=2;
    while(strcmp(textdata(incr,1),'')|| incr>100)
       incr = incr+1;
     end
        
    if(incr>100)
      error('problem with source file');
    end
        
    name1(i) = textdata(incr+1,2);
    name2(i) = textdata(incr+2,2);

    unit1(i) = textdata(incr+3,2);
    unit2(i) = textdata(incr+4,2);
    title(i) = textdata(incr+5,2);
    
    C1(:,i)    = data(2:end,1);
    C2(i,:)    = data(1,2:end);
    Data     = data(2:end,2:end);
        
%     if(find(Data<0))
%       warndlg('One of your file has negative data! This is set to 0.0');
%       Data(Data<0)=0;
%     end
                
     Resp(:,:,i) = Data;
          
  end
    
  % CHECK ALL LABELS ARE EQUAL
  nopb = 1;
  for i=2:length(XLS_File)
    nopb = min(nopb,strcmp(name1(1),name1(i)))
    nopb = min(nopb,strcmp(name2(1),name2(i)))
    nopb = min(nopb,strcmp(unit1(1),unit1(i)))
    nopb = min(nopb,strcmp(unit2(1),unit2(i)))
    nopb = min(nopb,strcmp(title(1),title(i)))        
  end
  if(~nopb)
     warndlg(['Your drug/agent names or units, or your title, are not ' ...
              'consistent across files. This might results in errors or '...
              'wrong labels.']);          
  end
   
  % CHECK ALL CONCENTRATIONS/DOSES ARE EQUAL
  nopb_C = 1;
  for i=2:length(XLS_File)
    nopb_C = min(nopb_C, isequal(C1(:,1),C1(:,i)));
    nopb_C = min(nopb_C, isequal(C2(1,:),C2(i,:)));
  end
  if(~nopb_C)
    warndlg(['Your drug/agent concentrations/doses are not consistent '...
             'across files. Please correct and rerun analysis.']);
    stop_run = 1;      
  end
    
  % CHECK CONCENTRATIONS ARE IN INCREASING ORDER
  % Drug 1 
  nopb_C1_order = 1;
  for i=1:length(XLS_File)
     nopb_C1_order = min(nopb_C1_order,issorted(C1(:,i)));
  end
  if(~nopb_C1_order && nopb_C)
    warndlg(['Your concentrations for agent/drug 1 are not in increasing '...
             'order. Or maybe you have a lost value somewhere.'...
             'Please correct and rerun analysis.']);
    stop_run = 1;
  end
  % Drug 2
  nopb_C2_order = 1;
  for i=1:length(XLS_File)
   nopb_C2_order = min(nopb_C2_order,issorted(C2(i,:)));
  end
  if(~nopb_C2_order && nopb_C)
    warndlg(['Your concentrations for agent/drug 2 are not in increasing '...
             'order. Please correct and rerun analysis.']);
    stop_run = 1;
  end
    
  % no files, no data!
  if(length(XLS_File)>=1)
    C1out    = C1(:,1);
    C2out    = C2(1,:);
    titout   = title(1);
    name1out = name1(1);
    name2out = name2(1);
    unit1out = unit1(1);
    unit2out = unit2(1);
  else
    Resp = 0.0;
    C1out    = 0.0;
    C2out    = 0.0;
    titout   = 'no title';
    name1out = 'no name1';
    name2out = 'no name2';
    unit1out = 'no unit1';
    unit2out = 'no unit2';
      
    stop_run = 1;
  end
  
  Nrepli = size(Resp,3);    
  Resp_AVG = mean(Resp,3);
  Resp_STD = std(Resp,0,3);
  if ( any(any(isnan(Resp_AVG))) || any(isnan(C1out)) || any(isnan(C2out)) )
     warndlg(['One of your data files contains NaN numbers. Please correct and rerun analysis.']);
    stop_run = 1; 
  end
  
  cd(CombeFolder); 
 
  
  Data_Info = struct('Title', titout, 'Agent1', name1out, 'Agent2', name2out,...
                     'Dose_ag1', C1out,  'Dose_ag2', C2out, 'Unit1',unit1out, ... 
                     'Unit2',unit2out,'N',Nrepli,'Resp', Resp, 'Avg', Resp_AVG,...
                     'Std',Resp_STD, 'Stop',stop_run,'Folder',DataFolder);
  
end