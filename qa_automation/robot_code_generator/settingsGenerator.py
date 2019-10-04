"""
-------------------------------------------------------------------------------------------------
Description: This is an helper class for the RobotCodeGenerator Module and generates the
             *** Settings *** portion in the robot code file 
            
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


class settingsGenerator:
    '''
        This class initiates a file with the robot extention which has the robot
        code to be executed and writes the static portion
        in the robot file of the Settings
        The static code will be edited if new settings are to be imported
    '''

    def __init__(self):
        pass

    def get_settings_section(self, configuration_file):
        '''
        This classmethod returns the ***Settings*** part for the robot code
        This portion is to hardcoded if any new files are to be added or included
        using the robotframework Library keyword

        :param configuration_file: name of the configuration file which is required to form variables using robotframeword's :func: get_variables() method
        :type configuration_file: str
        :return: the ***Settings*** section for the robot code file
        :rtype: str
        '''
        section = ('Variables' + TAB_SEPERATOR + 'Modules/configuration_parser/variableGenerator.py' +
                   TAB_SEPERATOR + '{}'.format(configuration_file) + TAB_SEPERATOR +
                   'VARIABLEDUMP.json' + TAB_SEPERATOR +
                   'ENTITYVARIABLEDUMP.json' + END_OF_LINE +
                   'Library' + TAB_SEPERATOR + 'Modules/aws/validation.py' + END_OF_LINE +
                   'Library' + TAB_SEPERATOR + 'Modules/aws/job.py' + END_OF_LINE +
                   'Library' + TAB_SEPERATOR + 'Modules/aws/ingestion.py' + END_OF_LINE +
                   'Library' + TAB_SEPERATOR + 'Modules/aws/entity.py' + END_OF_LINE +
                   'Library' + TAB_SEPERATOR + 'Modules/aws/emailHelper.py' + END_OF_LINE +
                   'Library' + TAB_SEPERATOR + 'Modules/aws/dbHelper.py' + END_OF_LINE +
                   'Library' + TAB_SEPERATOR + 'Modules/aws/athenaHelper.py' + END_OF_LINE + END_OF_LINE
                   )

        return section
