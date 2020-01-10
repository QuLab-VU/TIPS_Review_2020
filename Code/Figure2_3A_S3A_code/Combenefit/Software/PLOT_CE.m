function    PLOT_CE(params, ExpDat, Agent, saveornot);

% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

% Plot dose-response curves and highlight Abs EC50 or Rel EC95

if(Agent==1)
   dose_resp_exp     = ExpDat.Avg(2:end,1);
   dose_resp_exp_std = ExpDat.Std(2:end,1);
   CC                = ExpDat.Dose_ag1(2:end);
   name              = ExpDat.Agent1;
   unit              = ExpDat.Unit1;
elseif(Agent==2)
   dose_resp_exp     = ExpDat.Avg(1,2:end);
   dose_resp_exp_std = ExpDat.Std(1,2:end);
   CC                = ExpDat.Dose_ag2(2:end);
   name              = ExpDat.Agent2;
   unit              = ExpDat.Unit2;
end

  Cstart = CC(1)/3.1623;
  Cend = CC(end)*3.1623;

  X = [params 100];
  AB_EC50_value = 0;
  if(X(3)<50.0)
    AB_EC50_value = 1;
    AB_EC50 = responsedose(X,50);
    switch floor(log10(abs(AB_EC50))+1)
        case -1
            AB_EC50_displ_form = '%.e';
        case 0
            AB_EC50_displ_form = '%.3f';
        case 1
            AB_EC50_displ_form = '%.2f';
        case 2
            AB_EC50_displ_form = '%.1f';
        otherwise
            AB_EC50_displ_form = '%.f';
    end
  else    
    RE_EC95_value = 0;
% %     if(1.05*X(3)<100)
% %       RE_EC95 = responsedose(X,5 + 0.95*X(3));
    if((5 + 0.95*X(3))<100)
      RE_EC95 = responsedose(X,1.05*X(3));
      if(RE_EC95<10*CC(end))
        RE_EC95_value = 1;    
        switch floor(log10(abs(RE_EC95))+1)
          case -1
            RE_EC95_displ_form = '%.e';
          case 0
            RE_EC95_displ_form = '%.2f';
          case 1
            RE_EC95_displ_form = '%.1f';
          otherwise
            RE_EC95_displ_form = '%.f';
        end
      end
    end
  end

  % LOGARITHMIC SCALE
  n_points=100;
  logspacing = (log10(Cend)-log10(Cstart))/(n_points-1);
  for i=1:n_points
    Cgrid(i) = Cstart*10^((i-1)*logspacing);
  end
  figure
  semilogx(Cgrid,real(doseresponse(X,Cgrid)),'r-','LineWidth',6);         
  hold on;

  if(AB_EC50_value)
    if(AB_EC50<CC(end))
      title(strcat('Abs EC_{50}=',num2str(AB_EC50,AB_EC50_displ_form),' ',unit),'Fontsize',24)
    else
        if(AB_EC50<10*CC(end))
          title(strcat(' Interp. Abs EC_{50}=',num2str(AB_EC50,AB_EC50_displ_form),unit),'Fontsize',24)                  
        else
          title(strcat('Abs EC_{50}>',num2str(CC(end),'%.f'),' ',unit),'Fontsize',24)  
        end
    end
  else
    if(RE_EC95_value)
%       title(strcat('No Abs EC_{50}, Rel EC_{95}=',num2str(RE_EC95,RE_EC95_displ_form),' ',unit),'Fontsize',24)
      title(strcat('Rel EC_{95}=',num2str(RE_EC95,RE_EC95_displ_form),' ',unit),'Fontsize',24)
    else
      title(strcat('Abs EC_{50}>',num2str(CC(end),'%.f'),' ',unit),'Fontsize',24)      
    end
  end
  xlabel(strcat(name,' [',unit,']'),'Fontsize',24);
  ylabel(' % Change','Fontsize',24);
  axis('tight');
  xlim([Cstart Cend]); 
  ylim([0 115]);
  
  if(AB_EC50_value)      
    plot([AB_EC50 AB_EC50 1e-10],[0.0 50 50],'Color',[.51 .38 .48],'LineStyle','-.','LineWidth',3);
    plot(AB_EC50,50,'o','MarkerFaceColor',[.51 .38 .48],'MarkerSize',10);   
  elseif(RE_EC95_value)      
    y_reec95 = doseresponse(X,RE_EC95);  
    plot([RE_EC95 RE_EC95 1e-10],[0.0 y_reec95 y_reec95],'Color',[.51 .38 .48],'LineStyle','-.','LineWidth',3);
    plot(RE_EC95,y_reec95,'^','MarkerFaceColor',[.51 .38 .48],'MarkerSize',10);
    if(y_reec95>60)
%         set(gca,'YTick', [0 50 round(y_reec95) 100])
        set(gca,'YTick', intersect([0 50 round(y_reec95) 100],[0 50 100]))
    else
        set(gca,'YTick', [0 round(y_reec95) 100])        
    end
  end
  
  hE    = errorbar(CC,dose_resp_exp,dose_resp_exp_std,'xk','MarkerSize',25);

% %Does not work for Matlab 2014
%   hE_c  = get(hE     , 'Children'    );
%   errorbarXData  = get(hE_c(2), 'XData');
%   errorbarXData(4:9:end) = errorbarXData(1:9:end);
%   errorbarXData(7:9:end) = errorbarXData(1:9:end);
%   errorbarXData(5:9:end) = errorbarXData(1:9:end);
%   errorbarXData(8:9:end) = errorbarXData(1:9:end);
%   set(hE_c(2), 'XData', errorbarXData);
  set(hE,'LineWidth',4);
  
  set(gca,'LineWidth',2,'FontSize',24);
  set(gca,'XTick', [0.001 0.01 0.1 1 10 100 1000 1e4 1e5]);
  set(gca,'XTicklabel', {0.001 0.01 0.1 1 10 100 1000 '1e4' '1e5'});
  set(gca,'XMinorTick','off');  
  
  box off;  
  hold off;
  
   if saveornot
        saveas(gcf,char(strcat(ExpDat.Folder,'/Dose-response/pdf/',name,'_dose_res_curve.pdf')), 'pdf')
        set(gca,'color','none')       
        export_fig(char(strcat(ExpDat.Folder,'/Dose-response/png/',name,'_dose_res_curve')),'-png','-transparent')              
    end
end

    
