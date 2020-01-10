function Write_metrics_on_table_batch_long(Folder,QA,HillA, HillB, Metric, MetricName, Drugs, Combi, directory_name, dir_here)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Filter data for HTS when replicates are not availables

      Tab_Folder = cell2table(Folder');
      Tab_QA = array2table(QA);
      Tab_Hill_A = array2table(HillA);
      Tab_Hill_B = array2table(HillB);
      
      Tab_Metric = array2table(Metric);
      Drugs( cellfun(@isempty, Drugs) ) = {'No_data'};
      Tab_Drugs = cell2table(Drugs);
      Combi( cellfun(@isempty, Combi) ) = {'No_data'};
      Tab_Combi = cell2table(Combi);

      Tab_Folder.Properties.VariableNames = {'Folder'};
      Tab_QA.Properties.VariableNames = {'QA'};
      Tab_Hill_A.Properties.VariableNames = {'IC50_A','H_A','Einf_A'};
      Tab_Hill_B.Properties.VariableNames = {'IC50_B','H_B','Einf_B'};
      Tab_Metric.Properties.VariableNames = {[MetricName '_SAN'], [MetricName '_LOEWE'], [MetricName '_BLISS'], [MetricName '_HSA']};
      Tab_Drugs.Properties.VariableNames = {'COMPOUND_A', 'COMPOUND_B','MAX_CONC_A','MAX_CONC_B'};
      Tab_Combi.Properties.VariableNames = {'TITLE'};
      Tab_all = [Tab_Folder,Tab_Combi,Tab_Drugs,Tab_Hill_A,Tab_Hill_B,Tab_Metric,Tab_QA];
      
%       Tab_Metric.Properties.DimensionNames{1} = 'COMPOUND_A';
      cd(directory_name);
      
      fID = fopen(strcat(MetricName,'.csv'),'w');
      if(fID>2)
        fclose(fID);
        writetable(Tab_all,strcat(MetricName,'.csv'),'WriteRowNames',true);   
      else
        warndlg(['Combenefit could not save ',strcat(MetricName,'.csv'), ' because the file was open!']);          
      end
      cd(dir_here);  
end