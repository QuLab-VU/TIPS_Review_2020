function    ContourPlot(InputDat,saveornot, matrix_case)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Displays loaded experimental data and generated synergy models as 
% contour plots

  switch matrix_case
    case 1 
        Title = strcat([InputDat.Title]);
        TitlePlot = Title;
    case 2
        Title = strcat(['SANE synergy model ',InputDat.Title]);        
         TitlePlot={'SANE synergy model',InputDat.Title};
    case 3
        Title = strcat(['SANE antagonism model ',InputDat.Title]);
        TitlePlot={'SANE antagonism model',InputDat.Title};
    case 4
        Title = strcat(['Loewe model ',InputDat.Title]);
         TitlePlot={'Loewe model',InputDat.Title};
    case 5
        Title = strcat(['Bliss model ',InputDat.Title]);
         TitlePlot={'Bliss model',InputDat.Title};
    case 6
        Title = strcat(['HSA model ',InputDat.Title]);
        TitlePlot={'HSA model',InputDat.Title};
  end

  figure; 
  zlevs = 0:25:100;
  % contourf(InputDat.Avg,50,'LineStyle','none');
  % changed order v.2.0
  contourf(InputDat.Avg(end:-1:1,1:end),50,'LineStyle','none');

  hold on;
  % [C,h]=contour(InputDat.Avg,zlevs,'LineStyle',':','LineColor',[0.8 0.88 0.97],'ShowText','on');
  % changed order v.2.0
  [C,h]=contour(InputDat.Avg(end:-1:1,1:end),zlevs,'LineStyle',':','LineColor',[0.8 0.88 0.97],'ShowText','on');

  clabel(C,h,'FontSize',16,'Color',[0.31 0.4 0.58])
  
  set(gca,'FontSize',16);
  colormap(pink);
  
 %corrected v1.22
  caxis([0 110]);

  set(gca,'YTick', 1:size(InputDat.Avg,1));
 % set(gca,'YTickLabel',InputDat.Dose_ag1,'FontSize',14);
 % changed order v.2.0
  set(gca,'YTickLabel',InputDat.Dose_ag1(end:-1:1),'FontSize',14);


  set(gca,'XTick', 1:size(InputDat.Avg,2));
  set(gca,'XTickLabel',InputDat.Dose_ag2,'FontSize',14);
  
  % changed order v.2.0
  set(gca, 'XAxisLocation', 'top');

  title(TitlePlot,'FontSize',16);  
  % changed order v.2.0
  set(get(gca,'title'),'Position',[0.5 + size(InputDat.Avg,2)/2, 1-0.15*(size(InputDat.Avg,1)-1)]);

  xlabel(strcat(InputDat.Agent2,' [',InputDat.Unit2,']'),'FontSize',17);
  ylabel(strcat(InputDat.Agent1,' [',InputDat.Unit1,']'),'FontSize',17);

  if saveornot
    switch matrix_case
      case 1
        saveas(gcf,char(strcat(InputDat.Folder,'/Dose-response/pdf/Contour_',Title,'.pdf')), 'pdf')
        set(gca,'color','none')
        export_fig(char(strcat(InputDat.Folder,'/Dose-response/png/Contour_',Title)),'-png','-transparent')
      otherwise
        saveas(gcf,char(strcat(InputDat.Folder,'/pdf/Contour_',Title,'.pdf')), 'pdf')
        set(gca,'color','none')       
        export_fig(char(strcat(InputDat.Folder,'/png/Contour_',Title)),'-png','-transparent')        
    end 
  end
  
end