# merge_ncov_qc_results
Merges the result fields from artic &amp; ncov-tools qc summaries, pangolin, and ncov-watch into 1 csv file. 


<b>To run:</b>
1st set up environment with pandas (done on sabin already)

cd to directory with result files 
(for BCCDC: cd projects/covid-19_production/analysis_by_run/<MiSeqRunID>)

conda activate pandas
python3 path/to/script/mergeQCresults.py
