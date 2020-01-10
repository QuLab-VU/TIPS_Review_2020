function    DRSurfSynergyPlot(InputDat,SynDat,saveornot, model_case)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Displays loaded data as a surface plot (experimental data colormap)

  switch model_case
    case 1 
        Title = strcat(['SANE_SYN_ANT_',InputDat.Title]);
        TitlePlot={'Synergy mapped to D-R (SAN)',InputDat.Title};
        plot_bar = 1;
    case 2
        Title = strcat(['SANE_SYN_ONLY',InputDat.Title]);        
        TitlePlot={'Synergy only, mapped to D-R (SAN)',InputDat.Title};
        plot_bar = 2;
    case 3
        Title = strcat(['SANE_ANT_ONLY_',InputDat.Title]);
        TitlePlot={'Antagonism only, mapped to D-R (SAN)',InputDat.Title};
        plot_bar = 3;
    case 4
        Title = strcat(['Loewe_SYN_ANT_',InputDat.Title]);
         TitlePlot={'Synergy mapped to D-R (LOEWE)',InputDat.Title};
         plot_bar = 1;
    case 5
        Title = strcat(['Bliss_SYN_ANT_',InputDat.Title]);
         TitlePlot={'Synergy mapped to D-R (BLISS)',InputDat.Title};
         plot_bar = 1;
    case 6
        Title = strcat(['HSA_SYN_ANT_',InputDat.Title]);
        TitlePlot={'Synergy mapped to D-R (HSA)',InputDat.Title};
        plot_bar = 1;
  end
  
  figure;
  
  % surf(InputDat.Avg,SynDat.Avg,'MarkerSize',14,'MarkerEdgeColor','k','Marker','.',...
  % 'EdgeColor',[0.8 0.88 0.97], 'FaceColor','interp');
  % changed order v.2.0
  surf(InputDat.Avg',SynDat.Avg','MarkerSize',14,'MarkerEdgeColor','k','Marker','.',...
  'EdgeColor',[0.8 0.88 0.97], 'FaceColor','interp');

  map_syn_ant = colormap(jet);
  map_syn_ant = map_syn_ant(end:-1:1,:);
  colormap(map_syn_ant);
  caxis([-50 50]);
  
%   hold on;
%   h_mesh=mesh(InputDat.Avg,'FaceColor','none');
%   colormap(pink);
%   caxis([0 110]);
 
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
  
  H=colorbar;
  set(H,'YTick',[]);
  
  switch plot_bar
    case 1
%       text(3.5,-60.0,'Antagonism','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
%       text(3.5,30.0,'Synergy','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
      
      ylabel(H, 'Antagonism           Synergy','FontWeight','bold','FontSize',14)
    case 2
      text(3.5,-60.0,'Synergy lack','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
      text(3.5,30.0,'Synergy','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
    case 3
      text(3.5,-60.0,'Antagonism','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
      text(3.5,30.0,'Antagonism lack','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14) 
  end

  if saveornot
        saveas(gcf,char(strcat(SynDat.Folder,'/pdf/Mapped_Surface_',Title,'.pdf')), 'pdf')
        set(gca,'color','none')       
        export_fig(char(strcat(SynDat.Folder,'/png/Mapped_Surface_',Title)),'-png','-transparent')
  end
  
end


