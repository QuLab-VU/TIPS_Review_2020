#!/bin/bash
cd bliss && python prediction_step1.py && cd .. && cd loewe && python prediction_step1.py && cd .. && cd hsa && python prediction_step1.py && cd ..
