function metrics = CollectMetrics(ModelEstim)
% The MIT License (MIT)
% 
% Copyright (c) 2015 Giovanni Di Veroli

      metrics(1,1) = ModelEstim.MaxSyn;
      metrics(1,2) = ModelEstim.SynVol;
      metrics(1,3) = ModelEstim.WeiSynVol;
      metrics(1,4) = ModelEstim.SynSpread;
      metrics(1,5) = ModelEstim.C1Syn;
      metrics(1,6) = ModelEstim.C2Syn;
      
      metrics(1,7) = ModelEstim.MaxAnt;
      metrics(1,8) = ModelEstim.AntVol;
      metrics(1,9) = ModelEstim.WeiAntVol;
      metrics(1,10) = ModelEstim.AntSpread;
      metrics(1,11) = ModelEstim.C1Ant;
      metrics(1,12) = ModelEstim.C2Ant;
      
      metrics(1,13) = ModelEstim.TotVol;
      metrics(1,14) = ModelEstim.TotWeiVol;


end