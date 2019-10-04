"""
-------------------------------------------------------------------------------------------------
Description: TestCreationHelper holds methods that assist the testCaseGenerator.py module
             This module has all the methods that are required to print the testcases in the 
             robot code file under the *** Test Cases *** section.
            
Author: Taha Bilal Gillani

Modification Log:
---------------------------------------------------------------------------------------------------
Date						Author					                                    Description
---------------------------------------------------------------------------------------------------
24/09/2019					Taha Bilal Gillani	    	Final draft.
---------------------------------------------------------------------------------------------------\
"""
import json

TAB_SEPERATOR = '    '
END_OF_LINE = '\n'


class testcaseCreationHelper():
    '''
    Helper class for testCaseGenerator.py class. This holds all methods that help in
    constructing the string that holds the testcase in robot code fashion
    '''

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
            input_string =  '${' + input_string[1:] + '}'
            return input_string
        else:
            return input_string

    def positional_printer(self, testcase_name, section_name, key_name, data_json):
        '''
        This function takes the job name, section name, key name and data to be printer, it checks
        if the provided input is a list or a dict, if no, it wil have a name implementation in the variable
        section and it can be reference here with ${variable} structure, if yes, this value will be passed
        to stringify function which performs it's implementation.

        :param testcase_name: The name of the test case
        :type  testcase_name: str
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
            return_section = ('$' + '{' + testcase_name + '_' + section_name + '_' + key_name + '}')
            return return_section

        elif type(data_json) == list:
            return_section = ('$' + '{' + testcase_name + '_' + section_name + '_' + key_name + '}')
            return return_section

        elif type(data_json) == str:
            return_section = self.stringify(data_json)
            return return_section

        else:
            raise ValueError(
                "Is the Value entered in JobName {} , Section : {} , Key : {}".format(testcase_name, section_name,
                                                                                      key_name)
                + " Correct? \n It seems like an invalide or unsupported option. ")

    def validations(self, testcase_name, section_name, validations_json):
        '''
        It requires job name and the ingestion json as input, ingestion_json comes from
        the configuraiton file, the implementation of this function has decision statements that are taken on
        basis of the configurations provided in the JSON portion. At end it prints the test cases against the
        given configuration in the robot code file.

        :param testcase_name: name of the test case for which the section is passed
        :type testcase_name: str
        :param section_name: name of the section in test case for which the section is passed for
        :type section_name: str
        :param validations_json: the data of the section
        :type validations_json: dict
        :return: the robot code keyword implementation string to write in file
        :rtype: str
        '''

        if validations_json["Type"] == "Athena":

            if validations_json["ComparisonType"] == "RowbyRow":

                if "ExpectedOutput" in validations_json.keys():

                    if "ActualOutput" in validations_json.keys():

                        keyword_string = (TAB_SEPERATOR +
                                          'validate output athena' +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_ExpectedOutput",
                                                                  validations_json["ExpectedOutput"]) +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_ActualOutput",
                                                                  validations_json["ActualOutput"]) +
                                          END_OF_LINE
                                          )

                        return keyword_string

                    else:
                        raise KeyError(
                            "ActualOutput Type is absent or wrong in Validations section " +
                            "for Testcase {} ".format(testcase_name))
                else:
                    raise KeyError(
                        "ExpectedOutput missing in Validations Section " +
                        "for Testcase {} ".format(testcase_name))
            else:
                raise KeyError(
                    "ComparisonType is absent or incorrect in Validations " +
                    "for Testcase {} ".format(testcase_name))

        if validations_json["Type"] == "RDS":

            if "ExpectedOutput" in validations_json.keys():

                if "ActualOutput" in validations_json.keys():

                    if "Configurations" in validations_json.keys():

                        keyword_string = (TAB_SEPERATOR +
                                          'validate output rds' +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_ExpectedOutput",
                                                                  validations_json["ExpectedOutput"]) +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_ActualOutput",
                                                                  validations_json["ActualOutput"]) +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_Configurations",
                                                                  validations_json["Configurations"]) +
                                          END_OF_LINE
                                          )

                        return keyword_string

                    else:
                        raise KeyError(
                            "Configurations Type is absent or wrong in Validations section " +
                            "for Testcase {} ".format(testcase_name))
                else:
                    raise KeyError(
                        "ActualOutput Type is absent in Validations Section " +
                        "for Testcase {} ".format(testcase_name))
            else:
                raise KeyError(
                    "ExpectedOutput missing in Validations Section " +
                    "for Testcase {} ".format(testcase_name))

        if validations_json["Type"] == "Redshift":

            if "ExpectedOutput" in validations_json.keys():

                if "ActualOutput" in validations_json.keys():

                    if "Configurations" in validations_json.keys():

                        keyword_string = (TAB_SEPERATOR +
                                          'validate output redshift' +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_ExpectedOutput",
                                                                  validations_json["ExpectedOutput"]) +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_ActualOutput",
                                                                  validations_json["ActualOutput"]) +
                                          TAB_SEPERATOR +

                                          self.positional_printer(testcase_name, section_name,
                                                                  validations_json["Type"] + "_Configurations",
                                                                  validations_json["Configurations"]) +
                                          END_OF_LINE
                                          )

                        return keyword_string

                    else:
                        raise KeyError(
                            "Configurations Type is absent or wrong in Validations section " +
                            "for Testcase {} ".format(testcase_name))
                else:
                    raise KeyError(
                        "ActualOutput Type is absent in Validations Section " +
                        "for Testcase {} ".format(testcase_name))
            else:
                raise KeyError(
                    "ExpectedOutput missing in Validations Section " +
                    "for Testcase {} ".format(testcase_name))

        else:
            raise ValueError(
                "ValidationType is absent or incorrect in Validations " +
                "for Testcase {} ".format(testcase_name))

    def test_metadata(self, testcase_name, metadata_json):
        '''
        It requires testcase name and the metadata json as input, metadata_json comes from
        the configuraiton file, the metadata includes the Documentation of the test case and the tags that are
        passed to the test case in configuration file. This function prints the [Documentation] and [Tags] tags in
        the robot code file against a test case.

        :param testcase_name: name of the test came for which the metadata is to be produced
        :type  testcase_name: str
        :param metadata_json: the information that is to be formatted in robot code documentation format
        :type  metadata_json: dict
        :return: robot code formatted test case metadata
        :rtype: str
        '''
        if "Documentation" in metadata_json.keys():

            if "Tags" in metadata_json.keys():

                tags_string = ''
                for tags in metadata_json["Tags"]:
                    tags_string += TAB_SEPERATOR + str(tags)

                metadata = (
                        TAB_SEPERATOR + "[Documentation]" + TAB_SEPERATOR + metadata_json["Documentation"] +
                        END_OF_LINE +
                        TAB_SEPERATOR + "[Tags]" + tags_string + END_OF_LINE
                )

                return metadata

            else:
                raise KeyError(
                    "Tags are missing or incorrect from TestMetadata in Testcase : " + testcase_name + ".\n"
                )
        else:
            raise KeyError(
                "Descriptions is missing from TestMetadata in Testcase : " + testcase_name + ".\n")
