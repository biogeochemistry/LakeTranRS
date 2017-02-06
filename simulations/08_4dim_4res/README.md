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

![](inputs/postprocessing/Air Temperature.png) 
![](results_raw/postprocessing/AT colder.png) 
![](results_raw/postprocessing/AT warmer.png) 
![](results_raw/postprocessing/Air Temperature.png) 

## impact of **WS**

![](inputs/postprocessing/Wind Speed.png) 
![](results_raw/postprocessing/WS calmer.png) 
![](results_raw/postprocessing/WS stronger.png) 
![](results_raw/postprocessing/Wind Speed.png) 

## impact of **TP**

![](inputs/postprocessing/Total P.png) 
![](results_raw/postprocessing/TP lower.png) 
![](results_raw/postprocessing/TP higher.png) 
![](results_raw/postprocessing/Total P.png) 

## impact of **DOC**

![](inputs/postprocessing/DOC.png) 
![](results_raw/postprocessing/DOC lower.png) 
![](results_raw/postprocessing/DOC higher.png) 
![](results_raw/postprocessing/DOC.png) 




## Primary comparison

TBD

# Tentative results

to come
