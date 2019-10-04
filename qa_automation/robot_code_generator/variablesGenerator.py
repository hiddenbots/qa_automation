"""
-------------------------------------------------------------------------------------------------
Description: VariableGenerator.py module generates the *** Variables *** section for only the hard-coded
             /static parts variables in the configuration file
            
Author: Taha Bilal Gillani

Modification Log:
---------------------------------------------------------------------------------------------------
Date						Author					                                    Description
---------------------------------------------------------------------------------------------------
24/09/2019					Taha Bilal Gillani	    	Final draft.
---------------------------------------------------------------------------------------------------\
"""
import json
from pprint import pprint

TAB_SEPERATOR = '    '
END_OF_LINE = '\n'


class variablesGenerator:
    '''
    This module produces the *** Variables *** section in the robotcode file for the 
    dictionaries and the lists involved.
    '''

    def __init__(self):

        self.variables_list = []
        self.replace_variables_list = []
        pass

    def get_configurations(self, configurations_json):
        '''
        This function extracts the "Configurations" portion from the input
        configurations JSON file

        :param configurations_json: complete configuration file json in dict
        :type configurations_json: dict
        :return: this returns the "Configurations" part from the configuration JSON
        :rtype:  dict
        '''
        configurations = configurations_json['Configurations']
        return {"Configurations": configurations}

    def get_cleanup_configurations(self, configuration_json):
        '''
        This method takes the configuration file path as an input and extracts
        the "CleanupSection" portion from the configuration file and returns it as
        a JSON dump

        :param configuration_json: the JSON dumps of the configuration file
        :type  configuration_json: dict
        :return: job_data has each object which holds a unique JobName, JobTags, Entities of the Job and complete CleanupSection
        :rtype: object
        '''

        cleanup_sections = {}

        cleanups_list = configuration_json["CleanupSection"]

        for cleanup_object in cleanups_list:
            cleanup_sections[cleanup_object["Name"]] = cleanup_object["Steps"]

        jobs_data = []

        for each_job in configuration_json["JobsDefinitions"]:
            job_object = {
                "JobName": each_job["JobName"],
                "JobTags": each_job["JobMetadata"]["Tags"],
                "Entities": each_job["Entities"],
                "CleanupSection": cleanup_sections
            }

            jobs_data.append(job_object)

        return jobs_data

    def save_variables(self, configurations_json):
        '''
        This fucntion takes the configuration file and extracts all the variables
        from the sections that are to be defined as variables and not has hardcoded
        files inside the robot code file.
        The fucntions first extracts variables from JobsDefinitions, in JobsDefinitions from
        Sections like,
        - **EntityConfigs**
        - **Ingestion**
        - **ETLWait**
        The function secondly extracts the variables from the TestCases, in Testcases from Sections
        like,
        - **Validations**

        :param configurations_json: The configuration file in JSON format
        :type configurations_json: dict
        '''
        jobs_configs = configurations_json['JobsDefinitions']
        testcase_configs = configurations_json['TestCases']

        '''
        For JobsDefinitions
        '''
        for jobs in jobs_configs:

            job_name = None

            if jobs["JobName"] and jobs["JobMetadata"]:

                job_name = jobs["JobName"].replace(' ', '_')

                '''
                Section: EntityConfiguration
                '''
                # since each job can have multiple Entity Configurations so it requires a counter logic
                counter = 0
                for entity in jobs["EntityConfigs"]:
                    self.parse_section(testcase_name=job_name,
                                       section_name='EntityConfigs_' + str(counter),
                                       section_dict=entity)
                    counter += 1
                '''
                Section: Ingestion
                '''
                # since each job can have multiple Ingestions so it requires a counter logic
                counter = 0
                for ingest in jobs["Ingestion"]:
                    self.parse_section(testcase_name=job_name,
                                       section_name='Ingestion_' + str(counter) + '_' + ingest["IngestionName"],
                                       section_dict=ingest)
                    counter += 1
                '''
                Section: ETLWait
                '''

                # Entity is a probable { key : value } that will require replacement)
                etl_dict = self.replace_values_in_section(jobs["Entities"][0], jobs["ETLWait"])

                self.parse_section(testcase_name=job_name, section_name='ETLWait',
                                   section_dict=etl_dict)

        '''
        For TestCases
        '''
        for tests in testcase_configs:

            testcase_name = None

            if tests["Name"] and tests["TestCaseType"] and tests["TestMetadata"]:

                testcase_name = tests["Name"].replace(' ', '_')

                '''
                Section: Validations
                '''
                # since each testcase can have multiple validations so it requires a counter logic
                counter = 0
                for validation in tests["Validations"]:
                    self.parse_section(testcase_name=testcase_name,
                                       section_name='Validations_' + str(counter) + '_' + validation["Type"],
                                       section_dict=validation)
                    counter += 1

            else:
                raise ValueError("Either Test Case Name, it's TestCaseType or TestMetadata is " +
                                 "missing from one of the mentioned testcases in configuration file.")

        self.dump_variables(filename="VARIABLEDUMP.json")

    def dump_variables(self, filename):
        '''
        This functions on making a decision on filename generates a JSON
        file locally including the variables

        :param filename: this filename suggest in which file the variables are to be saved
        :type filename: str
        '''
        if filename == "VARIABLEDUMP.json":
            fd = open(filename, 'w')

            json_to_dump = {
                "RequiredVariables": self.variables_list
            }

            fd.write(json.dumps(json_to_dump))
            fd.close()

        if filename == "ENTITYVARIABLEDUMP.json":
            fd = open(filename, 'w')

            json_to_dump = {
                "RequiredVariables": self.replace_variables_list
            }

            fd.write(json.dumps(json_to_dump))
            fd.close()

    def save_entity_varialbes(self, entity_json):
        '''
        In our code flow, the cleanup section is generic and runs for multiple
        entites by replacing the values passed in the "Entities" section inside the JSON
        configuration file. This functions inputs a complex defined variable entity_json which includes
        "JobName": string,
        "JobTags": string,
        "Entities": a list of objects,
        "CleanupSection" : a list of nested objects
        It utilizes this information to create variables used for the CleanupSection

        :param entity_json: entity json holds JobName, CleanupSection, JobTags and Entites for that Job
        :type  entity_json: object
        '''

        # entity_json has variable objects that are in
        # definition packed by function : get_cleanup_configuration
        # "JobName": string,
        # "JobTags": string,
        # "Entities": a list of objects,
        # "CleanupSection" : a list of nested objects

        for object in entity_json:

            job_name = object["JobName"]
            entities = object["Entities"]
            cleanup_section_list = object["CleanupSection"]

            # Each list object in CleanupSection is divided as
            # [  { Name : step name
            #      Steps : a list of steps to follow
            #    } ]

            # This conversion is made because the json.loads() function
            # being used does not properly treat objects unless
            # they are not in proper JSON format

            for each_object_key in cleanup_section_list:

                section = {
                    "Name": each_object_key,
                    "Section": cleanup_section_list[each_object_key]
                }

                # Now we iterated through each entity defined in a single JobsDefinition
                # Section

                for entity in entities:

                    # Each entity will have many steps to follow and steps can have similar names,
                    # so we use a counter to differentiate them

                    counter = 0

                    # Iterate through the list of sections extracted from the
                    # cleanup section

                    for each_section in section["Section"]:

                        # We opt only for that section that the
                        # entity has defined for itself in the configuration file
                        # else we pass that element in the list

                        if section["Name"] == entity["Cleanup"]:

                            str_section = json.dumps(each_section)

                            for key in entity:
                                if key == "Cleanup":
                                    pass
                                else:
                                    str_section = str_section.replace('{' + key + '}', entity[key])

                            dict_section = json.loads(str_section)

                            self.variable_object("Replace",
                                                 job_name,
                                                 entity["EntityName"],
                                                 dict_section["OperationType"] + '_' + str(counter),
                                                 dict_section["Configurations"])
                            counter += 1
                        else:
                            pass

        self.dump_variables(filename="ENTITYVARIABLEDUMP.json")

    def parse_section(self, testcase_name, section_name, section_dict):
        '''
        Takes a section as input like ingestion, validations etc and creates required dictionaries
        and lists variables in robot code file. This method returns the parse section as a string.
        This method uses other two methods like variable_dictionary and variable_list.

        :param testcase_name: Name of the testcase for which the section is to be parsed
        :type testcase_name: str
        :param section_name: Section of the testcase for which the section is to be parsed
        :type section_name: str
        :param section_dict: This depends on the input, it may be a list, a dictionary or a complex nested object
        :type section_dict: object
        '''

        for keys in section_dict:

            if type(section_dict[keys]) is dict or type(section_dict[keys]) is list:

                if keys == "Steps":
                    if "Ingestion" in section_name:
                        send_dict = {
                            "Steps": section_dict[keys]
                        }

                        self.variable_object("Plain",
                                             testcase_name, section_name, keys, send_dict)
                else:
                    self.variable_object("Plain",
                                         testcase_name, section_name, keys, section_dict[keys])
            else:
                pass

    def variable_object(self, list_type, testcase_name, section_name, key, value):
        '''
        It forms a list variable for the robot code against a list and returns
        it as a string on basis of the passed parameters

        :param list_type: this determines in which list to append the variables into
        :type list_type: str
        :param testcase_name: name of the testcase for which the variable is to be generated
        :type testcase_name: str
        :param section_name: section name of the testcase for which the variable is to be generated
        :type section_name: str
        :param key: This key is basically the operation type or the choice taken inside the section to generate the variable for
        :type key: str
        :param value: This is the object for the variable that will be packed and added to a global list on basis of the list_type choice
        :type  value: dict
        '''

        format_name = '{}_{}_{}'.format(testcase_name, section_name, key)
        object_name = '{}'.format(format_name)

        object_pack = {
            "Name": object_name,
            "Value": value
        }

        if list_type == 'Plain':
            self.variables_list.append(object_pack)
        if list_type == 'Replace':
            self.replace_variables_list.append(object_pack)

    def replace_values_in_section(self, entity, section):
        '''
        This function inputs entity with it's other defined parameters and replaces
        them in a section, in section it's mentioned with the key in entities like EntityName, Domain etc

        :param entity: A single entity object which has EntityName, Cleanup and other optional key value pairs
        :type entity: dict
        :param section: the section in which the file is to be replaced
        :type section: object
        :return: The section sent as parameter with replaced values with entity dict keys
        :rtype: dict
        '''

        dummy_section = { "Dummy": section }
        dict_to_json = json.dumps(dummy_section)

        for key in entity:
            if key == "Cleanup":
                pass
            else:
                dict_to_json = dict_to_json.replace('{' + key + '}', entity[key])

        json_to_dict = json.loads(dict_to_json)
        replaced_section = json_to_dict["Dummy"]

        return replaced_section
