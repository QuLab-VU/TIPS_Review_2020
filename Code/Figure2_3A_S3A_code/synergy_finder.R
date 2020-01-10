
#Install the correct package
#if (!requireNamespace("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
#BiocManager::install("synergyfinder")

#setwd('/home/meyerct6/Papers/papers_in_progress/TIPS_Review_2019_submission/Code/Figure2_3A_S3A_code')
library(synergyfinder)
#Check version.  Must be 2.0.3 according to Reviewer #1
#packageVersion(synergyfinder)

fil <- list.files('../../Data/Figure2_data/synF/',pattern = '*fmt.csv')
for (f in fil){
  print(f)
  df <- read.csv(paste('../../Data/Figure2_data/synF/',f,sep=''))
  dose.response.mat = ReshapeData(df,data.type = "viability")
  for (mth in c('ZIP','Loewe','Bliss','HSA')){
    tryCatch({synergy.score <- CalculateSynergy(data = dose.response.mat,method = mth,adjusted=TRUE)
             write.csv(synergy.score$scores[[1]],file = paste('../../Data/Figure2_data/synF/',strsplit(f,'\\.')[[1]][1],'_',mth,".csv",sep=''))},
             error = function(err) {write.csv(NaN,file = paste('../../Data/Figure2_data/synF/',strsplit(f,'\\.')[[1]][1],'_',mth,".csv",sep=''))})
  }
}

####For testing....
# df <- read.csv('clobetasonebutyrate_decoquinate_PLASMODIUM_FALCIPARUM_3D7_synergyFinder_fmt.csv')
# dose.response.mat = ReshapeData(df,data.type = "viability")
# print('SynergyFinder:')
# for (mth in c('ZIP','Loewe','Bliss','HSA')){
#   synergy.score <- CalculateSynergy(data = dose.response.mat,method = mth,correction = FALSE,Emin = NA, Emax = NA)
#   print(paste0('Mean ',mth,':',mean(synergy.score$scores[[1]])))
#   PlotSynergy(synergy.score, type = "all", save.file = TRUE)
#   write.csv(synergy.score$scores[[1]],file = paste("synergy_finder_",mth,".csv",sep=''))
# }
# print('DrugComb')
# dc <- read.csv('DataTable5d30d0259190f56533.csv')
# print(paste0('Mean Loewe:',dc$synergy_loewe))
# print(paste0('Mean Bliss:',dc$synergy_bliss))
# print(paste0('Mean HSA:',dc$synergy_hsa))
