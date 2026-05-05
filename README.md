# MEIEP Signal Extraction Framework

**Author:** Riam Daou  
**Status:** Open Source Release  

## Overview
This repository contains the computational framework designed to extract **non-thermal mechanical transients** resulting from macroscopic decoherence. It is built to support the Mass-Energy-Information Equivalence Principle (MEIEP).

While standard quantum biological or optomechanical research models decoherence as a thermodynamic entropy increase, this framework utilizes **Matched Filtering** and **RANSAC-based robust outlier rejection** to computationally isolate the precise temporal phase-shift indicating physical mass release upon quantum collapse.

## Features
* **Synthetic Injection Recovery:** Generates thermal Brownian noise models with injected MEIEP transient signatures.
* **Matched Filter Pipeline:** Cross-correlates raw sensor streams against theoretical high-mass information release templates.
* **RANSAC Isolation:** Mathematically uncouples standard thermal variance from sudden non-thermal phase-shifts, bypassing the limitations of traditional thermal averaging.

## Quick Start
Ensure you have `numpy`, `scipy`, `scikit-learn`, and `matplotlib` installed.
```bash
pip install numpy scipy scikit-learn matplotlib
python meiep_signal_extraction.py
