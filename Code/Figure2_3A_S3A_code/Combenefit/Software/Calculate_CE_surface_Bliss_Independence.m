function [ Bliss_Matrix ] = Calculate_CE_surface_Bliss_Independence(ParamsD1,ParamsD2, C1, C2)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Bliss model used to calculate surface
  Bliss_Matrix = doseresponse_EC0_100(ParamsD1,C1) * ...
                     doseresponse_EC0_100(ParamsD2,C2)/100 ;
end
