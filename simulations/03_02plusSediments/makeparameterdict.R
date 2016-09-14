## this file creates the file intermediate/parameterdict.csv
## -- provides the combinations of the parameter levels
## -- convenient because I want to avoid telling Matlab parameter settings
##    instead of telling parameter settings, just give Matlab the folders and run it


n1 <- 3
n2 <- 3
n3 <- 3
n4 <- 3

x1 <- 1:n1
x2 <- 1:n2
x3 <- 1:n3
x4 <- 1:n4

d <- expand.grid(x1, x2, x3, x4)
d[['simid']] <- 1:nrow(d)

write.csv(d, file='intermediate/parameterdict.csv',
          row.names=FALSE)


## > d
##    Var1 Var2 Var3 Var4 simid
## 1     1    1    1    1     1
## 2     2    1    1    1     2
## 3     3    1    1    1     3
## 4     1    2    1    1     4
## 5     2    2    1    1     5
## 6     3    2    1    1     6
## 7     1    3    1    1     7
##          **snipped**
## 78    3    2    3    3    78
## 79    1    3    3    3    79
## 80    2    3    3    3    80
## 81    3    3    3    3    81

