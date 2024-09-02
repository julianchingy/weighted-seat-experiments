# Code for thesis chapter titled "Apportionment with Weighted Seats"

This is the code used to run the experiments for both the synthetic data analysis and the Bundestag Case Study section in the
chapter titled "Apportionment with Weighted Seats".

## Folder structure.

Here are some details on the contents of this folder.

`main.py` - This is the script to run the experiments.

`rules.py` - This contains the implementation of the WSAMs.

`experiment.py` - This contains methods related to the experiments such as checking the satisfaction of proportionality properties, parsing Bundestag committee election data from the `bundestag_committees' folder, generating synthetic election instances, etc.

`election.py` - This contains the methods to calculate the various quota values for parties.

`experiment_results` - This is a folder that contains the text files that contains the summarised results of the experiments.

`bundestag_committees` - This is a folder that contains the Bundestag committee election data that was used in the Bundestag case study experiments.

`README.md` - This is the README file.

## How to run the experiments

Run the main script and perform the Bundestag case study experiments by using the following command and argument (experiments coded using Python3):

	python3 main.py 0

The Bundestag experiment results can then be read in the `bundestag_results.txt` file which can be found in the `experiment_results` folder.

Run the main script and perform the synthetic data experimentsby using the following command and argument (experiments coded using Python3):

	python3 main.py 1

The synthetic experiment results can then be read in the `results_synth.txt`, `results_synth_2.txt` and `results_synth_3.txt` files which can be found in the `experiment_results` folder. Note that due to randomly generated data, results may vary after each run of the synthetic experiments.

If no argument is specified or a non-integer argument is used when running the script then an error message will be printed.

Also note that the following must be installed to run the experiments:

- The `mip' package (https://pypi.org/project/mip/).
- The `numpy' package (https://pypi.org/project/numpy/).