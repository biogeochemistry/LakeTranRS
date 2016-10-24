# How to run this simulation

1. Preparation. Review makeparameterdict.R and makeMLfiles.R and run
   them in that order.
1. Run response.surface.run.m in Matlab
1. Postprocessing files are in [postprocessing](postprocessing).


# Checking results using the July verions

#Parameters

* Air temperature **T**
* Total P concentration **TP**
* ~~ Fe3+ concentration FE ~~
* DOC concentration **DOC**

Last three are controlled using runoff input to MyLake. This time
there's no change in MyLake parameters. 

## Levels

Temperature variation is on the lower end because of failing at high
temperature levels in simulation number 06. 

Level | Temperature | Total P | ~~Fe3+~~ | DOC
--- | --- | --- | --- | ---
1 | original - 3.0 | original * 0.25 | ~~zero~~ | original * 0.25
2 | original - 2.5  | original * 0.5  | ~~0.5~~ | original * 0.5
3 | original - 2.0 | **original** | ~~1.0~~ | **original**
4 | original - 1.5 | original * 2.0 | ~~2.0~~ | original * 2.0
5 | original - 1.0 | original * 4.0 | ~~4.0~~ | original * 4.0 
6 | original - 0.5 | original * 8.0 | ~~8.0~~ | original * 8.0 
7 | **original** | original * 16 | ~~16~~ | original * 16
8 | original + 0.5 | original * 32 | ~~32~~ | original * 32
9 | original + 1.0 | original * 64 | ~~64~~ | original * 64
10 | original + 1.5 | original * 128 | ~~128~~ | original * 128


### Observation

to be listed

# Responses

* Water temperature
* Chl concentration
* Total P concentration
* O2 saturation (absolute)


## model crashes
to be listed

## Primary comparison

* Maximum Chl concentration on surface in 2013 **R1**
* Number of surface anoxia days (abs < 0.01) in 2013 **R2**
