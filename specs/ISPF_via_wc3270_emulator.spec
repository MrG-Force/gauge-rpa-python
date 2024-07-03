# Perform ISPF operations via wc3270 emulator

Setup:
* Setup environment
* Open wc3270 emulator
* Connect to the host
* Login to IBM Z Xplore learning platform

## Get the ZXP list of datasets
* Go to the Utilities menu
* Go to Data Set List Utility
* Set Dsname Level to "ZXP.*" and press Enter
* Capture the list of datasets
* Dump data sets to "output/data_sets.json"
* The list should contain the following datasets:

   |Dataset Name     |
   |-----------------|
   |ZXP.SQL          |
   |ZXP.PUBLIC.CLIST |
   |ZXP.PUBLIC.README|
   |ZXP.PUBLIC.SOURCE|
   |ZXP.UTILITY      |


## Get data from a public dataset
* Go to the Utilities menu
* Go to Data Set List Utility
* Set Dsname Level to "ZXP.PUBLIC" and press Enter
* View "ZXP.PUBLIC.JCL" dataset
* Find and open the record named "JCLSETUP"
* Capture the text from the record
* The text should start with "//JCLSETUP JOB"
* Dump record content to "output/jcl_setup.txt"

_____________________________
Teardown:

* Log off from the mainframe
