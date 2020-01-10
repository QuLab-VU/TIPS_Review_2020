function MatrixPlotSynergy(InputDat,RunOpt,matrix_case)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
                        
% Displays loaded Delta as a Matrix (Synergu/Antagonism colormap)

figure;
hold on;

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

% changed order v.2.0 - modification local only
InputDat.Avg      = InputDat.Avg(end:-1:2,2:end);
InputDat.Std      = InputDat.Std(end:-1:2,2:end);
InputDat.Ttest    = InputDat.Ttest(end:-1:2,2:end,:);
InputDat.Dose_ag1 = InputDat.Dose_ag1(end:-1:2);
InputDat.Dose_ag2 = InputDat.Dose_ag2(2:end);


%corrected v1.22
Nx = length(InputDat.Dose_ag2);
Ny = length(InputDat.Dose_ag1);

xlim([0 Nx]);
ylim([0 Ny]);

xdata = [0:(Nx-1) ; 1:Nx ; 1:Nx ; 0:(Nx-1)];
xdata = repmat(xdata,1,Ny);

ydata = [];
for jy = 0:Ny-1;
 ydata = horzcat(ydata,repmat([jy;jy;jy+1;jy+1],1,Nx));
end

map_syn_ant = colormap(jet);
map_syn_ant = map_syn_ant(end:-1:1,:);
colormap(map_syn_ant);

%Checking if Concentration is above limit
Above_Limit = zeros(size(InputDat.Avg));
% Above_Limit(:,InputDat.Dose_ag2>InputDat.D2max)=1;
% Above_Limit(InputDat.Dose_ag1>InputDat.D1max,:)=1;

Delta_SIG=InputDat.Avg;
% Displaying only significan data unless otherwise requested
if(RunOpt.T_Test_chk)
 Delta_SIG(InputDat.Ttest(:,:,1)==0) = 0.0;
end

% For more than 1 replicates only significant data is plotted
if(InputDat.N>1)
%  %corrected v1.22
%   Delta_Color = reshape((Delta_SIG')./120 + 0.5,1,Nx*Ny);
 %corrected v2.01
  Delta_Color = reshape((Delta_SIG')./100 + 0.5,1,Nx*Ny);
else
%  %corrected v1.22
%   Delta_Color = reshape((InputDat.Avg')./120 + 0.5,1,Nx*Ny);
 %corrected v2.01
  Delta_Color = reshape((InputDat.Avg')./100 + 0.5,1,Nx*Ny);
end
Delta_Color(Delta_Color>1)=1;
Delta_Color(Delta_Color<0)=0;
Delta_Color(isnan(Delta_Color))=0;
patch(xdata,ydata,Delta_Color);
caxis([0 1])

% Vectorizing data for patch display
patch_CMAX = round(reshape(Above_Limit',1,Nx*Ny)); 
patch_MEAN = round(reshape(InputDat.Avg',1,Nx*Ny));

%corrected v1.22
if(InputDat.N>1 && ~isempty(InputDat.Std))
  patch_STD = round(reshape(InputDat.Std',1,Nx*Ny));
end
%corrected v1.22
if(InputDat.N>1 && ~isempty(InputDat.Ttest))
  patch_TTest_SIG = reshape(InputDat.Ttest(:,:,1)',1,Nx*Ny);
  patch_TTest_PVAL = reshape(InputDat.Ttest(:,:,2)',1,Nx*Ny);
end

for k=1:Nx*Ny
    % Values beyond maximum highlighted in red
    if(patch_CMAX(k)==1)
        textcolor = 'r';
    else
        textcolor = [0.39 0.47 0.64];        
    end    
    % If more than 1 replicate, show STD and highlight colour only if
    % significant
    if(InputDat.N>1)
      text(xdata(1,k) + 0.2, ydata(1,k) + 0.7, num2str(patch_MEAN(k)),'Color',textcolor,'FontSize',15,'FontWeight','bold');
      text(xdata(1,k) + 0.2, ydata(1,k) + 0.35, strcat('+/- ',num2str(patch_STD(k))),'Color',textcolor,'FontSize',9,'FontWeight','bold');
      if(patch_TTest_SIG(k)==1 && RunOpt.T_Test_chk)
          if(patch_TTest_PVAL(k)<1e-4)
            text(xdata(1,k) +.25,ydata(1,k)+.0,'***','Color',textcolor,'FontSize',16);
          elseif(patch_TTest_PVAL(k)<1e-3)
            text(xdata(1,k) +.35,ydata(1,k)+.0,'**','Color',textcolor,'FontSize',16);
          else
            text(xdata(1,k) +.45,ydata(1,k)+.0,'*','Color',textcolor,'FontSize',16);
          end
      end
    % If only 1 replicate, no STD, always show colours
    else
      text(xdata(1,k) + 0.2, ydata(1,k) + 0.45, num2str(patch_MEAN(k)),'Color',[0.39 0.47 0.64],'FontSize',16,'FontWeight','bold');        
    end
end

set(gca,'YTick', 0.5:1:Ny+0.5);
set(gca,'YTickLabel',InputDat.Dose_ag1,'FontSize',14);

set(gca,'XTick', 0.5:1:Nx+0.5);
set(gca,'XTickLabel',InputDat.Dose_ag2,'FontSize',14);
% because changed order v.2.0
set(gca, 'XAxisLocation', 'top');


title(TitlePlot,'FontSize',16);
% because changed order v.2.0
set(get(gca,'title'),'Position',[Nx/2 -0.15*Ny])

xlabel(strcat(InputDat.Agent2,' [',InputDat.Unit2,']'),'FontSize',17);
ylabel(strcat(InputDat.Agent1,' [',InputDat.Unit1,']'),'FontSize',17);

H=colorbar;
set(H,'YTick',[])

switch plot_bar
  case 1
%      text(3.5,0.0,'Antagonism','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
%      text(3.5,0.75,'Synergy','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
     ylabel(H, 'Antagonism           Synergy','FontWeight','bold','FontSize',14)

  case 2
    text(3.5,0.1,'Synergy lack','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
    text(3.5,0.75,'Synergy','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
  case 3
    text(3.5,0.0,'Antagonism','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14)
    text(3.5,0.5,'Antagonism lack','Parent',H,'rotation',90,'FontWeight','bold','FontSize',14) 
end

% text(-0.9,Ny+1/Ny,['N=', num2str(InputDat.N)],'FontSize',18);
text(-Nx/10,Ny+Ny/10,['N=', num2str(InputDat.N)],'FontSize',18);

axis tight;

if RunOpt.Save
  saveas(gcf,char(strcat(InputDat.Folder,'/pdf/Matrix_',Title,'.pdf')), 'pdf')
  set(gca,'color','none')       
  export_fig(char(strcat(InputDat.Folder,'/png/Matrix_',Title)),'-png','-transparent')
  DATA_AVG = InputDat.Avg(end:-1:1,1:end);
  save(char(strcat(InputDat.Folder,'/data/Mean_',Title,'.txt')), 'DATA_AVG', '-ascii')
  DATA_STD = InputDat.Std(end:-1:1,1:end);
  save(char(strcat(InputDat.Folder,'/data/STD_',Title,'.txt')), 'DATA_STD', '-ascii')
end

end





