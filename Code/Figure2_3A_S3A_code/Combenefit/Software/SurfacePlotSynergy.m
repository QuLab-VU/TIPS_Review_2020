function SurfacePlotSynergy(InputDat,saveornot, matrix_case)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

% Displays synergy delta analysis as a surface plot (Synergy/Antagonism colormap)

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
  % surf(InputDat.Avg,'MarkerSize',14,'MarkerEdgeColor','k','Marker','.',...
  % 'EdgeColor','k','FaceColor','interp');
  % changed order v.2.0
  surf(InputDat.Avg','MarkerSize',14,'MarkerEdgeColor','k','Marker','.',...
  'EdgeColor','k','FaceColor','interp');

  map_syn_ant = colormap(jet);
  map_syn_ant = map_syn_ant(end:-1:1,:);
  colormap(map_syn_ant);

  %corrected v2.01
  caxis([-50 50])
  
  
  % set(gca,'YTick', 1:size(InputDat.Avg,2))
  % set(gca,'YTickLabel',InputDat.Dose_ag1,'FontSize',14)
  % set(gca,'XTick', 1:size(InputDat.Avg,1))
  % set(gca,'XTickLabel',InputDat.Dose_ag2,'FontSize',14)
  
  % changed order v.2.0  
  set(gca,'YTick', 1:size(InputDat.Avg,2))
  set(gca,'YTickLabel',InputDat.Dose_ag2,'FontSize',14)
     
  set(gca,'XTick', 1:size(InputDat.Avg,1))
  set(gca,'XTickLabel',InputDat.Dose_ag1,'FontSize',14)
   
  title(TitlePlot,'FontSize',16);
  
  % xlabel(strcat(InputDat.Agent2,' [',InputDat.Unit2,']'),'FontSize',16);
  % ylabel(strcat(InputDat.Agent1,' [',InputDat.Unit1,']'),'FontSize',16);
  % changed order v.2.0
  xlabel(strcat(InputDat.Agent1,' [',InputDat.Unit1,']'),'FontSize',16);
  ylabel(strcat(InputDat.Agent2,' [',InputDat.Unit2,']'),'FontSize',16);
  
  zlabel('% Control','FontSize',16);
  view(135,60);
  axis('tight') 
       
  if saveornot
    saveas(gcf,char(strcat(InputDat.Folder,'/pdf/Surface_',Title,'.pdf')), 'pdf')
    set(gca,'color','none')       
    export_fig(char(strcat(InputDat.Folder,'/png/Surface_',Title)),'-png','-transparent')
  end
  
end


