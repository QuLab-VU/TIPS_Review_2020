function MatrixPlot(InputDat,saveornot,matrix_case) 
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

% Displays loaded experimental data and generated synergy models as 
% matrix plots

figure;
hold on;

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

%corrected v1.22 + changed order v.2.0
% Data_Color = reshape(InputDat.Avg'./110,1,Nx*Ny);
Data_reversed = InputDat.Avg(end:-1:1,1:end);
Data_Color = reshape(Data_reversed'./110,1,Nx*Ny);


Data_Color(Data_Color>1)=1;
Data_Color(Data_Color<0)=0;
Data_Color(isnan(Data_Color))=0;
patch(xdata,ydata,Data_Color);
colormap(pink);
caxis([0 1]);

% changed order v.2.0
% patch_MEAN = round(reshape(InputDat.Avg',1,Nx*Ny));
patch_MEAN = round(reshape(Data_reversed',1,Nx*Ny));

if(~isempty(InputDat.Std))
% changed order v.2.0
%   patch_STD = round(reshape(InputDat.Std',1,Nx*Ny));
  Data_STD_reversed = InputDat.Std(end:-1:1,1:end);
  patch_STD = round(reshape(Data_STD_reversed',1,Nx*Ny));    
end
for k=1:Nx*Ny
%     if(InputDat.N>1) doesnt work for models
    if(~isempty(InputDat.Std))
      text(xdata(1,k) + 0.2, ydata(1,k) + 0.7, num2str(patch_MEAN(k)),'Color',[0.39 0.47 0.64],'FontSize',16,'FontWeight','bold');
      text(xdata(1,k) + 0.2, ydata(1,k) + 0.3, strcat('+/- ',num2str(patch_STD(k))),'Color',[0.39 0.47 0.64],'FontSize',10,'FontWeight','bold');
    else
      text(xdata(1,k) + 0.2, ydata(1,k) + 0.45, num2str(patch_MEAN(k)),'Color',[0.39 0.47 0.64],'FontSize',16,'FontWeight','bold');        
    end
end

% changed order v.2.0
set(gca,'YTick', 0.5:1:Ny+0.5);
% set(gca,'YTickLabel',InputDat.Dose_ag1,'FontSize',14);
set(gca,'YTickLabel',InputDat.Dose_ag1(end:-1:1),'FontSize',14);

set(gca,'XTick', 0.5:1:Nx+0.5);
set(gca,'XTickLabel',InputDat.Dose_ag2,'FontSize',14);

% changed order v.2.0
set(gca, 'XAxisLocation', 'top');

title(TitlePlot,'FontSize',16);

% changed order v.2.0
set(get(gca,'title'),'Position',[Nx/2 -0.15*Ny])

xlabel(strcat(InputDat.Agent2,' [',InputDat.Unit2,']'),'FontSize',17);
ylabel(strcat(InputDat.Agent1,' [',InputDat.Unit1,']'),'FontSize',17);

h = colorbar;
set(h,'YTick',[]);
% text(3.5,0.35,'% Control','Parent',h,'rotation',90,'FontWeight','bold','FontSize',14);
ylabel(h, '% Control','FontWeight','bold','FontSize',14)
axis tight;

if saveornot
  DATA_AVG = InputDat.Avg;
  switch matrix_case
    case 1
        saveas(gcf,char(strcat(InputDat.Folder,'/Dose-response/pdf/Matrix_',Title,'.pdf')), 'pdf')
        set(gca,'color','none')
        export_fig(char(strcat(InputDat.Folder,'/Dose-response/png/Matrix_',Title)),'-png','-transparent')
        save(char(strcat(InputDat.Folder,'/Dose-response/data/Mean_',Title,'.txt')), 'DATA_AVG', '-ascii')
        DATA_STD = InputDat.Std;
        save(char(strcat(InputDat.Folder,'/Dose-response/data/STD_',Title,'.txt')), 'DATA_STD', '-ascii')
    otherwise
        saveas(gcf,char(strcat(InputDat.Folder,'/pdf/Matrix_',Title,'.pdf')), 'pdf')
        set(gca,'color','none')       
        export_fig(char(strcat(InputDat.Folder,'/png/Matrix_',Title)),'-png','-transparent')
        save(char(strcat(InputDat.Folder,'/data/Mean_',Title,'.txt')), 'DATA_AVG', '-ascii')
  end 
end
    
end





