## this file creates the input files
## see README.md for details
## the key line is   data <- f4(f3(f2(f1(original, L1), L2), L3), L4)
## 1. read the template, 2. apply the above line, 3. write the result

original <- read.table('../input/LAE_input.txt', sep='\t', skip=1, header=TRUE)

dict <- read.csv('intermediate/parameterdict.csv')

f1 <- function (d, level) {
  d[['AirTemperature']] <- d[['AirTemperature']] - 5 + 5 * (level - 1)
  return (d)
}

f2 <- function (d, level) {
  d[['InflowTP']] <- d[['InflowTP']] * (10 ^ (level - 1))
  d[['InflowDOP']] <- d[['InflowDOP']] * (10 ^ (level - 1))
  d[['InflowChla']] <- d[['InflowChla']] * (10 ^ (level - 1))
  return (d)
}

f3 <- function (d, level) {
  diminish <- seq(from=1, to=1-(level-1)*0.45, length=nrow(d))
  d[['InflowTP']] <- d[['InflowTP']] * diminish
  d[['InflowDOP']] <- d[['InflowDOP']] * diminish
  d[['InflowChla']] <- d[['InflowChla']] * diminish
  return (d)
}

f4 <- function (d, level) {
  d[['InflowDOC']] <- d[['InflowDOC']] * (5 ^ (level - 1))
  return (d)
}

for (s in 1:nrow(dict)) {
  L1 <- dict[s, 1]
  L2 <- dict[s, 2]
  L3 <- dict[s, 3]
  L4 <- dict[s, 4]
  simid <- dict[s, 5] ## should be same as s anyway
  data <- f4(f3(f2(f1(original, L1), L2), L3), L4)
  pathname <- sprintf('intermediate/id/%02d/input.txt', simid)
  dirname <- sprintf('intermediate/id/%02d', simid)
  dirname2 <- sprintf('simulations/id/%02d', simid)
  if (!dir.exists('intermediate')) { dir.create('intermediate') }
  if (!dir.exists('intermediate/id')) { dir.create('intermediate/id') }
  if (!dir.exists(dirname)) { dir.create(dirname) }
  if (!dir.exists('simulations')) { dir.create('simulations') }
  if (!dir.exists('simulations/id')) { dir.create('simulations/id') }
  if (!dir.exists(dirname2)) { dir.create(dirname2) }
  else { unlink(dirname2, recursive = TRUE) ; dir.create(dirname2) }
  if (file.exists(pathname)) { file.remove(pathname) }
  ## delete existing, because we want to append later
  f <- file(pathname)
  writeLines(sprintf('Simulation_AT%d_TP%d_TPR%d_DOC%d', L1, L2, L3, L4), f)
  close(f)
  write.table(data, file=pathname, append=TRUE, sep='\t', eol='\r\n', na='NaN',
              quote=FALSE, row.names=FALSE)
}

  

