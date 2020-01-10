function Data_smooth = Filter_ExpData_COMBI(ExpDataIn)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

% Filter data for HTS when replicates are not availables - here used only
% in quality checks.
 
h = fspecial('gaussian',3,0.75);      

% ONLY SMOOTHING COMBINATION DATA
n = size(ExpDataIn.Resp(:,:,1),1) - 1;
m = size(ExpDataIn.Resp(:,:,1),2) - 1;
Data_rough = zeros(n,m);
    
for irepli=1:ExpDataIn.N      
   Data_rough = ExpDataIn.Resp(2:end,2:end,irepli);        
   Data_smooth = imfilter( Data_rough,h,'replicate');      
end
    
end