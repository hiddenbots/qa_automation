"""
-------------------------------------------------------------------------------------------------
Description: CleanupCreationHelper holds methods that assist the testCaseGenerator.py module
             This module has all the methods that are required to print the cleanup jobs in the
             robot code file under the *** Test Cases *** section.

Author: Taha Bilal Gillani

Modification Log:
---------------------------------------------------------------------------------------------------
Date						Author					                                    Description
---------------------------------------------------------------------------------------------------
26/09/2019					Taha Bilal Gillani	    	Initial draft.
---------------------------------------------------------------------------------------------------\
"""
TAB_SEPERATOR = '    '
END_OF_LINE = '\n'


class cleanupCreationHelper:

    def __init__(self):
        pass

    @staticmethod
    def stringify(input_string):
        '''
        Staticmethod inputs a string which is to be check if it's a reference to a varible string
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

    def positional_printer(self, job_name, entity_name, key_name, data_json):
        '''
        This function takes the job name, entity_name, key_name and data_json to be printer, it checks
        if the provided input is a list or a dict, if no, it wil have a name implementation in the variable
        section and it can be reference here with ${variable} structure, if yes, this value will be passed
        to stringify function which performs it's implementation.

        :param job_name: name of the job for the variable
        :type job_name: str
        :param entity_name: name of the entity (must be unique) for the variable
        :type entity_name: str
        :param key_name: name of the key for the variable
        :type key_name: str
        :param data_json: the data required to determine type
        :type data_json: object
        :return: variable definition in robot code for a keyword or hardcoded value
        :rtype: str
        '''

        if type(data_json) == dict:
            return ('$' + '{' + job_name.replace(' ', '_') + '_' + entity_name.replace(' ', '_') + '_' + key_name + '}')

        elif type(data_json) == list:
            return ('$' + '{' + job_name.replace(' ', '_') + '_' + entity_name.replace(' ', '_') + '_' + key_name + '}')

        elif type(data_json) == str:
            return self.stringify(data_json)
        else:
            raise ValueError(
                "Is the Value entered in JobName {} , Section : {} , Key : {}".format(
                    job_name, entity_name, key_name)
                + " Correct? \n It seems like an invalide or unsupported option. ")

    def get_cleanup_operation(self, job_name, entity_name, cleanup_json, counter):
        '''
        This function takes JobName, EntityName, CleaupJSON which is to determine type and
        a counter is passed to it to differentiate it's variable reference with other
        references

        :param job_name: Name of the Job for which the section is to be printed
        :type str
        :param entity_name: Name of the Entity for a job for which the section is to be printed
        :type str
        :param cleanup_json: The section is passed to determine it's actual or referenced type in variables
        :type dict
        :param counter: A counter is passed to ensure uniqueness between variables in a section
        :type int
        :return: returns each keyword for cleanup formatted as a string in robot code format
        :rtype: str
        '''

        if cleanup_json["OperationType"] == "DeleteTableRedshift":

            if "Configurations" in cleanup_json.keys():

                return (TAB_SEPERATOR +
                        'delete redshift table' + TAB_SEPERATOR +
                        self.positional_printer(job_name, entity_name,
                                                cleanup_json["OperationType"] + '_' + str(counter),
                                                cleanup_json["Configurations"]) +
                        END_OF_LINE
                        )
            else:
                raise KeyError(" In CleanupSection for CleanupName : {} ".format(job_name) +
                               " Configurations are either incorrect or unavailible.")

        elif cleanup_json["OperationType"] == "DeleteTableAthena":

            if "Configurations" in cleanup_json.keys():

                return (TAB_SEPERATOR +
                        'delete athena table' + TAB_SEPERATOR +
                        self.positional_printer(job_name, entity_name,
                                                cleanup_json["OperationType"] + '_' + str(counter),
                                                cleanup_json["Configurations"]) +
                        END_OF_LINE
                        )
            else:
                raise KeyError(" In CleanupSection for CleanupName : {} ".format(job_name) +
                               "Configurations are either incorrect or unavailible. ")

        elif cleanup_json["OperationType"] == "DeleteTableRDS":

            if "Configurations" in cleanup_json.keys():

                return (TAB_SEPERATOR +
                        'delete rds table' + TAB_SEPERATOR +
                        self.positional_printer(job_name, entity_name,
                                                cleanup_json["OperationType"] + '_' + str(counter),
                                                cleanup_json["Configurations"]) +
                        END_OF_LINE
                        )
            else:
                raise KeyError(" In CleanupSection for CleanupName : {} ".format(job_name) +
                               "Configurations are either incorrect or unavailible. ")

        elif cleanup_json["OperationType"] == "DeleteRowsRDS":

            if "Configurations" in cleanup_json.keys():

                return (TAB_SEPERATOR +
                        'delete rows rds' + TAB_SEPERATOR +
                        self.positional_printer(job_name, entity_name,
                                                cleanup_json["OperationType"] + '_' + str(counter),
                                                cleanup_json["Configurations"]) +
                        END_OF_LINE
                        )
            else:
                raise KeyError(" In CleanupSection for CleanupName : {} ".format(job_name) +
                               "Configurations are either incorrect or unavailible. ")
        else:
            raise ValueError(" In CleanupSection, OperationType for CleanupName : {} ".format(job_name) +
                             " OperationType is either incorrect or unavailible. ")

    def cleanup_metadata(self, tags):

        if type(tags) == list:
            tags_string = ''
            for tag in tags:
                tags_string += TAB_SEPERATOR + str(tag)
            return (
                    TAB_SEPERATOR + "[Tags]" + tags_string + END_OF_LINE
            )
        else:
            raise ValueError(
                "Tags are missing or incorrect when writing cleanup metadata")
