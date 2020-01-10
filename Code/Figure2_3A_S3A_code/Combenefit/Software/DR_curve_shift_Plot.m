function    DR_curve_shift_Plot(ExpDat,saveornot)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Displays loaded data as shifts in d-r curves from the point pf view of
% each drug

  Title = strcat(['Data ',ExpDat.Title]);
  TitlePlot = Title;
  
  for drug = 1:2
  
  figure;
  hold on;
  
  if(drug==1)
    name1              = ExpDat.Agent1;
    name2              = ExpDat.Agent2;
 
    unit1              = ExpDat.Unit1;
    CC1     = ExpDat.Dose_ag1(2:end);
    unit2              = ExpDat.Unit2;
    CC2     = ExpDat.Dose_ag2(2:end);
  else
    name1              = ExpDat.Agent2;
    name2              = ExpDat.Agent1;
  
    unit1              = ExpDat.Unit2;
    CC1     = ExpDat.Dose_ag2(2:end); 
    unit2              = ExpDat.Unit1;
    CC2     = ExpDat.Dose_ag1(2:end);
  end
  
  Cend1 = 10^(log10(CC1(end)) + log10(CC1(end)/CC1(1))/24);
  Cstart1 = 10^(log10(CC1(1)) - log10(Cend1/CC1(1))/3);
  
  n_c2 = length(CC2);
  for jj=1:(n_c2+1)
    if(drug==1)
      dose_resp_exp     = ExpDat.Avg(2:end,jj);
    else
      dose_resp_exp     = ExpDat.Avg(jj,2:end);
    end
   
    plot(CC1,dose_resp_exp,'color',[(jj/(n_c2+1)),0,1],'LineWidth',3)
    set(gca,'LineWidth',2,'FontSize',20);
    set(gca,'XTick', [0.001 0.01 0.1 1 10 100 1000 1e4 1e5]);
    set(gca,'XTicklabel', {0.001 0.01 0.1 1 10 100 1000 '1e4' '1e5'});
    set(gca,'XMinorTick','off'); 
    if(jj>1)
      if((abs(prev_y-dose_resp_exp(1)))>5)
        text(CC1(1)*0.95,dose_resp_exp(1),[num2str(CC2(jj-1)) unit1],'Fontsize',14,'HorizontalAlignment','right')
        prev_y = dose_resp_exp(1);
      end
    else
      text(CC1(1)*0.95,dose_resp_exp(1),[num2str(0) unit1],'Fontsize',14,'HorizontalAlignment','right')
      prev_y = dose_resp_exp(1);
    end
  end
  xlabel(strcat(name1,' [',unit1,']'),'Fontsize',20);
  ylabel(' % Change','Fontsize',20);
  axis('tight');
  xlim([Cstart1 Cend1]); 
  ylim([-15 115]);
  set(gca,'XScale','log');
  
%   title([name1 ' d-r shift when adding ' name2],'FontSize',18);
  title(['D-r shift (+' name2 ')'],'FontSize',18);
  
  if saveornot
     saveas(gcf,char(strcat(ExpDat.Folder,'/Dose-response/pdf/',name1,'_DR_shift_',Title,'.pdf')), 'pdf')
     set(gca,'color','none')
     export_fig(char(strcat(ExpDat.Folder,'/Dose-response/png/',name1,'_DR_shift_',Title)),'-png','-transparent')   
  end
  
  end
  

  
end


