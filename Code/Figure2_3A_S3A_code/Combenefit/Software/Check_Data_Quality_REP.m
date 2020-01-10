function QA = Check_Data_Quality_REP(ExpDat)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Filter data for HTS when replicates are not availables

% QA=1 IS FOR OK
QA=1;

% IN FUTURE VERSION WOULD BE NICE TO INCORPORATE CHOICE OF CUTOFF IN INTERFACE
% MAX DOSE_RESPONSE CUTOFF
MaxDR = 125;
% MIN DOSE_RESPONSE CUTOFF
MinDR = -10;
% MAX DIFF WITH FILTERED DATA (EXCLUDE TOO STRONG FLUCTUATIONS)
MaxDelta = 25.0

% CHECKING:
for irepli=1:ExpDat.N  
    
% MAX DOSE-RESPONSE
if( max(max(ExpDat.Resp(:,:,irepli))) >MaxDR)
  QA = -1;  

% MIN DOSE-RESPONSE
elseif( min(min(ExpDat.Resp(:,:,irepli))) <MinDR)
  QA = -2;  

%MAX difference with filtered data
else
DataCombiSmooth = Filter_ExpData_COMBI(ExpDat)
[nx,ny]=size(ExpDat.Resp(:,:,irepli))
Delta= abs(DataCombiSmooth-ExpDat.Resp(2:nx,2:ny,irepli))
  if( max(max(Delta)) >MaxDelta)
    QA = -3;
  end
end
end
    
end