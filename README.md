# merge_ncov_qc_results
Merges (left Join) the result fields from artic &amp; ncov-tools qc summaries, pangolin, and ncov-watch into 1 csv file. 

   *_summary_qc.tsv (ncov-tools qc summary)

   *_ncov_watch_summary.tsv (VoC mutations summary) (in qc_reports directory, not the ncov_watch directory)

   *_lineage_report.csv (pangolin lineage report)

   *.qc.csv (artic qc summary)


<b>To run:</b>

1st set up environment with pandas (done on sabin already)

cd to directory with result files 

      (for BC: cd path/to/AnalysisDirectory/[MiSeqRunID] )

      conda activate pandas

      python3 path/to/script/mergeQCresults.py
      
      conda deactivate


<b>To run/loop through all MiSeqRunID directories:</b>

    conda activate pandas

    (For BC:) cd path/to/AnalysisDirectory/

    for dir in /path/to/AnalysisDirectory/*/; do cd $dir; python3 /path/to/script/mergeQCresults.py; cd ..; done
    
    conda deactivate


<b>Assumed Directory Structure:</b>

![Github_AssumedDirectoryStructure_paint2](https://user-images.githubusercontent.com/72042148/109408269-a1886000-793c-11eb-9f22-b481ceb6dea6.png)



