#!/bin/bash
cd bliss && python data_normalization_step1.py && python data_normalization_step2.py && cd .. && cd loewe && python data_normalization_step1.py && python data_normalization_step2.py && cd .. && cd hsa && python data_normalization_step1.py && python data_normalization_step2.py && cd ..

