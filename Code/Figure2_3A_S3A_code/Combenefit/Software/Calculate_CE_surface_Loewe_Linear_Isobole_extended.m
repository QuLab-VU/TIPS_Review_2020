function [ Linear_Isobole_Matrix ] = Calculate_CE_surface_Loewe_Linear_Isobole_extended(ParamsD1,ParamsD2, C1, C2)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Generate C-E surface based on Loewe Linear Isobole

  Linear_Isobole_Matrix = zeros(length(C1),length(C2));

  k1 = [ParamsD1, 100];
  k2 = [ParamsD2, 100];

  for i=1:length(C1) 
    for j=1:length(C2) 
        if C2(j)==0&&C1(i)==0
            Linear_Isobole_Matrix(i,j)  = 100;
        else
            Linear_Isobole_Matrix(i,j)  =  E_Linear_Isobole_extended(k1,k2,C1(i),C2(j));
        end
    end
  end

end
