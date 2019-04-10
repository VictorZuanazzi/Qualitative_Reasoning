# Qualitative Reasoning

This project is the final assignment for Knowledge Representation VU Spring 2019.

Group: Victor Zuanazzi and David Speck

In this project we developed a qualitative reasoning engine and applied it to a bath tube causal model. 

## System description
Consider containers such as bathtubs and kitchen sinks, which can be filled with water (e.g. via a tab) and emptied (e.g. via a drain). What behaviours can occur with such container systems? Your assignment is to create a programme that reasons about the possible behaviours of such systems and generates a state-graph showing all possible behaviours.
Start with the following details:

**Quantities**
- Inflow (of water into the container)
- Outflow (of water out of the container)
- Volume (of the water in the container)

**Quantity spaces**
- Inflow: [0, +]
- Outflow and Volume: [0, +, max]

**Dependencies**
- I+(Inflow, Volume) – The amount of inflow increases the volume
- I–(Outflow, Volume) – The amount of outflow decreases the volume
- P+(Volume, Outflow) – Outflow changes are proportional to volume changes
- VC(Volume(max), Outflow(max)) –The outflow is at its highest value (max), when
the volume is at its highest value (also max).
- VC(Volume(0), Outflow(0)) – There is no outflow, when there is no volume.

## Dependencies

Use the `environment.yml` file to re-create the conda environment used during development. To do so run:
```
conda env create -f environment.yml
```

## How to run

To re-run the QR engine for the assignment causal model simply run:
```
python src/main.py 
```

To use it with another causal model use the following lines in python:
```
from qr_engine import qr_engine

# run QR engine with a blue print of a state 
# and a list of relations
states = qr_engine(blue_print, relations)

# util to plot the resulting state graph
make_state_graph(states, 'state_graph')
```
Check `src/main.py` for examples.