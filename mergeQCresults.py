# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 23:52:48 2021

@author: KMacDo
"""
#import packages I need
import os
import fnmatch
import pandas as pd
#If you need to change a directory, you can do it this way (but you don't here):
#os.chdir('C:/Users/KMacDo/Desktop/PythonTest')

#save the current working directory (cwd) to a variable to use in everything below. 
#For us, this would be the MiSeqRunID directory for each run - it changes each time we analyze a run, 
#so i want to pull this from where ever I am, 
#so I don't have to enter it each time:
cwdPath = os.getcwd()

#Define Paths for each file to combine:
file1Path = os.path.dirname('ncov2019-artic-nf-v1.1-output/ncov-tools-v1.4-output/qc_reports/')
#print(file1Path)  #you can use this to test that each step is working. I had to do this for every line.
file2Path = os.path.dirname('ncov2019-artic-nf-v1.1-output/ncov-tools-v1.4-output/qc_reports/')
file3Path = os.path.dirname('ncov2019-artic-nf-v1.1-output/ncov-tools-v1.4-output/lineages/')
file4Path = os.path.dirname('ncov2019-artic-nf-v1.1-output/')



#NCOV-TOOLS QC FILE: (store the file contents as dataframe (df)):
for dir_path, dir_names, file_names in os.walk(cwdPath):
    for f in file_names:
        if fnmatch.fnmatch(f, '*_summary_qc.tsv'):
            #print(f)  # worked
            file1 = os.path.join(cwdPath, file1Path, f)
            df_ncovtools = pd.read_table(file1)
            #print(df_ncovtools) #worked
    
    

#VARIANT SUMMARY FILE: (want only ObsMutation, TotalMutations, ProportionMutations from this)
#use more specific file path b/c are similarly named files in the ncov_watch subdirectory as well, which will be detected 1st and cause an error that the file isn't found. 
#sort first to match highest number first for each sample
#remove duplicate lines (keep the first occurrence b/c it has the highest mutations)

for dir_path, dir_names, file_names in os.walk(os.path.join(cwdPath, file2Path)):
    for f in file_names:
        if fnmatch.fnmatch(f, '*_ncov_watch_summary.tsv'):
            #print(f)  # worked 
            file2 = os.path.join(cwdPath, file2Path, f)
            df_variantsum = pd.read_table(file2)
            df_variantsum2 = df_variantsum.sort_values('proportion_watchlist_mutations_observed', ascending=False)
            df_variantsum3 = df_variantsum2.drop_duplicates(subset=['sample_id'], keep='first')
            #print(df_variantsum3) #worked 

#MERGE NCOV-TOOLS/LINEAGEmerge WITH VARIANT df: (store merged tables as new dataframe)
df_ncov_variant_merge = pd.merge(df_ncovtools, df_variantsum3, how='left', left_on='sample', right_on='sample_id')
#print(df_ncov_variant_merge) #works


#LINEAGE FILE
for dir_path, dir_names, file_names in os.walk(cwdPath):
    for f in file_names:
        if fnmatch.fnmatch(f, '*_lineage_report.csv'):
            #print(f)  # worked  
            file3 = os.path.join(cwdPath, file3Path, f)
            df_lineage = pd.read_csv(file3) #, names = ['taxon', 'lineage', 'probability', 'pangoLEARN_version', 'status', 'note'])
            pd.set_option('display.max_columns', None)
            #print(df_lineage)
            #df_lineage_split = pd.DataFrame(df_lineage.str.split('_').tolist(), columns = ['text', 'taxon']) #nope
            df_lineage_split = df_lineage['taxon'].str.replace('Consensus_', '')
            #print(df_lineage_split)
            df_lineage_combo1 =  [df_lineage_split, df_lineage.iloc[:, 1:6]]
            df_lineage_combo2 = pd.concat(df_lineage_combo1, axis=1)
            #axis=1 is to join/concat by putting columns next to each other
            #axis=0 is to concat by putting rows of diff sources on top of each other
            #print(df_lineage_combo2)  #works


#MERGE NCOVTOOLS/VARIANTmerge AND LINEAGE df:
df_ncov_variant_lineage_merge = pd.merge(df_ncov_variant_merge, df_lineage_combo2, how='left', left_on='sample', right_on='taxon')
#print(df_ncov_variant_lineage_merge) #works  


#ARTIC QC FILE:
for dir_path, dir_names, file_names in os.walk(cwdPath):
    for f in file_names:
        if fnmatch.fnmatch(f, '*.qc.csv'):
            #print(f)  # worked 
            file4 = os.path.join(cwdPath, file4Path, f)
            df_artic1 = pd.read_csv(file4)
            df_artic2 = df_artic1.iloc[:, 0:5]
            df_artic3 = df_artic1.iloc[:, 7:8]
            df_artic4 = [df_artic2, df_artic3]
            df_artic = pd.concat(df_artic4, axis=1)
            #print(df_artic) #works


#MERGE NCOV-TOOLS/VARIANT/LINEAGEmerge WITH ARTIC df:
df_ncov_variant_lineage_artic_merge = pd.merge(df_ncov_variant_lineage_merge, df_artic, how='left', left_on='sample', right_on='sample_name')
#print(df_ncov_variant_lineage_artic_merge) #works


#CREATE NEW COLUMN FOR TOTAL MUTATIONS:
df_ncov_variant_lineage_artic_merge["TotalMutations"] = df_ncov_variant_lineage_artic_merge.num_observed_mutations.astype(str).str.cat(df_ncov_variant_lineage_artic_merge.num_mutations_in_watchlist.astype(str), sep="/")
#print(df_ncov_variant_lineage_artic_merge)  #works

#Define variable using last part of directory/path
#This will be used to name your files uniquely:
MiSeqRunID = os.path.basename(os.path.normpath(cwdPath))
#print(MiSeqRunID)  #works
    
#save final1 file as csv (easier to open in Excel than tsv) 
#(this has ALL columns of ALL files, used for testing mostly - not needed):
#df_ncov_variant_lineage_artic_merge.to_csv(MiSeqRunID + '_' + 'ncov_variantsum_lineage_artic_merge_leftJoin.csv')


#BREAK APART MERGED FILE TO JUST KEEP COLUMNS I WANT:
#probably a more efficient way to do this, but I'm a beginner and this works. 
df_ncov1 = df_ncov_variant_lineage_artic_merge.iloc[:, 0:18]
#print(df_ncov1)
df_variant1 = df_ncov_variant_lineage_artic_merge.iloc[:, 19:23]
#print(df_variant1)   
df_variant2 = df_ncov_variant_lineage_artic_merge.iloc[:, 35:36]
#print(df_variant2)
df_lineage1 = df_ncov_variant_lineage_artic_merge.iloc[:, 28:29]
df_lineage2 = df_ncov_variant_lineage_artic_merge.iloc[:, 26:27]
#print(df_lineage1)
#print(df_lineage2)
df_artic5 = df_ncov_variant_lineage_artic_merge.iloc[:, 30:35]
df_artic6 = df_ncov_variant_lineage_artic_merge.iloc[:, 29:30]
#print(df_artic5)
#print(df_artic6)


#CONCATENATE above dfs IN DESIRED ORDER:
#df_ncov_variant_lineage_artic_merge2 = [df_ncov1, df_variant1, df_variant2.TotalMutations.astype(str), df_lineage1, df_lineage2, df_artic5, df_artic6]
#TotalMutations column (e.g. 16/17) opens in excel as date for some, so remove this column (no way to fix here), and just make the column in dashboard instead. 
df_ncov_variant_lineage_artic_merge2 = [df_ncov1, df_variant1, df_lineage1, df_lineage2, df_artic5, df_artic6]
df_ncov_variant_lineage_artic_merge3 = pd.concat(df_ncov_variant_lineage_artic_merge2, axis=1)
#print(df_ncov_variant_lineage_artic_merge3)

#save final2 file as csv (easier to open in Excel than tsv):
#(this has only the columns I want to link my dashboard to, for various people's purposes)
df_ncov_variant_lineage_artic_merge3.to_csv(MiSeqRunID + '_' + 'QC_lineage_VoC_OrderedFinal.csv')



                    
