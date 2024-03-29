function E = E_Linear_Isobole_extended(k1, k2, D1,D2)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli
%
% Solvee extended version of linear isobole equation

  if(doseresponse(k1, D1)<k2(3))
      E=doseresponse(k1, D1);
  elseif(doseresponse(k2, D2)<k1(3))
      E=doseresponse(k2, D2);
  else
    FUN_MIN = @(x)Fun_Lin_Iso(x,k1, k2, D1,D2);
    options = optimset('Display','off','MaxIter',50000,'MaxFunEvals',50000,'TolFun',1e-8,'TolX',1e-8);
    UB=min(doseresponse(k1, D1),doseresponse(k2, D2));
    LB=max(k1(3),k2(3));
    if(abs((UB-LB)/UB)>1e-4)
      [E,fval,exitflag] =  fminsearchbnd(FUN_MIN,100,LB,UB,options);
      if(fval>1e-3 || exitflag<=0)
        E=NaN;
      end
    else
      E=LB;
    end
   
  end
end

