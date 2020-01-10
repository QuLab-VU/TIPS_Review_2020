function    SurfacePlot(InputDat,saveornot, matrix_case)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

% Displays loaded data as a surface plot (experimental data colormap)

  switch matrix_case
    case 1 
        Title = strcat([InputDat.Title]);
        TitlePlot = Title;
    case 2
        Title = strcat(['SANE synergy model ',InputDat.Title]);        
         TitlePlot={'SANE synergy model;',InputDat.Title};
    case 3
        Title = strcat(['SANE antagonism model ',InputDat.Title]);
        TitlePlot={'SANE antagonism model;',InputDat.Title};
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
  % surf(InputDat.Avg,'MarkerSize',14,'MarkerEdgeColor','k','Marker','.',...
  % 'EdgeColor',[0.8 0.88 0.97], 'FaceColor','interp');
  % changed order v.2.0
  surf(InputDat.Avg','MarkerSize',14,'MarkerEdgeColor','k','Marker','.',...
  'EdgeColor',[0.8 0.88 0.97], 'FaceColor','interp');

  colormap(pink);
 %corrected v1.22
  caxis([0 110]);

 
  % set(gca,'YTick', 1:size(InputDat.Avg,2))
  % set(gca,'YTickLabel',InputDat.Dose_ag1,'FontSize',14)
  
  % set(gca,'XTick', 1:size(InputDat.Avg,1))
  % set(gca,'XTickLabel',InputDat.Dose_ag2,'FontSize',14)
  % changed order v.2.0
  set(gca,'YTick', 1:size(InputDat.Avg,2))
  set(gca,'YTickLabel',InputDat.Dose_ag2,'FontSize',14)

  set(gca,'XTick', 1:size(InputDat.Avg,1))
  set(gca,'XTickLabel',InputDat.Dose_ag1,'FontSize',14)

  % xlabel(strcat(InputDat.Agent2,' [',InputDat.Unit2,']'),'FontSize',16);
  % ylabel(strcat(InputDat.Agent1,' [',InputDat.Unit1,']'),'FontSize',16);
  % changed order v.2.0
  xlabel(strcat(InputDat.Agent1,' [',InputDat.Unit1,']'),'FontSize',16);
  ylabel(strcat(InputDat.Agent2,' [',InputDat.Unit2,']'),'FontSize',16);
  
  zlabel('% Control','FontSize',16);
  title(TitlePlot,'FontSize',16);
  view(135,45);
  axis('tight');
  
 %corrected v1.22
  zlim([0 max(max(InputDat.Avg))]);

  if saveornot
    switch matrix_case
      case 1
        saveas(gcf,char(strcat(InputDat.Folder,'/Dose-response/pdf/Surface_',Title,'.pdf')), 'pdf')
        set(gca,'color','none')
        export_fig(char(strcat(InputDat.Folder,'/Dose-response/png/Surface_',Title)),'-png','-transparent')
       otherwise
        saveas(gcf,char(strcat(InputDat.Folder,'/pdf/Surface_',Title,'.pdf')), 'pdf')
        set(gca,'color','none')       
        export_fig(char(strcat(InputDat.Folder,'/png/Surface_',Title)),'-png','-transparent')        
    end 
  end
  
end


