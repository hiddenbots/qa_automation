"""
-------------------------------------------------------------------------------------------------
Description: testCaseGenerator.py is a module which assists the robotCodeGenerator.py module
             and takes responsibility of the *** Test Case *** section 
            
Author: Taha Bilal Gillani

Modification Log:
---------------------------------------------------------------------------------------------------
Date						Author					                                    Description
---------------------------------------------------------------------------------------------------
24/09/2019					Taha Bilal Gillani	    	Final draft.
---------------------------------------------------------------------------------------------------\
"""
from qa_automation.robot_code_generator import cleanupCreationHelper
from qa_automation.robot_code_generator import jobCreationHelper
from qa_automation.robot_code_generator import testcaseCreationHelper
import json

TAB_SEPERATOR = '    '
END_OF_LINE = '\n'


class testCaseGenerator:
    '''
    TestCaseGenerator Class generates the *** TestCases *** portion in the
    robot file. This module uses the testcaseCreationHelper.py, cleanupCreationHelper.py and
    jobCreationHelper.py hand-in-hand as it holds it's positional printing implementation

    The section follows the pattern like

            *** Test Cases ***
        JobDefinitions (it's test cases in robot logic)
        TestCases      (it's test cases in robot logic)
        CleanupSection (it's test cases in robot logic)
    '''

    def __init__(self):
        self.testcase_helper = testcaseCreationHelper.testcaseCreationHelper()
        self.job_helper = jobCreationHelper.jobCreationHelper()
        self.cleanup_helper = cleanupCreationHelper.cleanupCreationHelper()

    def get_jobs_configurations(self, configuration_json):
        '''
        This method takes the configuration file path as an input and extracts
        the "JobDefinitions" portion from the configuration file and returns it as
        a JSON dump.

        :param configuration_json: the JSON dumps of the configuration file
        :type configuration_json: dict
        :return: a dictionary object which includes all the JobsDefinition list of Jobs
        :rtype: dict
        '''
        jobs = configuration_json['JobsDefinitions']
        return jobs

    def get_testcases_configurations(self, configuration_json):
        '''
        This method takes the configuration file path as an input and extracts
        the "TestCases" portion from the configuration file and returns it as
        a JSON dump.

        :param configuration_json: the JSON dumps of the configuration file
        :type configuration_json: dict
        :return: It holds all the TestCases section from the input configuration file
        :rtype: dict
        '''
        testcases = configuration_json['TestCases']
        return testcases

    def get_job(self, job_name, job_json):
        '''
        This classmethod takes input **job_name** and **job_json** and gets the generated
        section of test cases for that particular job which includes the [Documentation], [Tags]
        and keywords.

        :param testcase_name: the specific name of the job
        :type testcase_name: string
        :param testcase_json: the json body of the specific job definition in array of job definitions
        :type testcase_json: dict
        :return: the robot file format for the job configuration
        :rtype: string
        '''

        job_name = job_name.replace(' ', '_')

        metadata = self.job_helper.job_metadata(
            job_name, job_json["JobMetadata"])

        ingests = ''
        counter = 0
        for ingest in job_json["Ingestion"]:
            ingests += self.job_helper.ingestion(job_name, "Ingestion_" + str(counter), ingest)
            counter += 1

        entities = ''
        counter = 0
        for entity in job_json["EntityConfigs"]:
            entities += self.job_helper.entity_config(job_name, "EntityConfigs_" + str(counter), entity)
            counter += 1

        etlwait = self.job_helper.etl_wait(job_name, job_json["ETLWait"])

        job = (job_name + END_OF_LINE + metadata + entities + ingests + etlwait)

        return job

    def get_testcase(self, testcase_name, job_name, testcase_json):
        '''
        This class method takes input testcase_name, job_name and the testcase_json which has
        contents related to that specific test case. It uses a helper function testcase_helper.validations
        to parse the section to refer variables and inputs in robot format.

        :param testcase_name: the specific name of the testcase
        :type testcase_name: str
        :param testcase_json: the json body of the specific testcase in array of testcases
        :type testcase_json: dict
        :return: the robot file format for the testcase configuration
        :rtype: str
        '''

        testcase_name = testcase_name.replace(" ", "_")

        #determination of testcase tpye
        if testcase_json["TestCaseType"] == 'DataValidation':

            metadata = self.testcase_helper.test_metadata(
                testcase_name, testcase_json["TestMetadata"])

            val = ""
            counter = 0
            for validation in testcase_json["Validations"]:
                val += self.testcase_helper.validations(
                    testcase_name, "Validations_" + str(counter), validation)
                counter += 1

            combine_name = (job_name + '_' + testcase_name).replace(' ', '_')

            testcase = (combine_name + END_OF_LINE +
                        metadata +
                        val + END_OF_LINE)

            return testcase

        else:
            raise Exception("In testcase {}, ".format(testcase_name) +
                            "the TestCaseType is not correct, missing or mis-typed," +
                            "please refer to the documentation")

    def perform_cleanup(self, entity_vars):
        '''
        This takes input the entity_vars list which is a list of objects, each object includes
        JobName, JobTag, Entites for that Job, and CleanupSection for specific job. It uses the sections
        to generate a Testcase Teardown against Entities which were created as a trace for testing.

        :param entity_vars: Variable holds all sections mentioned in description
        :type  entity_vars: A complex variable returned by variableGenerator.get_cleanup_configurations
        :return: This consists of cleanup section for all the entities created if they opt for cleanup
        :rtype: str
        '''
        cleanup_section = ''
        cleanup_section += END_OF_LINE

        for each_object in entity_vars:
            each_job_cleanup = ''
            tags_metadata = self.cleanup_helper.cleanup_metadata(each_object["JobTags"])

            for entity in each_object["Entities"]:

                if entity["Cleanup"] in each_object["CleanupSection"].keys():
                    steps_keywords = ''
                    counter = 0

                    for step in each_object["CleanupSection"]:

                        if entity["Cleanup"] == step:

                            for each_section in each_object["CleanupSection"][step]:
                                steps_keywords += self.cleanup_helper.get_cleanup_operation(each_object["JobName"],
                                                                                            entity["EntityName"],
                                                                                            each_section,
                                                                                            counter)
                                counter += 1
                    for_job_all_entity = (
                                each_object["JobName"].replace(" ", "_") + '-' + entity["EntityName"] + END_OF_LINE +
                                tags_metadata  +
                                steps_keywords +
                                END_OF_LINE
                                )
                    each_job_cleanup += for_job_all_entity

                else:
                    pass

            cleanup_section += each_job_cleanup

        return cleanup_section
