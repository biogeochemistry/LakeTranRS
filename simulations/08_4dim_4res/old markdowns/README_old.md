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

Model crashes happened with certain combinations of **T** and **WS**.

\ | **WS1** | **WS2** | **WS3 original** | **WS4** | **WS5** 
--- | --- | --- | --- | --- | ---
**T1** | ok | ok | ok | ok | fails
**T2** | ok | ok | ok | ok | fails (see note below) 
**T3 original** | ok | ok | ok | ok | fails
**T4** | fails | fails | ok | fails | fails
**T5** | ok | ok | ok | fails | fails

Out of the 25 cases (5 **TP** x 5 **DOC**) for **T2W5** combinations:
- the model crashed before finishing 20 cases 
- the model finished runs but created imaginary numbers somewhere
  halfway into simulation in 5 cases
  - T2W5P1C3 
  - T2W5P1C5 
  - T2W5P2C2 
  - T2W5P3C4 
  - T2W5P3C5

I don't know
- why **T4** failed more often than **T5**, or why **T4W3** is okay
- why **T2W5** created imaginary numbers in some cases

I have not looked into reasons why **W5** crashes, but 'educated
guesses' are possible

# Raw outputs

## impact of **T**

![](postprocessing/inputs_old/Air Temperature.png) 
![](postprocessing/results_raw_old/AT colder.png) 
![](postprocessing/results_raw_old/AT warmer.png) 
![](postprocessing/results_raw_old/Air Temperature.png) 

## impact of **WS**

![](postprocessing/inputs_old/Wind Speed.png) 
![](postprocessing/results_raw_old/WS calmer.png) 
![](postprocessing/results_raw_old/WS stronger.png) 
![](postprocessing/results_raw_old/Wind Speed.png) 

## impact of **TP**

![](postprocessing/inputs_old/Total P.png) 
![](postprocessing/results_raw_old/TP lower.png) 
![](postprocessing/results_raw_old/TP higher.png) 
![](postprocessing/results_raw_old/Total P.png) 

## impact of **DOC**

![](postprocessing/inputs_old/DOC.png) 
![](postprocessing/results_raw_old/DOC lower.png) 
![](postprocessing/results_raw_old/DOC higher.png) 
![](postprocessing/results_raw_old/DOC.png) 




## Response surfaces

![](postprocessing/RSver1_old.png)

# TODO

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
