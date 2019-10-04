"""  
-------------------------------------------------------------------------------------------------  
Description: to upload configuration of an entity for its creation.
Author: Ahmad Afraz Khan  
  
Modification Log:  
---------------------------------------------------------------------------------------------------  
Date                        Author                  Description  
---------------------------------------------------------------------------------------------------  
27/09/2019                  Ahmad Afraz Khan            initial draft.  
---------------------------------------------------------------------------------------------------\  
"""  

from qa_automation.aws import s3Helper

class entity:

    def __init__(self):
        self.s3_helper = s3Helper.s3Helper()
    
    def upload_entity(self, IngestionS3Config,entitypath):  
        """  
        This method will be used to create an entity on s3 for Ingestion in   
        DataLake  
  
        @IngestionS3Config: it is a dictionary containing s3 path info for uploading entity  
        @entityPath: it is path to local entity to be uploaded.  
        """
        if entitypath.find('s3://') == -1:
            self.s3_helper.upload_object(IngestionS3Config, entitypath)
        else:
            self.s3_helper.s3_object_copy(IngestionS3Config, entitypath)
  