"""
-------------------------------------------------------------------------------------------------
Description: These are methods that assist in creation of the Test Case section in the robot suite
             related to the JobDefinitions

Author: Taha Bilal Gillani

Modification Log:
---------------------------------------------------------------------------------------------------
Date						Author					                                    Description
---------------------------------------------------------------------------------------------------
24/09/2019					Taha Bilal Gillani	    	Final draft.
---------------------------------------------------------------------------------------------------\
"""
TAB_SEPERATOR = '    '
END_OF_LINE = '\n'

import json

'''
Helper Functions for Testcase Generation
used by testCaseGenerator.py

+--- Ingestion Portion             --> ingestion 
+--- ETL Wait Portion              --> etl_wait (to be coded)
+--- Job Metadata Portion          --> job_metadata
+--- Entity Configguration Portion --> entity_config 
+--- String Conversion             --> stringify
+--- Positional Printer            --> positional_printer

 '''


class jobCreationHelper:

    def __init__(self):
        pass

    def stringify(self, input_string):
        '''
        Classmethod inputs a string which is to be check if it's a reference to a varible string
        in "$value" format or "value" format, if it's in the later format, the value will be hardcoded
        in the test suite.

        :param input_string: string to be checked for the format
        :type  input_string: str
        :return: determined string if it's to be hardcoded or to be made a variable reference
        :rtype: str

        '''
        if input_string[0] == '$':
            input_string = '${' + input_string[1:] + '}'
            return input_string
        else:
            return input_string

    def positional_printer(self, job_name, section_name, key_name, data_json):
        '''
        This function takes the job name, section name, key name and data to be printer, it checks
        if the provided input is a list or a dict, if no, it wil have a name implementation in the variable
        section and it can be reference here with ${variable} structure, if yes, this value will be passed
        to stringify function which performs it's implementation.

        :param job_name: The name of the test case
        :type  job_name: str
        :param section_name: The section of the test case
        :type  section_name: str
        :param key_name: The key passed, will be different and totally on choice
        :type  key_name: str
        :param data_json: the test case data in form of dictionary which determins type of data
        :type  data_json: object
        :return: variable definition in robot code for a keyword
        :rtype: str
        '''

        if type(data_json) == dict:
            return ('$' + '{' + job_name.replace(' ', '_') + '_' + section_name + '_' + key_name + '}')

        elif type(data_json) == list:
            return ('$' + '{' + job_name.replace(' ', '_') + '_' + section_name + '_' + key_name + '}')

        elif type(data_json) == str:
            return self.stringify(data_json)
        else:
            raise ValueError(
                "Is the Value entered in JobName {} , Section : {} , Key : {}".format(job_name, section_name, key_name)
                + " Correct? \n It seems like an invalide or unsupported option. ")


    def job_metadata(self, job_name, metadata_json):
        '''
        It requires job name and the metadata json as input, metadata_json comes from
        the configuraiton file, the metadata includes the Documentation of the test case and the tags that are
        passed to the test case in configuration file. This function prints the [Documentation] and [Tags] tags in
        the robot code file against a test case.

        :param job_name: the name of the job which metadata belongs to
        :type job_name: str
        :param metadata_json: consists all the data required for production of the [Documentation] and [Tags]
        :type metadata_json: str
        :return: a string in robot code format having the needful
        :rtype: str
        '''

        if "Documentation" in metadata_json.keys():

            if "Tags" in metadata_json.keys():

                tags_string = ''
                for tags in metadata_json["Tags"]:
                    tags_string += TAB_SEPERATOR + str(tags)

                return (
                        TAB_SEPERATOR + "[Documentation]" + TAB_SEPERATOR +
                        metadata_json["Documentation"] + END_OF_LINE +
                        TAB_SEPERATOR + "[Tags]" + tags_string + END_OF_LINE
                )

            else:
                raise KeyError(
                    "Tags are missing or incorrect from JobMetadata in JobDefinitions : " + job_name + ".\n" +
                    "Please add tag \"no_tag\" if no tag is to be assigned.")
        else:
            raise KeyError(
                "Descriptions is missing from TestMetadata in Testcase : " + job_name + ".\n")

    def entity_config(self, job_name, section_name, entity_config_json):
        '''
        This function takes the name and data json of the section as input and outputs the entity configuration
        portion in robotcode file against a testcase. the implementation of this function has decision statements that are taken on
        basis of the configurations provided in the JSON portion. At end it prints the test cases against the
        given configuration in the robot code file.

        :param job_name: name of the job for which entity configuration belongs to
        :type job_name: str
        :param section_name: name of the section which is EntityConfigs
        :type section_name: str
        :param entity_config_json: consists all the data related to entity configurations for the specific job
        :type entity_config_json: dict
        :return: returns the entity upload keyword with required fields in robot code fashion
        :rtype: str
        '''

        if entity_config_json["Type"] == "S3Upload":

            if "S3Path" in entity_config_json.keys():

                if "S3BucketConfig" in entity_config_json.keys():
                    return (TAB_SEPERATOR +
                            'upload entity' +
                            TAB_SEPERATOR +
                            self.positional_printer(job_name, section_name, 'S3BucketConfig',
                                                    entity_config_json["S3BucketConfig"]) +
                            TAB_SEPERATOR +
                            self.positional_printer(job_name, section_name, 'S3Path', entity_config_json["S3Path"]) +
                            END_OF_LINE
                            )
            else:
                raise ValueError("In jobdefinition : {} , In EntityConfig ".format(job_name) +
                                 "S3Path is either incorrect, or unavailible. ")


        elif entity_config_json["Type"] == "Local":
            pass

            if entity_config_json["LocalPath"]:
                pass


        else:
            raise KeyError("In jobdefinition : {} , In EntityConfig ".format(job_name) +
                           "Type is either incorrect, or unavailible. ")

    def ingestion(self, job_name, section_name, ingestion_json):
        '''
        It requires job name and the ingestion json as input, ingestion_json comes from
        the configuraiton file, the implementation of this function has decision statements that are taken on
        basis of the configurations provided in the JSON portion. At end it prints the test cases against the
        given configuration in the robot code file.

        :param job_name: the name of the job for which ingestion is to be executed
        :type job_name: str
        :param section_name: the name of the section which is Ingestion
        :type section_name: str
        :param ingestion_json: the data required for the ingestion
        :type ingestion_json: dict
        :return: the ingestion robot code for the particular job
        :rtype: object
        '''

        if "IngestionName" in ingestion_json.keys():

            ingestion_name = ingestion_json["IngestionName"]

            if "Steps" in ingestion_json.keys():

                if type(ingestion_json["Steps"]) == list:

                    return (TAB_SEPERATOR +
                            'ingestion' +
                            TAB_SEPERATOR +
                            self.positional_printer(job_name, section_name, ingestion_name + "_Steps",
                                                    ingestion_json["Steps"]) +
                            END_OF_LINE
                            )

                else:
                    raise ValueError("In JobName {} and Section Ingestion ".format(job_name) +
                                     "Steps should be a list with dictionaries. ")

            else:
                raise KeyError("In JobName {} and Section Ingestion ".format(job_name) +
                               "Steps keyword does not exisit. ")
        else:
            raise KeyError("Name is incorrect in Ingestion for " +
                           "JobName {} ".format(job_name))

    def etl_wait(self, job_name, etl_json):

        section_name = "ETLWait"

        if "GetDependencyConfig" and "ETLWaitConfig" in etl_json.keys():

            if etl_json["ETLWaitConfig"]["Type"] == "DatabaseTable":

                if etl_json["GetDependencyConfig"]["Type"] == "SQL":

                    return (
                            TAB_SEPERATOR +
                            'etlwait' +
                            TAB_SEPERATOR +
                            self.positional_printer(job_name, section_name, "GetDependencyConfig",
                                                    etl_json["GetDependencyConfig"]["Details"]) +
                            TAB_SEPERATOR +
                            self.positional_printer(job_name, section_name, "ETLWaitConfig",
                                                    etl_json["ETLWaitConfig"]["Details"]) +
                            END_OF_LINE
                    )
                else:
                    raise Exception("In JobName : {} , in GetDependencyConfig, in Types ".format(job_name) +
                                    "Type is either incorrect or unavailible. ")
            else:
                raise Exception("In JobName : {} , in ETLWaitConfig, ".format(job_name) +
                                "Type is either incorrect or unavailible. ")

        else:
            raise KeyError("In JobDefinition {} , either the ".format(job_name) +
                           "GetDependancyConfig or ETLWaitConfig are empty or missing. ")
