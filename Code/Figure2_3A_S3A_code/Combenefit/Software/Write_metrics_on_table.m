function Write_metrics_on_table(metrics, directory_name, dir_here, saveda)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Filter data for HTS when replicates are not availables

if(saveda)
      Tab_Metric = array2table(metrics);
      Tab_Metric.Properties.RowNames = {'SYN_MAX','SYN_SUM','SYN_SUM_WEIGHTED','SYN_SPREAD','SYN_AVERAGE_C1','SYN_AVERAGE_C2',...
                                         'ANT_MAX','ANT_SUM', 'ANT_SUM_WEIGHTED', 'ANT_SPREAD', 'ANT_AVERAGE_C1','ANT_AVERAGE_C2', ...
                                         'SUM_SYN_ANT', 'SUM_SYN_ANT_WEIGHTED' };
      
      Tab_Metric.Properties.VariableNames = { 'SANE', 'LOEWE', 'BLISS', 'HSA' };
      Tab_Metric.Properties.DimensionNames{1} = 'Metrics';      
      cd(directory_name);
      if (~exist([directory_name '\Metrics'], 'dir')) 
        mkdir(directory_name, 'Metrics')
      end
      cd('Metrics')
      % Check if file has been opened by user and avoid crash
      fID = fopen('Metrics.csv','w');
      if(fID>2)
        fclose(fID); 
        writetable(Tab_Metric,'Metrics.csv','WriteRowNames',true);   
      else
        warndlg('Combenefit could not save this combination metrics because the corresponding .xls file was open!');          
      end
      cd(dir_here);
  end
end