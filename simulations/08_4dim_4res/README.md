# How to run this simulation TESTING

1. Preparation. Review makeparameterdict.R and makeMLfiles_testing.R and run
   them in that order. This will populate the input files and create
   directories for the outputs. 
1. Run makebatch_testing.py. This will create batch .m files.
1. Run the batch files made in the previous steps. Use Raoul's
   launch__24__batch_testing.m if appropriate. 
1. Postprocessing files are in [postprocessing_testing](postprocessing_testing). Run
   pp_testing.py and sim__specific__testing.py in the directory. 

# How to run this simulation ORIGINAL

1. Preparation. Review makeparameterdict.R and makeMLfiles.R and run
   them in that order. This will populate the input files and create
   directories for the outputs. 
1. Run makebatch.py. This will create batch .m files.
1. Run the batch files made in the previous steps. Use Raoul's
   launch__24__batch.m if appropriate. 
1. Postprocessing files are in [postprocessing](postprocessing). Run
   pp.py and sim_specific in the directory. 

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
1 | original - 3.0 | original * 0.25 | original * 0.33 | original * 0.0316 
2 | original - 1.0 | original * 0.50 | original | original * 0.010
3 | **original** | **original** | **original * 3.0** |  **original * 0.316** 
4 | original + 1.0 | original * 2.0 | original * 9.0 | original * 1.00
5 | original + 3.0 | original * 4.0 | original * 27 | original * 3.16

# Responses

* something about water temperature / ice
* something about oxygen / anoxia
* something about light / colour
* something about algae bloom

## model crashes

None this time

# Raw outputs

## impact of **T**

![](postprocessing/inputs/Air Temperature.png) 
![](postprocessing/results_raw/Air Temperature.png) 

## impact of **WS**

![](postprocessing/inputs/Wind Speed.png) 
![](postprocessing/results_raw/Wind Speed.png) 

## impact of **TP**

![](postprocessing/inputs/Total P.png) 
![](postprocessing/results_raw/Total P.png) 

## impact of **DOC**

![](postprocessing/inputs/DOC.png) 
![](postprocessing/results_raw/DOC.png) 




## Response surfaces

![](postprocessing/RSver2.png)

# old TODO

- make wind speed milder
- find good air temperature levels that work
- calculate and report the following variables
  - something about light
  - something about temerature profile, phenology of stratification
  - try other definitions of anoxia and algal bloom
- increase the resolution (?)
- set up the NIVA server workflow 
- confirm the following
  - time span seems fine (2010-2013 input repeated twice, use the
    2014-2017 for reporting)
  - we keep total P as a dimension. Total P seems to affect only the P scaling (?)
    and that might mean it's not 

# new TODO

- more response surfaces (more columns)
