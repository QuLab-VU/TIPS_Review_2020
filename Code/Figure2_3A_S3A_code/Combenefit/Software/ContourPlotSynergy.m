% function ContourPlotSynergy(Delta,CC1,CC2,Name1,Name2,unit1,unit2,Title)
function    ContourPlotSynergy(InputDat,saveornot, matrix_case)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Displays synergy delta analysis as a contour plot
  
  switch matrix_case
    case 1 
        Title = strcat(['SANE_SYN_ANT_',InputDat.Title]);
        TitlePlot={'SANE synergy and antagonism',InputDat.Title};
        plot_bar = 1;
    case 2
        Title = strcat(['SANE_SYN_ONLY',InputDat.Title]);        
        TitlePlot={'SANE synergy',InputDat.Title};
        plot_bar = 2;
    case 3
        Title = strcat(['SANE_ANT_ONLY_',InputDat.Title]);
        TitlePlot={'SANE antagonism',InputDat.Title};
        plot_bar = 3;
    case 4
        Title = strcat(['Loewe_SYN_ANT_',InputDat.Title]);
         TitlePlot={'Loewe synergy and antagonism',InputDat.Title};
         plot_bar = 1;
    case 5
        Title = strcat(['Bliss_SYN_ANT_',InputDat.Title]);
         TitlePlot={'Bliss synergy and antagonism',InputDat.Title};
         plot_bar = 1;
    case 6
        Title = strcat(['HSA_SYN_ANT_',InputDat.Title]);
        TitlePlot={'HSA synergy and antagonism',InputDat.Title};
        plot_bar = 1;
  end

  figure;
  zlevs = -50:25:50;
 % contourf(InputDat.Avg,50,'LineStyle','none');
 % changed order v.2.0
  contourf(InputDat.Avg(end:-1:1,1:end),50,'LineStyle','none');
 
  hold on;
  % [C,h]=contour(InputDat.Avg,zlevs,'LineStyle',':','LineColor','k','ShowText','on');
  % changed order v.2.0
  [C,h]=contour(InputDat.Avg(end:-1:1,1:end),zlevs,'LineStyle',':','LineColor','k','ShowText','on');
  
  clabel(C,h,'FontSize',16,'Color','k')
  set(gca,'FontSize',16);  
  map_syn_ant = colormap(jet);
  map_syn_ant = map_syn_ant(end:-1:1,:);
  colormap(map_syn_ant);
% %corrected v1.22
%   caxis([-60 60])
  %corrected v2.01
  caxis([-50 50])

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
    saveas(gcf,char(strcat(InputDat.Folder,'/pdf/Contour_',Title,'.pdf')), 'pdf')
    set(gca,'color','none')       
    export_fig(char(strcat(InputDat.Folder,'/png/Contour_',Title)),'-png','-transparent')
  end

end