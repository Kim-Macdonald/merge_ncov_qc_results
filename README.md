# merge_ncov_qc_results
Merges (left Join) the result fields from artic &amp; ncov-tools qc summaries, pangolin, and ncov-watch into 1 csv file. 

    *_summary_qc.tsv (ncov-tools qc summary)

    *_ncov_watch_summary.tsv (VoC mutations summary) (in qc_reports directory, not the ncov_watch directory)

    *_lineage_report.csv (pangolin lineage report)

    *.qc.csv (artic qc summary)


<b>To run:</b>

1st set up environment with pandas (done on sabin already)

cd to directory with result files 

(for BCCDC: cd projects/covid-19_production/analysis_by_run/[MiSeqRunID] )

conda activate pandas

python3 path/to/script/mergeQCresults.py
