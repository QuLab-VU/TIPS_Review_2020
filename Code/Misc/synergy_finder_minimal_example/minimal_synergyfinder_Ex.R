
#Install the correct package
#if (!requireNamespace("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
#BiocManager::install("synergyfinder")

#setwd('/home/meyerct6/Papers/papers_in_progress/TIPS_Review_2019_submission/Code/Figure2_3A_S3A_code')
library(synergyfinder)
#Check version.  Must be 2.0.3 according to Reviewer #1
#packageVersion(synergyfinder)

fil <- 'emetine_nvpbgt226_PLASMODIUM_FALCIPARUM_HB3_synergyFinder_fmt.csv'
df <- read.csv(fil)
dose.response.mat = ReshapeData(df,data.type = "viability")
mth = 'Bliss'
synergy.score <- CalculateSynergy(data = dose.response.mat,method = mth,adjusted=FALSE)
adj_synergy.score <- CalculateSynergy(data = dose.response.mat,method = mth,adjusted=TRUE)

col<- colorRampPalette(c("red", "white", "blue"))(256)
heatmap(synergy.score$scores[[1]],Rowv=NA,Colv=NA,col=col,main='Bliss Not Adjusted')


col<- colorRampPalette(c("red", "white", "blue"))(256)
heatmap(adj_synergy.score$scores[[1]],Rowv=NA,Colv=NA,col=col,main='Bliss Adjusted')
