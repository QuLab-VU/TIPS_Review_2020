requirements.txt contains the python packages necessary to recreate this code...

First run the calc_synergy.py file to calculate the synergy for the merck dataset "merck_perVia_10-29-2018.csv"
This is run in python2

Next activate the tensorflow gpu virtual enviroment (python3)
conda activate tf_gpu
Requirements for this enviroment are in the requirements.txt
Set up according to: https://towardsdatascience.com/tensorflow-gpu-installation-made-easy-use-conda-instead-of-pip-52e5249374bc
Run on Ubuntu 18.04
Spects according to nvidia-smi:
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 430.40       Driver Version: 430.40       CUDA Version: 10.1     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce RTX 2070    Off  | 00000000:18:00.0  On |                  N/A |
| 29%   33C    P8    13W / 175W |    684MiB /  7979MiB |      2%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               


After tf_gpu enviroment is activated run format_data.py which sets up the folders bliss,loewe,hsa for deep learning
This script copies the appropriate analysis files into each folder.

Next from bash run ./run_norm_files.h  
This runs the normalization step in each folder.
NOTE this is memory intensive (~16GB RAM needed).  Avoid parallel tasks
Next run ./run_model_build.h
This runs the deep learning algorithm according to DeepSynergy K Preuer et al. and saves the resulting models.

Finally run ./run_prediction_files.h which runs the prediction for each metric

Generate the plots using the plot_generation.py

