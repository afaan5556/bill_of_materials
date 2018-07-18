# bill_of_materials

### Overview

This script reads a standard Arena BoM export as a pandas dataframe and then performs the operations necessary to:

* Establish parent/child relationships
* Restructure the BoM from an Engineering (eBom) to a Construction (cBoM)
* Nest items as needed

### Files Needed
* A csv file of the Arena BoM export. In this example it is titled `BOM_Array_v3.3.csv` and is placed 1 folder up from where the script is saved
* A csv file of the Network Mapping. In this example it is titled `network.csv` and is placed 1 folder up from where the script is saved
