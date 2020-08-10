library(stats)
library(readxl)
library(testforDEP)
setwd('C:/Users/Benjamin/Dropbox/recherche/bitcoin/modèle SS/donnees_et_codes')
base=data.frame(read_xlsx('database.xlsx',col_names=F))
R=base[,1]
X=log(R[724:3003])-log(R[723:3002])
acf(X,lag.max=30,type="correlation")