#!/usr/bin/python3

import os
import sys
import copy
import argparse

# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/howto/argparse.html
# https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
# https://stackoverflow.com/questions/50965583/python-argparse-multiple-metavar-names
# http://zetcode.com/python/argparse/


class PumbaWizardArgParser :

    def __init__(self):
        
        self.argParser = argparse.ArgumentParser(description='Python Umba Wizardry (c) Alex Martynov, 2019')

        self.argParser.add_argument( "--no-builtins", help="Disable all builtins"
                                   , action="store_true"
                                   , default=False
                                   )

        self.argParser.add_argument( "-v", "--verbose", help="Increase output verbosity"
                                   , action="store_true"
                                   )
    
        self.argParser.add_argument( "-s", "--style", help="Set wizard window style: classic, modern, mac, aero"
                                   , type=str
                                   )
    
        self.argParser.add_argument( "-g", "--geometry", help="Set wizard window geometry - XSIZExYSIZE[+XOFFS+YOFFS] - spaces not allowed, units are the display pixels. Use 600 for 600x480, 800 for 800x600, 1024 for 1024x768"
                                   , type=str
                                   )
    
        self.argParser.add_argument( "-U", "--skip-gui", help="Don't show GUI (for test purposes)"
                                   , action="store_true"
                                   )
    
        self.argParser.add_argument( "-S", "--start-page", help="Set wizard start page"
                                   , type=str
                                   )
    
        self.argParser.add_argument( "-T", "--title", help="Set wizard window title"
                                   , type=str
                                   )
    
        self.argParser.add_argument( "--caller", help="Set wizard caller script full name. For .bat files good value is the '--caller %%~dpnx0'"
                                   , type=str
                                   )
    
        self.argParser.add_argument( "wizard_json", nargs='*' # type=list
                                   # , required=True
                                   , help="Add wizard definition jay-son file (.json)"
                                   )

        self.argParser.add_argument( "--template", help="Set name of wizard template file"
                                   , type=str
                                   )
    

    def parseArgs(self) :
        return self.argParser.parse_args()


#--------------------------------------------------
if __name__ == '__main__':
    
    argParser = PumbaWizardArgParser()
    cliArgs   = argParser.parseArgs()

