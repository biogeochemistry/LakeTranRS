# How to run this simulation

1. Preparation. Review makeparameterdict.R and makeMLfiles.R and run
   them in that order.
1. Run response.surface.run.m in Matlab
1. Postprocessing files are in [postprocessing](postprocessing).

#Parameters

* Air temperature **T**
* Wind speed **W**
* Total P concentration **TP**
* DOC concentration **DOC**

## Levels

Temperature variation is on the lower end because of failing at high
temperature levels in simulation number 06. 

Level | Temperature | Wind speed | Total P | DOC
--- | --- | --- | --- | ---
1 | original - 3.0 | original * 0.100 | original * 0.316 | original * 0.316 
2 | original - 1.5 | original * 0.316 | **original** | **original** 
3 | **original** | **original** | original * 3.16 |  original * 3.16 
4 | original + 1.5 | original * 3.16 | original * 10.0 | original * 10.0
5 | original + 3.0 | original * 10.0 | original * 31.6 | original * 31.6

### Observation

to be listed

# Responses

* something about water temperature / ice
* something about oxygen / anoxia
* something about light / colour
* something about algae bloom

## model crashes
to be listed

## Primary comparison

TBD

# Tentative results

to come
