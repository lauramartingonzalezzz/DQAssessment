## Data Quality Assessment 
Data Quality Assessment is a repository that contains the source code developed in the article [1], as well as the dataset used.

This repository comprises 9 files and 3 folders:
- *AI-enabled_data_quality_improvement_techniques.ipynb* is a Jupyter notebook presenting the improvement workflow of a raw dataset using domain knowledge and AI techniques.
- *DQ_dimensions_performance.py* is a Python script in charge of launching Monte Carlo simulations to obtain runtime performance when assessing the chosen quality dimensions.
- *main.m* is the Matlab script that is responsible for obtaining the performance metrics of the output results of the previous file.
- *DQ_dimensions_performance.ipynb* is a Jupyter notebook that depicts the performance of each quality dimension in terms of delay.
- *configuration_variables.py* is a Python script used as a configuration file.
- *basic_operations.py* is a Python script that comprises different base functions.
- *context_broker_api.py* is a Python script that defines the API requests needed to interact with the Context Broker.
- *requirements.txt* is the standard file listing the PyPI packages to be installed.
- *README.md* is this documentation.
- */raw_data* contains the dataset used prior to its assessment. (data can be downloaded [here](https://unican-my.sharepoint.com/:u:/g/personal/martingonl_unican_es/EeZ8K_njdbhOhpQz-sxQTLkBArLUzHXA1qjjAZBcwuzHIA?e=lZ5jFP))
- */data* is an empty folder tree which will be filled in as the *AI-enabled_data_quality_improvement_techniques.ipynb* script is run.
- */simulations* is an empty folder tree which will contain a subfolder for each of the Monte Carlo simulations obtaining the delay in the quality dimensions processes (*DQ_dimensions_performance.py*). It also includes an empty subfolder named */median_values*, where some of the results of the Matlab script (*main.m*) will be stored for later use in the Jupyter notebook *DQ_dimensions_performance.ipynb*.

[1] L. Martín, L. Sánchez, J. Lanza, and P. Sotres, “Development and evaluation of Artificial Intelligence techniques for IoT data quality assessment and curation,” Internet of Things, vol. 22, p. 100779, Jul. 2023, doi: 10.1016/J.IOT.2023.100779.]

## Acknowledgements

This work was supported by the European Commission CEF Programme by means of the project SALTED ‘‘Situation-Aware Linked heTerogeneous Enriched Data’’ under the Action Number 2020-EU-IA-0274 and by the Spanish State Research Agency (AEI) by means of the project SITED ‘‘Semantically-enabled Interoperable Trustworthy Enriched Data-spaces’’ under Grant Agreement No. PID2021-125725OB-I00.


## License
This material is licensed under the GNU Lesser General Public License v3.0 whose full text may be found at: [LICENSE](https://github.com/lauramartingonzalezzz/DQAssessment/blob/4869be148134f43e93cc81ab0ef0cd1e9d769a82/LICENSE)
