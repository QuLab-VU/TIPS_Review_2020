function FolderOut = CREATE_FOLDER(Dat,saveornot,foldercase)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

  switch foldercase
%     case 0
%       if (saveornot && ~exist([Dat.Folder '/Dose-response curves'], 'dir')) 
%         mkdir(Dat.Folder,'Dose-response curves')
%         mkdir(Dat.Folder,'Dose-response curves/pdf')
%         mkdir(Dat.Folder,'Dose-response curves/png')
%         mkdir(Dat.Folder,'Dose-response curves/parameters')
%       end
    case 1
      if (saveornot && ~exist([Dat.Folder '/Dose-response'], 'dir'))
        mkdir(Dat.Folder,'Dose-response')
        mkdir(Dat.Folder,'Dose-response/pdf')
        mkdir(Dat.Folder,'Dose-response/png')
        mkdir(Dat.Folder,'Dose-response/data')
      end
      FolderOut = Dat.Folder;
    case 2 
      if (saveornot && ~exist([Dat.Folder '/Analysis LOEWE'], 'dir'))
          mkdir(Dat.Folder,'Analysis LOEWE')
          mkdir(Dat.Folder,'Analysis LOEWE/pdf')
          mkdir(Dat.Folder,'Analysis LOEWE/png') 
          mkdir(Dat.Folder,'Analysis LOEWE/data')
      end
      FolderOut = strcat(Dat.Folder,'/Analysis LOEWE');
    case 3
      if (saveornot && ~exist([Dat.Folder '/Analysis BLISS'], 'dir'))
        mkdir(Dat.Folder,'Analysis BLISS')
        mkdir(Dat.Folder,'Analysis BLISS/pdf')
        mkdir(Dat.Folder,'Analysis BLISS/png') 
        mkdir(Dat.Folder,'Analysis BLISS/data')
      end
      FolderOut = strcat(Dat.Folder,'/Analysis BLISS');
    case 4
      if (saveornot && ~exist([Dat.Folder '/Analysis HSA'], 'dir'))
        mkdir(Dat.Folder,'Analysis HSA')
        mkdir(Dat.Folder,'Analysis HSA/pdf')
        mkdir(Dat.Folder,'Analysis HSA/png') 
        mkdir(Dat.Folder,'Analysis HSA/data')
      end
      FolderOut = strcat(Dat.Folder,'/Analysis HSA');
  end
end