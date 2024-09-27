#De-identification of EMR Data to a Limited Dataset

Current location of Data:  /labs/collab/K-lab-MODS/MODS-PHI/<Emory/Grady>_Data/

New Location of Deidentified data: 
EMORY: /labs/collab/K-lab-MODS/deid_Emory
GRADY: /labs/collab/K-lab-MODS/deid_grady

## De-identification Steps:

  1. All patient identifiers (csn, patient_id, mrn) will be hashed. It will be ensured that the mapping remains the same for the same encounter/patient across the dataset. 
     A list to map back to original identifiers will be retained and located at: 
     /labs/collab/K-lab-MODS/MODS-PHI/Emory_Data/<year>/matching_list_csn/patid.csv
     /labs/collab/K-lab-MODS/MODS-PHI/Grady_Data/1. Administrative Attributes/matching_list_cs/patid_<year>.csv
  2. Demographics data file: The following columns will be dropped from the dsv file
      * Last 4 digits of SSN
      * First Name 
      * Last Name
      * Mi (middle name)
     
