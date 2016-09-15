# How to run this simulation

1. Preparation. Review makeparameterdict.R and makeMLfiles.R and run
   then in that order.
1. Run response.surface.run.m in Matlab
1. Postprocessing files are in {postprocessing}[postprocessing].

#Parameters

* Air temperature **T**
* Total P concentration **TP**
* TP linear reduction **TPR**
* DOC concentration **DOC**

Last three are controlled using runoff input to MyLake. This time
there's no change in MyLake parameters. 

## Levels

Level | Temperature | Total P | TP linear reduction | DOC
--- | --- | --- | --- | ---
1 | original - 5 | original | Total P remains | original 
2 | original  | original * 10  | Total P diminishing to 55 % at the end | original * 10
3 | original + 5 | original * 100 | Total P diminishing to 10 % at the end | original * 100

(By the way Total P cannot be reduced to zero; hence 10 % at the end.)

Eventually increase resolution to 5x5x5x5 or 10x10x10x10?

Better scales? 

# Responses

* Water temperature
* Chl concentration
* Total P concentration
* O2 saturation (absolute)

## Primary comparison

* Maximum Chl concentration on surface in 2013 **R1**
* Number of surface anoxia days (abs < 0.01) in 2013 **R2**

# Tentative results

Colours are standardized for **R1** and **R2**.

**file name:** First+Second on Response.png

First on x axis (left to right), Second on y axis (top to bottom). 

See the 12 tentative files in [figures folder](figures).
