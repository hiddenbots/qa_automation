"""  
-------------------------------------------------------------------------------------------------  
Description: to upload data for ingestion in EDL.
Author: Ahmad Afraz Khan  
  
Modification Log:  
---------------------------------------------------------------------------------------------------  
Date                        Author                  Description  
---------------------------------------------------------------------------------------------------  
27/09/2019                  Ahmad Afraz Khan            Final draft.  
---------------------------------------------------------------------------------------------------\  
"""  

from qa_automation.aws import s3Helper
from qa_automation.aws import dbHelper
from operator import itemgetter

class ingestion:

    def __init__(self):
        self.s3_helper = s3Helper.s3Helper()
        self.db_helper = dbHelper.dbHelper()

    def ingestion(self, ingestion_steps):
        """
        uploads data to s3 for ingestion purpose

        @ingestion_steps: a dictionary containing steps to be performed for complete Ingestion
        """
        ordered_steps = sorted(ingestion_steps['Steps'], key=itemgetter('Order'))  
        for step in ordered_steps:
            
            if step['Type'] == 'S3Upload':
                self.s3_helper.s3_object_copy(step['S3BucketConfig'],step['S3Path'])  
                print('entity uploaded')
            elif step['Type'] == 'InsertRecord':
                self.db_helper.insert_record(step)  
                print('entity inserted in DB.')