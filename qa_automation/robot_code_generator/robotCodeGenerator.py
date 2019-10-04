"""

**Description**: This is an orchestration class which works in hand with modules SettingsGenerator, TestCaseGenerator, VariableGenerator. This class takes the configuration file and robot file name to be generated and generates a robot code file against the configurations.

**Author**: Taha Bilal Gillani

**Author Notes**:   Cleanup Functionality is not integrated in this file
                
`Modification Log`:


**Date			|			Author					          |                          Description**


**24/09/2019		|			Taha Bilal Gillani	   | 	Final draft.**

---------------------------------------------------------------------------------------------------\
"""
import json
from qa_automation.robot_code_generator import variablesGenerator
from qa_automation.robot_code_generator import testCaseGenerator
from qa_automation.robot_code_generator import settingsGenerator

TAB_SEPERATOR = '    '
END_OF_LINE = '\n'


class robotCodeGenerator:
    '''
    This is an orchestraction class which produces the robot code using
    the modules for file generation using the configuration file
    '''

    def __init__(self):
        pass

    def generate_code(self, configuration_file, robot_file_name):
        '''
        This method requires the configuration file name in local path and takes
        input of the robot code file name that is to be generated.
        This function goes herrarically, it reads the JSON configuration file, dumps it
        in a varialbe, the uses the SettingsGenerator module, VariablesGenerator module,
        TestCaseGenerator module. Each module returns it's parsed output in robot code fashion
        in string format

        :param configuration_file: the local file path of the configuration file
        :type configuration_file: str
        :param robot_file_name: name to be given to the generated robot code file
        :type robot_file_name: str
        '''

        '''
        Read the Configuration File to Pass JSON Objects
        '''
        configuration_json = self.configuration_convert_json(
            configuration_file)

        '''
        Settings Section Generation
        '''
        settings_generator = settingsGenerator.settingsGenerator()
        settings = settings_generator.get_settings_section(configuration_file)

        '''
        Variables Section Preperation
        '''
        variables_generator = variablesGenerator.variablesGenerator()
        entity_vars_dictionary = variables_generator.get_cleanup_configurations(configuration_json)

        # This will create a file named VARIABLEDUMP.JSON which will input
        # into a variable generator at Robotcode's runtime
        variables_generator.save_variables(configuration_json)

        # This will create a file named REPLACEVARIABLEDUMP.JSON which will input
        # into a variable generator at Robotcode's runtime
        variables_generator.save_entity_varialbes(entity_vars_dictionary)

        '''
        *****************************
        Test Case Section Generation
        ***         Jobs          ***
        ***      Test Cases       ***
        ***    Cleanup Section    ***
        *****************************
        '''

        test_case_gen = testCaseGenerator.testCaseGenerator()

        # Jobs
        jobs_dict = test_case_gen.get_jobs_configurations(configuration_json)

        jobs = ''
        for single_job in jobs_dict:
            jobs += test_case_gen.get_job(single_job['JobName'],
                                          single_job)

        # Test cases
        testcases_dict = test_case_gen.get_testcases_configurations(
            configuration_json)

        testcases = ''
        for single_testcase in testcases_dict:
            testcases += test_case_gen.get_testcase(single_testcase['Name'],
                                                    single_testcase['JobName'],
                                                    single_testcase)

        # # Cleanup cases
        cleanups = test_case_gen.perform_cleanup(entity_vars_dictionary)

        self.robot_file_generator(filename=robot_file_name,
                                  settings_section=settings,
                                  jobs_section=jobs,
                                  testcases_section=testcases,
                                  cleanups_section=cleanups
                                  )

    '''
    Helper Functions
    '''

    @staticmethod
    def configuration_convert_json(configuration_file_path):
        '''
        :param configuration_file_path: this is a local path to the json file holding the
        configuration
        :type
        :return: it returns the json dumps of the input file
        '''
        fd = open(configuration_file_path, 'r')
        file_content = fd.read()
        file_content = json.loads(file_content)
        return file_content

    # def robot_file_generator(filename, settings_section, variables_section, jobs_section, testcases_section):
    @staticmethod
    def robot_file_generator(filename, settings_section, testcases_section, jobs_section, cleanups_section):
        '''
        This is an orchestraction classmethod which takes input all the sections of robot code as string
        and dumps them into a robot extension file, ready for execution
        The Orchestraction must be in following manner

        1) **settings_section**
        2) **jobs_section**
        3) **testcases_section**
        4) **cleanups_section**

        :param filename: the name that is to be given to the to be generated robot file
        :type filename: str
        :param settings_section: settings section for the robot file
        :type settings_section: str
        :param testcases_section: testcase section for the robot file
        :type testcases_section: str
        :param variables_section: variable section for the robot file
        :type variables_section: str
        :param cleanups_section: cleanups section for robot file
        :type cleanups_section: str
        '''
        fd = open(filename, 'w')
        fd.write('*** Settings *** ' + END_OF_LINE +
                 settings_section + END_OF_LINE +
                 '***Test Cases***' + END_OF_LINE +
                 jobs_section + END_OF_LINE +
                 testcases_section + END_OF_LINE +
                 cleanups_section + END_OF_LINE
                 )
        fd.close()
