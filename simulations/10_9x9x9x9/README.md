# How to run this simulation

1. Preparation. Review makeparameterdict.R and makeMLfiles.R and run
   them in that order. This will populate the input files and create
   directories for the outputs. 
1. Run makebatch.py. This will create batch .m files.
1. Run the batch files made in the previous steps. Use Raoul's
   launch__24__batch.m if appropriate. 
1. Postprocessing files are in [postprocessing](postprocessing). Run
   pp.py and sim_specific in the directory. 

# What's new in Simulation 10

* Uses Igor's late February versions, except:
  * `dz = 0.5`
  * Ice output `His` outputs
* dimensions 9 by 9 by 9 by 9
  * with the base reference to be at 5 by 5 by 5 by 5
  * this base reference is not the original Langtjern weather, see
    table below

# Design

* Inputs taken from real Langtjern weather
  * with base being modified
  * all levels also modification of the original
  * 4 years (2010-2013)
* Simulation lasts 8 years (2010-2017)
  * repeats first 4 years twice
  * use the last 4 years (2014-2017) for reporting purpose
  * does that mean that water-sediment is in quasi steady state?
    * water part seem fine (short residence time ? days)
	* still don't know if the sediment is (and will ever be) in steady
      state with water
	* basically not tested but beyond our scope this time...?
* The levels control the scale of the inputs, called **dimensions**
  * Air temperature **AT**
  * Wind speed **WS**
  * Total P concentration **TP**
  * DOC concentration **DOC**
* The levels (1 though 9) are chosen so that
  * At the extremes the inputs are almost unrealistic but still
    interesting, and the model does not crash
  * At the base (5), the **responses** are about at the middle in
    scale
	  * makes sure that when keeping 3 dimensions at the base level 5,
        we can maximise the contrast (dynamic range) of the last
        dimension. For example, with levels AT1-AT9 but fixing WS5 TP5
        DOC5, none of the last three (WS5, TP5, DOC5) should not
        dominate how AT1-9 plays a role if any. 








## Levels

Level | Air Temp   | Wind Speed       | Total P             | DOC
--- | ------------ | ---------------- | ------------------- | -----------------
1 | original - 3.0 | original * 0.250 | original * 0.316    | original * 0.0316 
2 | original - 2.0 | original * 0.353 | original * 0.562    | original * 0.0562 
3 | original - 1.0 | original * 0.500 | original * 1.00     | original * 0.100 
4 | original - 0.5 | original * 0.707 | original * 1.78     | original * 0.178 
5 | **original**   | **original**     | **original * 3.16** | **original * 0.316** 
6 | original - 3.0 | original * 1.414 | original * 5.62     | original * 0.562 
7 | original - 3.0 | original * 2.000 | original * 10.0     | original * 1.00
8 | original - 3.0 | original * 2.828 | original * 17.8     | original * 1.78 
9 | original - 3.0 | original * 4.000 | original * 31.6     | original * 3.16 

```R
> level <- 1:9
> (2 ^ ((level - 5) / 2))
[1] 0.2500000 0.3535534 0.5000000 0.7071068 1.0000000 1.4142136 2.0000000
[8] 2.8284271 4.0000000
> (10 ^ ((level - 3) / 4))
[1]  0.3162278  0.5623413  1.0000000  1.7782794  3.1622777  5.6234133 10.0000000
[8] 17.7827941 31.6227766
> (10 ^ ((level - 7)/4))
[1] 0.03162278 0.05623413 0.10000000 0.17782794 0.31622777 0.56234133 1.00000000
[8] 1.77827941 3.16227766
>
```

# Responses

* no. hypoxia days per year (at 3000 micro g L-1) (d y-1)
* no. anoxia days per year (at 3000 micro g L-1) (d y-1)
* mean annual maximum chl concentration at surface (micro g L-1)
* mean JJA chl concentration at surface (micro g L-1)
* mean annual ice cover duration (d y-1)
* mean JJ mixing depth (m from the surface)

## Model crashes

None this time

## Input time series (2010-2013)

![](postprocessing/inputs/allinputs.png)

## Response surfaces 

![](postprocessing/RSver3.png)

## Other plots

See [impacts\_of\_dimenions.md](impacts_of_dimenions.md) for the following:
* AT1 WS5 TP5 DOC5 
* AT9 WS5 TP5 DOC5 
* AT5 WS1 TP5 DOC5 
* AT5 WS9 TP5 DOC5 
* AT5 WS5 TP1 DOC5 
* AT5 WS5 TP9 DOC5 
* AT5 WS5 TP5 DOC1 
* AT5 WS5 TP5 DOC9 

