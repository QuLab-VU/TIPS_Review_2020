function [ HSA_Matrix ] = Calculate_CE_surface_HSA(ParamsD1,ParamsD2, C1, C2)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Highest single agent effect  

  EC1 = doseresponse_EC0_100(ParamsD1,C1) * ones(1,length(C2));
  EC2 = ones(length(C1),1) * doseresponse_EC0_100(ParamsD2,C2); 
  HSA_Matrix = min(EC1,EC2);
  
end
