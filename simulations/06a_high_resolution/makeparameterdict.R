## this file creates the file intermediate/parameterdict.csv
## -- provides the combinations of the parameter levels
## -- convenient because I want to avoid telling Matlab parameter settings
##    instead of telling parameter settings, just give Matlab the folders and run it


n1 <- 10
n2 <- 10
n3 <- 10
n4 <- 10

x1 <- 1:n1
x2 <- 1:n2
x3 <- 1:n3
x4 <- 1:n4

d <- expand.grid(x1, x2, x3, x4)
d[['simid']] <- 1:nrow(d)

write.csv(d, file='intermediate/parameterdict.csv',
          row.names=FALSE)

