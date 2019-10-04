"""  

**Description**: to perform Activities relating to AWS S3 

**Author**: Ahmad Afraz Khan

**********************************************************
Modification Log:  
**********************************************************
Date             |           Author                    |                  Description
**********************************************************  
27/09/2019       |           Ahmad Afraz Khan, Danial Ahmed       |     Final draft.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--------------------------------------------------------------------------
"""  
  
import boto3  
from botocore.exceptions import ClientError,UnknownServiceError  
from logging import *  
import os  
import time
from datetime import datetime  
from operator import itemgetter  
  
class s3Helper:
    """ This class performes all operations related to AWS s3. 
    """

    
    def __init__(self):  
        """
        This method initiates a resource as well as a client for s3."""  
          
        try:  
            session = boto3.Session()  
            self.s3_client = session.client('s3')  
            self.s3_resource = session.resource('s3')
  
  
        except ClientError as e:  
            raise ValueError("s3 helper not started" + e)
        except Exception as e:
            raise ValueError(e)

    def generate_object_name_local(self, target_key, entitypath):
        """
        makes a bucket key of a local file for uploading it as an object to s3

        :param entitypath: it contains local file path
        :type entitypath: str
        :param target_key: it contains target bucket key, where object will be uploaded
        :type target_key: str
        :return: returns target s3 key where file will be uploaded.
        :rtype: str
        """

        file_name = entitypath

        if entitypath.find('/') != -1:
            Tokens = entitypath.split('/')
            file_name = Tokens[len(Tokens) - 1]

        if target_key != '':
            target_key = target_key.strip()
            key_path = target_key + "/" + file_name
        else:
            key_path = file_name

        return key_path

    def generate_object_name_s3(self, target_key, entitypath):
        """
        makes a bucket key for uploading an object to s3 from source bucket

        :param entitypath: it containes s3 path of source file on s3
        :type entitypath: str
        :param target_key: it contains target bucket key, where object will be uploaded
        :type target_key: str
        :return: returns a tuple, which containes source file s3 path ``dict {'Bucket':str,'Key':str}`` along with target bucket key
        :rtype: tuple
        """

        entity_config_s3_tokens = entitypath.split('/')
        entity_config_bucket_name = entity_config_s3_tokens[2]
        entity_config_prefix = ""

        for str in range(3, len(entity_config_s3_tokens) - 1):
            entity_config_prefix += entity_config_s3_tokens[str] + "/"

        entity_config_filename = entity_config_s3_tokens[len(entity_config_s3_tokens) - 1]
        entity_config_prefix += entity_config_filename

        copy_source = {
            'Bucket': entity_config_bucket_name,
            'Key': entity_config_prefix
        }

        if target_key == '':
            target_key = entity_config_filename
        else:
            target_key += '/' + entity_config_filename

        return copy_source, target_key

    def generate_folder_prefix(self, s3path):
        """
        this function generates s3 prefix without target object.

        :param s3path: s3 path 
        :type s3path: str
        :return: returns a tuple containing s3 prefix with no final object & bucket name
        :rtype: tuple
        """
        tokens = s3path.split('/')
        key = ""
        if len(tokens) > 3:

            for se in range(3, len(tokens)):
                if se == 3:
                    key += tokens[se]
                else:
                    key += "/" + tokens[se]
        return key, tokens[2]

    def upload_object(self, IngestionS3Config, entitypath):
        # modifying target bucket prefix 

        target_key, target_bucket_name = self.generate_folder_prefix(IngestionS3Config)
        key_path = self.generate_object_name_local(target_key, entitypath)

        try:
            # uploading entity from local path  
            with open(entitypath, "rb") as f:
                response = self.s3_client.upload_fileobj(f, target_bucket_name, key_path)
        except ClientError as e:
            raise (e)
        except IOError as e:
            raise ValueError(e)
        except Exception as e:
            raise ValueError(e)

    def s3_object_copy(self, IngestionS3Config, entitypath):
        """  
        this function moves s3 object from one bucket to other bucket  

        :param IngestionS3Config: s3 path for source obj 
        :type IngestionS3Config: str
        :param entitypath: s3 path for target object, which would be uploaded
        :type entitypath: str
        """
        target_key, target_bucket_name = self.generate_folder_prefix(IngestionS3Config)
        copy_source, target_key = self.generate_object_name_s3(target_key, entitypath)

        try:
            bucket = self.s3_resource.Bucket(target_bucket_name)
            response = bucket.copy(copy_source, target_key)

        except ClientError as e:
            raise (e)
        except IOError as e:
            raise ValueError(e)
        except Exception as e:
            raise ValueError(e)
   
    def download_athena_output(self, s3_output_athena, QueryExecutionId, file_name):  
        """  
        This method is used to download the output of an ETL job for comparison with expected output.  
  
        :param s3_output_athena: it is a s3 path to download output file of an ETL job.  
        :type s3_output_athena: str
        :param QueryExecutionId: ID of query bieng executed on Ahena.
        :type QueryExecutionId: int
        :param file_name: path to a local file.
        :type file_name: str
        :retun: a local file path, in which athena's results exist
        :rtype: str

        """  
  
        bucket_name = s3_output_athena.split('/')[2]  
        print(file_name)  
        object_path = QueryExecutionId + '.csv'  
  
        try:  
  
            with open(file_name, 'wb') as f:  
                response = self.s3_client.download_fileobj(bucket_name, object_path, f)  
  
            f.close()  
            if file_name.find('/') == -1:  
                path = os.path.dirname(file_name)  
                path += file_name  
            else:  
                path = file_name  
  
            return path  
  
        except ClientError as e:  
            raise ValueError(e)  
  
        except FileNotFoundError as e:  
            raise ValueError(e)  
        except Exception as e:  
            raise ValueError(e)  
  
    def download_object(self, s3path):  
        """  
        This method is used to download an object from s3 bucket.  
  
        :param s3path: s3 path where object is located
        :type s3path: str
        """  
  
        s3_tokens = s3path.split('/')  
        bucket_name = s3_tokens[2]  
        object_path = ""
        filename = s3_tokens[len(s3_tokens)-1]  
  
        if len(s3_tokens) > 4:  
            for str in range(3,len(s3_tokens)-1):  
                object_path+=s3_tokens[str]+"/"
            object_path+=filename
        else:
            object_path+=filename

        try:  
            with open(filename, 'wb') as f:  
                response = self.s3_client.download_fileobj(bucket_name, object_path , f)  
                f.close()  
  
            return filename  
  
        except ClientError as e:  
            raise ValueError(e)  
  
        except IOError as e:  
            raise ValueError(e)
        except Exception as e:  
            raise ValueError(e)

    def upload_results(self, s3path, testsuite_name, files):
        """
        uploads Test Suite execution results to specified bucket along with Robot code generated

        :param testsuite_name: Name of test suite containing test cases
        :type testsuite_name: str
        :param s3path: s3 path where files will be uploaded
        :type s3path: str
        :param files: a dictionary having paths of required files to be uploaded ``dict {'Robot':'','Log':'','Xml':'','Report':''}``
        :type files: dict
        """

        robot_path = os.path.basename(files['Robot'])
        log_path = os.path.basename(files['Log'])
        report_path = os.path.basename(files['Report'])
        xml_path = os.path.basename(files['Xml'])

        timestamp = log_path.split('-')[1] + '-' + log_path.split('-')[2].split('.')[0]

        folder_name = testsuite_name + "_" + timestamp
        prefix, bucket_name = self.generate_folder_prefix(s3path)

        code_prefix = prefix+testsuite_name+"_"+timestamp + '/Code/'
        results_prefix = prefix+testsuite_name+"_"+timestamp + '/Results/'
        try:
            with open(files['Robot'], "rb") as f:
                robot_prefix = code_prefix + robot_path
                response = self.s3_client.upload_fileobj(f, bucket_name, robot_prefix)

            with open(files['Log'], "rb") as f:
                log_prefix = results_prefix + log_path
                response = self.s3_client.upload_fileobj(f, bucket_name, log_prefix)

            with open(files['Report'], "rb") as f:
                report_prefix = results_prefix + report_path
                response = self.s3_client.upload_fileobj(f, bucket_name, report_prefix)

            with open(files['Xml'], "rb") as f:
                output_prefix = results_prefix + xml_path
                response = self.s3_client.upload_fileobj(f, bucket_name, output_prefix)

        except ClientError as e:
            raise (e)
        except FileNotFoundError as e:
            raise (e)
        except Exception as e:
            raise ValueError(e)