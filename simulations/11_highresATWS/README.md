# How to run this simulation

1. Preparation. Review **makeparameterdict.R** and **makeMLfiles.R** and run
   them in that order. This will populate the input files and create
   directories for the outputs.
1. Run **makebatch.py**. This will create batch .m files.
1. Run the batch files made in the previous steps. Use Raoul's
   **launch\_24\_batch.m** if appropriate.
1. Postprocessing files are in [postprocessing](postprocessing). Run
   **pp.py** and **sim_specific.py** in the
   directory. **inputs_ts.py** creates time series graphs.

# What's new in Simulation 11

* See [What's new in Simualation 10](../10_9x9x9x9/REASME.md)
* Increased resolution for 2 dimensions:
  * **AT** air temperature
  * **WS** wind speed

# Design

* See [What's new in Simualation 10](../10_9x9x9x9/README.md)
* **AT** and **WS** 51 levels, **TP** and **DOC** 1 level

## Levels

* **original** refers to the Langtjern original.

### **AT**

AT = original + (level - 26) * 0.12

### **WS**

WS = original * (2 ^ ((level - 26) * 0.08))

Level | Air Temp   | Wind Speed       | Total P             | DOC
--- | ------------ | ---------------- | ------------------- | -----------------
1 | original - 3.00 | original * 0.250 |   **original * 3.16** | **original * 0.316**
2 | original - 2.88 | original * 0.264 | |
26 | **original**   | **original**     |  |
51 | original + 3.0 | original * 4.000 |      |

```R

```



# Conversation with Tom 21 April 2017

There were a lot of interesting things but I make note here that we will look into increased resolution on **AT** and **WS** so that we might find some dual stability (in which different processes might dominate/explain the system dynamics). The last figure panel **b1** shows a rather complex response surface -- we may find a sweet spot or resonance frequency that is native/inherent to the lake physical and biological specs.

Tom had a good line to explain our straggle in finding a good steady state (here in this repository our straggle when we tried to run the model over a century, etc.) -- how the line reads, I slipped my mind out of it but I'll leave note about it.

The increased resolution on the two dimensions -- I try to finish by early June, in case something interesting comes out.
