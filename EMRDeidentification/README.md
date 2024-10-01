# De-identification of EMR Data to a Limited Dataset

Current location of Data:  /labs/collab/K-lab-MODS/MODS-PHI/<Emory/Grady>_Data/

New Location of Deidentified data: 

EMORY: */labs/collab/K-lab-MODS/deid_Emory*

GRADY: */labs/collab/K-lab-MODS/deid_grady*

## De-identification Steps:

  1. All patient identifiers (csn, patient_id, mrn) will be hashed. It will be ensured that the mapping remains the same for the same encounter/patient across the dataset. 
     A list to map back to original identifiers will be retained and located at: 
     * /labs/collab/K-lab-MODS/MODS-PHI/Emory_Data/<year>/matching_list_csn/patid.csv
     * /labs/collab/K-lab-MODS/MODS-PHI/Grady_Data/1. Administrative Attributes/matching_list_cs/patid_<year>.csv
  2. Demographics data file: The following columns will be dropped from the dsv file
      * Last 4 digits of SSN
      * First Name 
      * Last Name
      * Mi (middle name)
      * Ethnicity (Ethnicity code is retained as a categorical variable)
      * Race (Race code is retained as a categorical variable)
   3. Encounters data file:
      * zip_code is dropped
      * csn, patient_id are hashed
      * facility_nm is converted to a categorical variable
   4. All dates and times were deidentified using the following scheme:
      1. Times are converted to UTC.
      2. The _datetime_ object is converted to unix timestamp. 
      3. The first digit is replaced with a 0
      4. The resulting timestamp is converted back to datetime.     
   5. The following columns are dropped from the files, wherever they occur:
      * Performing physician name
      * flow_row_id (GCS)
