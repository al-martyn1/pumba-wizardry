#!/usr/bin/python3

# https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html

#require python v3

import os
import sys
import copy

# https://docs.makotemplates.org/en/latest/usage.html
from mako.template import Template as MakoTemplate
#from StringIO import StringIO

# for debug
import pprint

# https://docs.python.org/2/library/pprint.html
pp4 = pprint.PrettyPrinter( indent=4, compact=False )

# https://stackoverflow.com/questions/139180/how-to-list-all-functions-in-a-python-module
# help(pprint)
# exit(0)

# https://medium.com/python-pandemonium/how-to-test-your-imports-1461c1113be1
try:
   import commentjson as json # for automatic use C++ single line comments in jayson files
except ImportError:
   import json

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.Qt as Qt


# https://docs.python.org/3/tutorial/modules.html
# https://stackoverflow.com/questions/2349991/how-to-import-other-python-files
WizSizeMan   = __import__( 'pumba-wizsizeman', [], [], ['WizardSizeManager']    )
WizArgParser = __import__( 'pumba-wizargs'   , [], [], ['PumbaWizardArgParser'] )
pwutils      = __import__( 'pw-utils'   , [], [], ['deepupdate'] )



#---------

# https://docs.python.org/3/library/os.path.html
# normcase - ?
scriptFileName          = __file__
scriptRealFileName      = os.path.realpath(scriptFileName)           # F:\_rtc\wizardry\pumba-wizardry.py
scriptFileNameNorm      = os.path.abspath(scriptFileName)            # F:\_rtc\wizardry\pumba-wizardry.py
scriptRealFileNameNorm  = os.path.abspath(scriptFileNameNorm)        # F:\_rtc\wizardry\pumba-wizardry.py

scriptPath              = os.path.dirname( scriptFileName         )  # F:\_rtc\wizardry\wizards\tests\..\..
scriptRealPath          = os.path.dirname( scriptRealFileName     )  # F:\_rtc\wizardry
scriptPathNorm          = os.path.dirname( scriptFileNameNorm     )  # F:\_rtc\wizardry
scriptRealPathNorm      = os.path.dirname( scriptRealFileNameNorm )  # F:\_rtc\wizardry

callerFullName           = '' # F:\_rtc\wizardry\wizards\tests\test.bat
callerFullNameNoExtList  = '' # ('F:\\_rtc\\wizardry\\wizards\\tests\\test', '.bat')
callerFullNameNoExt      = '' # F:\_rtc\wizardry\wizards\tests\test

wizLauncher              = '' # test.bat
wizRcDirName             = '' # test
wizFamilyName            = '' # F:\_rtc\wizardry\wizards\tests
wizResourcesPath         = '' # F:\_rtc\wizardry\wizards\tests\test

wizardsRoot              = os.path.join( scriptRealPathNorm, 'wizards' )


#---------

verboseMode      = False

def isVeboseMode( ) :
    global verboseMode
    return verboseMode

# from tkinter import Tk, Label, Button
# root = Tk()

#see 003.py

#---------
# Command Line Interface arguments

cliArgs       = None
jsonEncoding  = 'utf-8'
selfPath      = None
app           = None
startPage   = 'welcome'
#finalPage   = 'finish'
wizCaller   = None
wizTitle    = 'Pumba Wizardry'
wizStyle    = 'classic'



#---------
# Wizard configuration from jayson config

wizOptions       = {}
wizTypes         = {}
wizConfigValues        = {}
wizPageConfigs   = {}
#wizPages         = {}
wiz              = None

#---------
# Wizard dynamic filled 
wizDynamicNext   = {}
wizResultValues  = {}
wizResultTitles  = {}
wizResultOrder   = []

#---------



# for super pumba
wizardFamilies = {}


#--------------------------------------------------
# https://doc.qt.io/archives/qt-4.8/qwizard.html#elements-of-a-wizard-page
# https://impatientprogrammer.net/2018/07/06/pyside-pyqt-qwizard-in-3-minutes/
# https://toster.ru/q/385266
# http://itnotesblog.ru/note.php?id=237

# https://www.fileformat.info/tip/web/imagesize.htm

class PumbaWizardPageBase(QtWidgets.QWizardPage):

    #-----

    def __init__(self, parent, config):
        QtWidgets.QWizardPage.__init__(self, parent)

        self.config    = config
        self.wizardWnd = parent
        self.page_name = self.config['self-name']

        wizHeight = self.wizardWnd.height()

        global wizResultTitles  # = {}
        global wizResultOrder   # = []

        

        if 'title' in config and config['title'] != '':
            self.setTitle(config['title'])

        if 'subtitle' in config and config['subtitle'] != '':
            self.setSubTitle(config['subtitle'])

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout( self.layout )

        if 'description' in config and config['description'] != '':

            dummySpaceLabel  = QtWidgets.QLabel()
            self.layout.addWidget(dummySpaceLabel);

            descriptionLabel = QtWidgets.QLabel()
            descriptionLabel.setText( config['description'] )
            self.layout.addWidget(descriptionLabel);


        self.page_type = config['page-type']
        self.pushResultOrderInfoPageName()

        if 'target-value' in self.config :
            #wizResultOrder.append( self.config['target-value'] )
            self.pushResultOrderInfo( self.config['target-value'] )
            if 'target-value-title' in self.config :
                self.setTargetValueTitle( self.config['target-value'], self.config['target-value-title'] )
                #wizResultTitles[ self.config['target-value'] ] = self.config['target-value-title']


    def setTargetValueTitle( self, targetValueName, targetValueTitle ) :

        global wizResultTitles  # = {}
        wizResultTitles[ targetValueName ] = targetValueTitle


    def pushResultOrderInfoPageName( self ) :

        global wizResultOrder   # = []

        if self.page_type=='welcome' or self.page_type=='summary' or self.page_type=='info' or ( 'summary-silent' in self.config and self.config['summary-silent'] != None ) :
            return None


        if 'title' in self.config and self.config['title'] != '':
            #self.setTitle(config['title'])
            wizResultOrder.append( '*' + self.config['title'] )

        else :
            wizResultOrder.append( '*' + self.page_type )


    def pushResultOrderInfo( self, targetValueName ) :

        global wizResultOrder   # = []

        if targetValueName not in wizResultOrder :
            wizResultOrder.append( targetValueName )



    #-----

    def simpleMessage( self, msg ) :
        #btn = QtWidgets.QMessageBox.StandardButtons.ok
        global wizTitle
        mbox = QtWidgets.QMessageBox( QtWidgets.QMessageBox.Information, wizTitle, msg, QtWidgets.QMessageBox.Ok, self )
        mbox.setModal(True)
        mbox.show()
        pass


    #-----

    def makeValueHtml( self, valName, val ) :

        global wizResultTitles
        global wizConfigValues

        if isinstance( val, str ) :
            nameTitle = valName
            if valName in wizResultTitles :
                nameTitle = wizResultTitles[valName]

            valDisplayAs = ''
            if val in wizConfigValues and 'title' in wizConfigValues[val]:
                valDisplayAs = wizConfigValues[val]['title']
            
            if valDisplayAs=='' :
                return '<B>' + nameTitle + '</B>' + ': ' + val
            else :
                return '<B>' + nameTitle + '</B>' + ': ' + valDisplayAs + ' (' + val + ')'

        elif isinstance( val, dict ) :
            return ''

        elif isinstance( val, list ) :
            return ''

        elif isinstance( val, set ) :
            return ''

        return ''

    #-----

    def makeValueHtmlWithTitle( self, valName, val ) :

        global wizResultTitles

        nameTitle = valName
        if valName in wizResultTitles :
            nameTitle = wizResultTitles[valName]

        return '<h3>' + nameTitle + '</h3>' +  self.makeValueHtml(valName, val)


    #-----

    def setTargetValue( self, value, targetValue = None ) :

        global wizResultValues

        if targetValue==None :
            if 'target-value' in self.config :
                wizResultValues[self.config['target-value']] = value
        else :
            wizResultValues[targetValue] = value

        pass

    #-----

    def clearTargetValue( self, targetValue = None ) :

        global wizResultValues

        if targetValue==None :
            if 'target-value' in self.config :
                targetValueName = self.config['target-value']
                if targetValueName in wizResultValues :
                    del wizResultValues[targetValueName]
        else :
            if targetValue in wizResultValues :
                del wizResultValues[targetValue]


    #-----

    def nextId( self ) :

        global wizDynamicNext   # = {}
        global wizConfigValues  # = {}
        global wizPageConfigs   # = {}

        nextPageName = ''

        if self.page_name in wizDynamicNext :
            nextPageName = wizDynamicNext[self.page_name]

        if nextPageName=='' :
            if 'next-page' not in self.config :
                return -1;
            nextPageName = self.config['next-page']

        if nextPageName=='' :
            return -1;

        nextPageConfig = wizPageConfigs[nextPageName]
        nextPageId     = nextPageConfig['page-id']

        return int(nextPageId)


    def checkCorrectVerticalInterval( self, interval, verticalItemsNumber ) :

        wizHeight = self.wizardWnd.height()

        if wizHeight < 400 :
            interval = interval - 1
            if len(verticalItemsNumber) > 3 :
                interval = interval - 1

        if interval < 0 :
            interval = 0

        return interval


    def getNumberOfFooterLines( self ) :

        wizHeight = self.wizardWnd.height()

        if wizHeight < 500 :
            return 2
        elif wizHeight < 800 :
            return 3
        else :
            return 4


    def addVerticalSpacing( self, n ) :
        for i in range(n) :
            dummySpaceLabel  = QtWidgets.QLabel()
            self.layout.addWidget(dummySpaceLabel)


    def addFooterLines( self ) :
        self.addVerticalSpacing(self.getNumberOfFooterLines())


    def checkAddExtraVerticalSpacing( self, itemNumber, numberOfRegularIntervals ) :
        if itemNumber==0 and numberOfRegularIntervals==0 :
            dummySpaceLabel  = QtWidgets.QLabel()
            self.layout.addWidget(dummySpaceLabel)


    def scaleControlSize( self, sz, scale, minSize = 200 ) :

        sepIdx = scale.find('/')
        if sepIdx < 0 :
            return int(scale) # assign taken value

        multiplierStr = scale[0:sepIdx]
        if multiplierStr==None or multiplierStr=='' :
            multiplierStr = '1'

        dividerStr    = scale[sepIdx+1:]
        if dividerStr==None or dividerStr=='' :
            dividerStr = '1'

        sz = sz * float(multiplierStr)
        sz = sz / float(dividerStr)

        sz = int( sz + float(0.5) )

        if sz < minSize :
            sz = minSize

        return int( sz + float(0.5) )


    def configureControlWidth( self, widget, width ) :

        if width > 0 :

            #dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)

            sizePolicy = widget.sizePolicy()
            sizePolicy.setHorizontalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
            widget.setSizePolicy(sizePolicy)

            minSize = widget.minimumSizeHint()
            minSize.setWidth(width)
            widget.setMinimumSize(minSize)



'''
        if controlsWidth!=0 :

            #dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)

            sizePolicy = listWidget.sizePolicy()
            sizePolicy.setHorizontalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
            listWidget.setSizePolicy(sizePolicy)

            minSize = listWidget.minimumSizeHint()
            minSize.setWidth(controlsWidth)
            listWidget.setMinimumSize(minSize)

            pass
'''





#--------------------------------------------------
class PumbaWizardPageRadioChoice(PumbaWizardPageBase):

    #-----

    def __init__(self, parent, config):
        PumbaWizardPageBase.__init__(self, parent, config)

        global wizConfigValues  # = {}
        global wizResultValues  # = {}

        
        radioChoices = config['radio-choice']
        radioChoicesSize = len(radioChoices)
        doVertIntervals  = 0

        if radioChoicesSize <= 2 :
            doVertIntervals = 3
        if radioChoicesSize <= 4 :
            doVertIntervals = 2
        elif radioChoicesSize <= 6 :
            doVertIntervals = 1
        else : # if radioChoicesSize <= 12 :
            doVertIntervals = 0

        doVertIntervals = self.checkCorrectVerticalInterval( doVertIntervals, radioChoicesSize )

        rbNumber = 0

        self.config['radiobutton-widgets'] = {}

        for radioButtonConfig in radioChoices :

            radiobutton = QtWidgets.QRadioButton( )

            valueName = ''
            btnKey    = 'radiobutton' + str(rbNumber)

            if 'value' not in radioButtonConfig :

                radioTitle = radioButtonConfig['text']

            else :

                valueName   = radioButtonConfig['value']
                btnKey      = valueName

                if valueName in wizConfigValues :

                    valueConfig = wizConfigValues[valueName]
                    radioTitle  = valueConfig['title'] # description also must be available
                    if 'long-title' in valueConfig :
                        radioTitle = valueConfig['long-title']
                   
                    if 'default' in radioButtonConfig and ( radioButtonConfig['default']==1 or radioButtonConfig['default']==True ):
                        config['default-choice'] = btnKey
              
                else :

                    radioTitle = radioButtonConfig['text']


            # https://pythonbasics.org/pyqt-radiobutton/

            self.checkAddExtraVerticalSpacing( rbNumber, doVertIntervals )
            
            self.addVerticalSpacing(doVertIntervals)

            '''
            if rbNumber==0 and doVertIntervals==0 :
                dummySpaceLabel  = QtWidgets.QLabel()
                self.layout.addWidget(dummySpaceLabel)
            '''

            self.layout.addWidget(radiobutton)
            radiobutton.setText( radioTitle )
            self.config['radiobutton-widgets'][ btnKey ] = radiobutton

            # https://docs.python.org/2/library/copy.html
            # https://www.learnpyqt.com/courses/start/signals-slots-events/
            # https://stackoverflow.com/questions/2216428/pyqt-qt-one-event-handler-working-with-many-items
            # https://stackoverflow.com/questions/41863366/updating-a-pyqt-qlabel-when-a-qradiobutton-associated-with-a-qcombobox-is-toggle
            # https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result

            # handler = lambda rbValue, n=valueName : self.onRadioButtonToggled( n , rbValue )
            # radiobutton.toggled.connect( handler )
            radiobutton.toggled.connect( lambda rbValue, n=valueName, i=rbNumber : self.onRadioButtonToggled( n , i, rbValue ) )

            rbNumber = rbNumber + 1

        '''
        for i in range(doVertIntervals) :
            dummySpaceLabel  = QtWidgets.QLabel()
            self.layout.addWidget(dummySpaceLabel)
        '''
        self.addVerticalSpacing(doVertIntervals)

        if 'default-choice' not in self.config and radioChoicesSize > 0:
                self.config['default-choice'] = radioChoices[0]['value']

        if radioChoicesSize > 0 :
            self.config['radiobutton-widgets'][ self.config['default-choice'] ].setChecked(True)


    #-----

    def onRadioButtonToggled( self, name, idx, rbValue ) :

        if rbValue != True :
            return None # https://stackoverflow.com/questions/6190776/what-is-the-best-way-to-exit-a-function-which-has-no-return-value-in-python-be

        global wizDynamicNext
        global wizResultValues

        radioChoices = self.config['radio-choice']
        radioButtonConfig = radioChoices[idx]

        if 'next-page' in radioButtonConfig :
            wizDynamicNext[self.page_name] = radioButtonConfig['next-page']
        elif 'next-page' in self.config :
            wizDynamicNext[self.page_name] = self.config['next-page']

        #self.setTargetValue( copy.deepcopy(name) )
        if name!='' :
            self.setTargetValue( name )
        else :
            self.clearTargetValue()

        pass


        






#--------------------------------------------------
class PumbaWizardPageListSingleSel(PumbaWizardPageBase):

    #-----

    def __init__(self, parent, config):
        PumbaWizardPageBase.__init__(self, parent, config)

        global wizConfigValues  # = {}
        global wizResultValues  # = {}


        dummySpaceLabel  = QtWidgets.QLabel()
        self.layout.addWidget(dummySpaceLabel)

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setMouseTracking(True)

        self.listWidgetItems = []

        wizWidgetsWidth = int( self.wizardWnd.getWidgetsAreaWidth() )

        controlsWidth = 0
        if 'controls-width' in config :
            controlsWidth = self.scaleControlSize( wizWidgetsWidth, config['controls-width'], 200 )

        if controlsWidth!=0 :

            #dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)

            sizePolicy = self.listWidget.sizePolicy()
            sizePolicy.setHorizontalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
            self.listWidget.setSizePolicy(sizePolicy)

            minSize = self.listWidget.minimumSizeHint()
            minSize.setWidth(controlsWidth)
            self.listWidget.setMinimumSize(minSize)

            pass


        self.layout.addWidget(self.listWidget, 0, QtCore.Qt.AlignLeft)
        self.addFooterLines()


        if 'list-choice' in config :
            config['radio-choice'] = config['list-choice']
        
        radioChoices = config['radio-choice']
        radioChoicesSize = len(radioChoices)

        rbNumber = 0

        self.config['radiobutton-widgets'] = {}


        for radioButtonConfig in radioChoices :

            #radiobutton = QtWidgets.QRadioButton( )

            radioDescription = None
            valueName = ''
            btnKey    = 'radiobutton' + str(rbNumber)

            if 'value' not in radioButtonConfig :

                radioTitle = radioButtonConfig['text']

            else :

                valueName   = radioButtonConfig['value']
                btnKey      = valueName

                if valueName in wizConfigValues :
              
                    valueConfig = wizConfigValues[valueName]
                    radioTitle  = valueConfig['title'] # description also must be available
                    if 'long-title' in valueConfig :
                        radioTitle = valueConfig['long-title']
                   
                    if 'default' in radioButtonConfig and ( radioButtonConfig['default']==1 or radioButtonConfig['default']==True ):
                        config['default-choice'] = btnKey
                   
                    #if 'description' in radioButtonConfig
                    if 'description' in valueConfig :
                        radioDescription = valueConfig['description']
                   
                    if 'description' in radioButtonConfig :
                        radioDescription = radioButtonConfig['description']

                else :

                    radioTitle = radioButtonConfig['text']


            rbNumber = rbNumber + 1

            listItem = QtWidgets.QListWidgetItem(radioTitle)
            #void QListWidgetItem::setText(const QString & text)

            if radioDescription != None and radioDescription != '' :
                listItem.setToolTip(radioDescription)
                listItem.setStatusTip(radioDescription) # https://stackoverflow.com/questions/41104372/how-to-show-qabstracttablemodels-status-in-a-qstatusbar
                

            self.listWidget.addItem(listItem)

            self.listWidgetItems.append(listItem)

            self.config['radiobutton-widgets'][ btnKey ] = listItem


        if 'default-choice' not in self.config and radioChoicesSize > 0:
                self.config['default-choice'] = radioChoices[0]['value']
                #print( 'Set \'default-choice\' to ', radioChoices[0]['value'] )

        if radioChoicesSize > 0 :
            #print( '\'default-choice\': ', self.config['default-choice'] )
            self.config['radiobutton-widgets'][ self.config['default-choice'] ].setSelected(True)
            self.onLisSelectionChanged()

        self.listWidget.itemSelectionChanged.connect( self.onLisSelectionChanged )
        #self.listWidget.toggled.connect( lambda rbValue, n=valueName, i=rbNumber : self.onRadioButtonToggled( n , i, rbValue ) )
#void QListWidget::currentItemChanged(QListWidgetItem * current, QListWidgetItem * previous)

        #self.config['radiobutton-widgets'][ self.config['default-choice'] ].setChecked(True)



    #-----

    #def onRadioButtonToggled( self, name, idx, rbValue ) :
    def onLisSelectionChanged( self ) :

        #self.simpleMessage('Selection changed')

        #print( 'Selection changed' )

        sz = len(self.listWidgetItems)
        if sz == 0 :
            return None

        curChoice = -1

        for i in range(sz) :
            item = self.listWidget.item(i)
            if item.isSelected() :
                curChoice = i
                break

        #print('curChoice: ', curChoice)

        radioChoices = self.config['radio-choice']

        if curChoice >= 0 :

            radioButtonConfig = radioChoices[curChoice]
            if 'next-page' in radioButtonConfig :
                wizDynamicNext[self.page_name] = radioButtonConfig['next-page']
            elif 'next-page' in self.config :
                wizDynamicNext[self.page_name] = self.config['next-page']

            if 'value' in radioButtonConfig:
                self.setTargetValue( radioButtonConfig['value'] )
                #print()
            else :
                self.clearTargetValue()

        else :

            self.clearTargetValue()


            #listWidgetItem = self.listWidgetItems[i]

            #self.simpleMessage( str(i) + ' of ' + str(sz) )

        #radioChoices = self.config['radio-choice']
        #radioChoicesSize = len(radioChoices)

        #rbNumber = 0


        #for i in range(n) :
        #    dummySpaceLabel  = QtWidgets.QLabel()
        #rbNumber = 0

        #self.config['radiobutton-widgets'] = {}

        #for radioButtonConfig in radioChoices :


        '''
        if rbValue != True :
            return None # https://stackoverflow.com/questions/6190776/what-is-the-best-way-to-exit-a-function-which-has-no-return-value-in-python-be

        global wizDynamicNext
        global wizResultValues

        radioChoices = self.config['radio-choice']
        radioButtonConfig = radioChoices[idx]

        if 'next-page' in radioButtonConfig :
            wizDynamicNext[self.page_name] = radioButtonConfig['next-page']
        elif 'next-page' in self.config :
            wizDynamicNext[self.page_name] = self.config['next-page']

        #self.setTargetValue( copy.deepcopy(name) )
        if name!='' :
            self.setTargetValue( name )
        else :
            self.clearTargetValue()
        '''

        pass


        







#--------------------------------------------------
class PumbaWizardPageDropdowns(PumbaWizardPageBase):

    #-----

    def __init__(self, parent, config):
        PumbaWizardPageBase.__init__(self, parent, config)

        global wizConfigValues  # = {}
        global wizResultValues  # = {}
        
        dropdownConfigList = config['dropdowns']
        dropdownConfigListSize = len(dropdownConfigList)
        doVertIntervals  = 0

        if dropdownConfigListSize <= 2 :
            doVertIntervals = 3
        if dropdownConfigListSize <= 3 :
            doVertIntervals = 2
        elif dropdownConfigListSize <= 4 :
            doVertIntervals = 1
        else :
            doVertIntervals = 0

        doVertIntervals = self.checkCorrectVerticalInterval( doVertIntervals, dropdownConfigListSize )

        wizWidgetsWidth = int( self.wizardWnd.getWidgetsAreaWidth() )

        dropdownsWidth = 0
        if 'controls-width' in config :
            dropdownsWidth = self.scaleControlSize( wizWidgetsWidth, config['controls-width'], 200 )

        '''
            dropdownsWidth = config['controls-width']

            test = self.scaleControlSize( wizWidgetsWidth, dropdownsWidth )

            if dropdownsWidth.startswith('/') :
                dropdownsWidth = int(int(wizWidgetsWidth) / int(dropdownsWidth[1:]))
            else :
                dropdownsWidth = int(dropdownsWidth)

        if dropdownsWidth!=0 and dropdownsWidth < 200:
            dropdownsWidth = 200

        '''


        comboboxNumber = 0

        self.config['dropdown-widgets'] = {}

        for dropdownConfig in dropdownConfigList :

            title = dropdownConfig['title']
            targetValue = dropdownConfig['target-value']
            
            targetValueTitle = targetValue
            if 'target-value-title' in dropdownConfig :
                targetValueTitle = dropdownConfig['target-value-title']

            dropdown = QtWidgets.QComboBox( )

            dropdownValues = dropdownConfig['values']

            addValuesLongTitle = False
            if 'add-values-long-title' in dropdownConfig and (dropdownConfig['add-values-long-title']==1 or dropdownConfig['add-values-long-title']==True):
                addValuesLongTitle = True
            
            useValuesLongTitle = False
            if 'use-values-long-title' in dropdownConfig and (dropdownConfig['use-values-long-title']==1 or dropdownConfig['use-values-long-title']==True):
                useValuesLongTitle = True

            valueIdx = 0
            defValueIdx = -1

            usedVals = set()


            for dropdownItem in dropdownValues :
    
                valueName = dropdownItem['value']

                if valueName in usedVals :
                    raise ValueError('Duplicated value \'' + valueName + '\' in dropdown \'' + title + '\'')

                usedVals.add(valueName)

                #btnKey      = valueName
                
                valueConfig = wizConfigValues[valueName]
                valueTitle  = valueConfig['title'] # description also must be available

                valueLongTitle = None

                if 'long-title' in valueConfig :
                    valueLongTitle = valueConfig['long-title']
                elif 'description' in valueConfig :
                    valueLongTitle = valueConfig['description']

                if valueLongTitle!=None :
                    if addValuesLongTitle==True :
                        valueTitle = valueTitle + ' (' + valueLongTitle + ')'
                    elif useValuesLongTitle==True :
                        valueTitle = valueLongTitle

    
                if 'default' in dropdownItem and ( dropdownItem['default']==1 or dropdownItem['default']==True ):
                    #config['default-choice'] = btnKey
                    defValueIdx = valueIdx

                dropdown.addItem(valueTitle)
    
                valueIdx = valueIdx + 1
                pass

            dropdown.setCurrentIndex(defValueIdx)
            if defValueIdx>=0 :
                self.onComboboxIndexChanged( defValueIdx, comboboxNumber, targetValue ) # not called while calling setCurrentIndex

            self.pushResultOrderInfo( targetValue )
            self.setTargetValueTitle( targetValue, targetValueTitle )




            '''
            if 'value' not in radioButtonConfig :

                radioTitle = radioButtonConfig['text']

            else :

                valueName   = radioButtonConfig['value']
                btnKey      = valueName
              
                valueConfig = wizConfigValues[valueName]
                radioTitle  = valueConfig['title'] # description also must be available
                if 'long-title' in valueConfig :
                    radioTitle = valueConfig['long-title']

                if 'default' in radioButtonConfig and ( radioButtonConfig['default']==1 or radioButtonConfig['default']==True ):
                    config['default-choice'] = btnKey
              
            '''        

            self.checkAddExtraVerticalSpacing( comboboxNumber, doVertIntervals )
            self.addVerticalSpacing(doVertIntervals)

            self.configureControlWidth(dropdown,dropdownsWidth)
            if dropdownsWidth!=0 :
                dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)

            '''
            if dropdownsWidth!=0 :

                dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)

                sizePolicy = dropdown.sizePolicy()
                sizePolicy.setHorizontalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
                dropdown.setSizePolicy(sizePolicy)

                minSize = dropdown.minimumSizeHint()
                minSize.setWidth(dropdownsWidth)
                dropdown.setMinimumSize(minSize)

                pass
            '''

            dropdownLabel  = QtWidgets.QLabel( title + ':')
            self.layout.addWidget(dropdownLabel )

            self.layout.addWidget(dropdown, 0, QtCore.Qt.AlignLeft)

            #self.config['dropdown-widgets'][ dropdownKey ] = dropdown

            dropdown.currentIndexChanged.connect( lambda idx, cbIdx=comboboxNumber, tv=targetValue : self.onComboboxIndexChanged( idx, cbIdx, tv ) )

            comboboxNumber = comboboxNumber + 1

        '''
        for i in range(doVertIntervals) :
            dummySpaceLabel  = QtWidgets.QLabel()
            self.layout.addWidget(dummySpaceLabel)
        '''
        self.addVerticalSpacing(doVertIntervals)

        '''
        if 'default-choice' not in self.config and radioChoicesSize > 0:
                self.config['default-choice'] = radioChoices[0]['value']

        self.config['radiobutton-widgets'][ self.config['default-choice'] ].setChecked(True)
        '''

    #https://doc.qt.io/qt-5/qcombobox.html#currentIndex-prop
    #connect(comboBox, QOverload<int>::of(&QComboBox::currentIndexChanged), [=](int index){ /* ... */ });

    def onComboboxIndexChanged( self, comboboxSelectionIdx, comboboxId, targetValueNameArg ) :

        #s = 'Combo \'' + str(comboboxId) + '\' target value: \'' + targetValueName + '\' - value changed to idx: ' + str(comboboxSelectionIdx)
        # self.simpleMessage( s )

        global wizDynamicNext
        global wizResultValues

        dropdownConfigList = self.config['dropdowns']
        dropdownConfig  = dropdownConfigList[comboboxId]
        dropdownValues  = dropdownConfig['values']
        targetValueName = dropdownConfig['target-value']
        valueInfo = dropdownValues[comboboxSelectionIdx]
        valueInfo['value']

        '''
        if 'next-page' in radioButtonConfig :
            wizDynamicNext[self.page_name] = radioButtonConfig['next-page']
        elif 'next-page' in self.config :
            wizDynamicNext[self.page_name] = self.config['next-page']
        '''
        #def setTargetValue( self, value, targetValue = None ) :
        self.setTargetValue( valueInfo['value'], targetValueName )




#--------------------------------------------------
class PumbaWizardPageSummary(PumbaWizardPageBase):

    #-----

    def __init__(self, parent, config):
        PumbaWizardPageBase.__init__(self, parent, config)

        global wizConfigValues  # = {}
        global wizResultValues  # = {}


        self.summaryTextField = QtWidgets.QTextEdit()
        self.layout.addWidget(self.summaryTextField);

        self.summaryTextField.setAcceptRichText(True)
        self.summaryTextField.setReadOnly(True)
        self.summaryTextField.setLineWrapColumnOrWidth(self.summaryTextField.WidgetWidth) # QTextEdit::WidgetWidth
        self.summaryTextField.setAutoFormatting(self.summaryTextField.AutoAll)
        # self.summaryTextField.setDocumentTitle('Bla-bla-bla')
        # self.summaryTextField.setPlaceholderText('Qu-qu-qu')


    #-----

    def initializePage( self ) :

        text = ''
        
        if 'title' in self.config and self.config['title'] != '' :
            text = text + '<h1>' + self.config['title'] + '</h1>' # <br/>
        else :
            text = text + '<h1>' + self.wizardWnd.windowTitle() + '</h1>' # <br/>

        #if 'title' in self.config and self.config['title'] != '' :
        #    text = text + '<h1>' + self.config['title'] + '</h1>' # <br/>

        reportedVals = set()

        sectionNumber    = 0
        inSectionCounter = 0

        for valName in wizResultOrder :

            if valName.startswith('*') :

                if sectionNumber!=0 and inSectionCounter==0 :
                    text = text + 'No options selected on this page' + '<BR/>'
                summarySubheader = valName[1:]
                if sectionNumber==0 :
                    #text = text + '<BR/>\n'
                    pass

                text = text + '<h2>' + summarySubheader + '</h2>' #  + '<BR/>\n'
                sectionNumber    = sectionNumber + 1
                inSectionCounter = 0

                continue

            if valName not in wizResultValues :
                continue

            val = wizResultValues[valName]
            #text = text + self.makeValueHtmlWithTitle( valName, val )
            text = text + self.makeValueHtml( valName, val ) + '<BR/>\n'
            # https://docs.python.org/3/library/stdtypes.html#set
            reportedVals.add(valName)

            inSectionCounter = inSectionCounter + 1

        if sectionNumber!=0 and inSectionCounter==0 :
            text = text + 'No options selected on this page' + '<BR/>'

        inSectionCounter = 0

        for valName, val in wizResultValues.items() :

            if valName in reportedVals :
                continue

            if inSectionCounter == 0 :
                text = text + '<h2>' + 'Other options' + '</h2>' #  + '<BR/>\n'

            #text = text + self.makeValueHtmlWithTitle( valName, val )
            text = text + self.makeValueHtml( valName, val ) + '<BR/>\n'

            inSectionCounter = inSectionCounter + 1

        self.summaryTextField.setHtml(text) # + '<h1>Header 1</h1>Header 1 text<br/><h2>Header 2</h2>Header 2 text<br/><h3>Header 3</h3>Header 3 text<br/><h4>Header 4</h4>Header 4 text<br/>'



'''
        dropdownsWidth = 0
        if 'controls-width' in config :
            dropdownsWidth = config['controls-width']
            if dropdownsWidth.startswith('/') :
                dropdownsWidth = int(int(wizWidgetsWidth) / int(dropdownsWidth[1:]))
            else :
                dropdownsWidth = int(dropdownsWidth)
'''










    #-----



        
# if 'radio-choice' in config :
# if self.page_type=='summary' :

def createWizardPage( parent, config ) :

    #pageType = config['self-name']
    pageType = config['page-type']

    if pageType=='welcome' : 
        return PumbaWizardPageBase(parent, config)

    elif pageType=='info' : 
        return PumbaWizardPageBase(parent, config)

    elif pageType=='radio-choice' : 
        return PumbaWizardPageRadioChoice(parent, config)

    elif pageType=='summary' : 
        return PumbaWizardPageSummary(parent, config)

    elif pageType=='dropdowns' : 
        return PumbaWizardPageDropdowns(parent, config)

    elif pageType=='listsinglesel' : 
        return PumbaWizardPageListSingleSel(parent, config)

    raise ValueError( 'Unknown page type - \'' + pageType + '\'' )



#--------------------------------------------------

class PumbaWizard(QtWidgets.QWizard):

    def getConfigValue( self, cfgValName, cliOverrideVal, defVal = None ) :

        global wizOptions

        res = None
        if cfgValName in wizOptions :
            res = wizOptions[cfgValName]

        if cliOverrideVal != None :
            res = cliOverrideVal

        if res == None or res=='':
            res = defVal

        return res;



    def __init__(self, parent) :

        QtWidgets.QWizard.__init__(self, parent)

        global wizOptions

        self.successCompleted = False

        geometryStr = self.getConfigValue( 'geometry', cliArgs.geometry, 'AUTO' )
        style       = self.getConfigValue( 'style', cliArgs.style )
        title       = self.getConfigValue( 'title', cliArgs.title, '' )

        # https://docs.makotemplates.org/en/latest/usage.html
        self.templateFile = self.getConfigValue( 'template', cliArgs.template, wizRcDirName + '.txt' )
        self.templateFile = os.path.join(wizResourcesPath, self.templateFile )
        #print( 'template: ', self.templateFile )

        self.imageWidth = 0

        self.setWindowTitle(title);
        self.setSizeGripEnabled(True)
        self.setOption(self.HaveHelpButton, False) 


        self.wizPages = {}
        self.pageIdToNameMap = {}

        if style   == None : 
            self.setWizardStyle( self.ClassicStyle )

        if style   == 'classic' : 
            self.setWizardStyle( self.ClassicStyle )

        elif style == 'modern' : 
            self.setWizardStyle( self.ModernStyle )

        elif style == 'mac' : 
            self.setWizardStyle( self.MacStyle )

        elif style == 'aero' : 
            self.setWizardStyle( self.AeroStyle )

        else :
            raise Exception('Invalid style taken')

        
        sizeManager = WizSizeMan.WizardSizeManager()

        geometry        = sizeManager.parseWizardRectString(geometryStr)
        wizScreenConfig = sizeManager.makeScreenConfigForWindow( geometry, self )
        #sizeManager.findBestWizardImage(bn,wszWin1)

        self.resize( wizScreenConfig.width , wizScreenConfig.height )
        self.move  ( wizScreenConfig.x     , wizScreenConfig.y      )

        if 'logo' in wizOptions :
            if wizOptions['logo'] != '':
                # 'file://' + 
                fileName = wizOptions['logo']
                logoPixmap = QtGui.QPixmap( fileName )
                self.setPixmap( self.LogoPixmap, logoPixmap )
       
        if 'image' in wizOptions :
            if wizOptions['image'] != '':
                fileName = wizOptions['image']
                fileName = sizeManager.findBestWizardImage( fileName, wizScreenConfig )
                if fileName != None :
                    imagePixmap = QtGui.QPixmap( fileName )
                    self.setPixmap( self.WatermarkPixmap, imagePixmap )
                    if not imagePixmap.isNull() :
                        self.imageWidth = imagePixmap.width() 
                '''
                fileName = wizOptions['image']
                filename = sizeManager.findBestWizardImage( fileName, wizScreenConfig )
                if filename != None :
                    imagePixmap = QtGui.QPixmap( fileName )
                    self.setPixmap( self.WatermarkPixmap, imagePixmap )
                '''
                    
        if 'banner' in wizOptions :
            if wizOptions['banner'] != '':
                fileName = wizOptions['banner']
                bannerPixmap = QtGui.QPixmap( fileName )
                self.setPixmap( self.BannerPixmap, bannerPixmap )

        #connect( button( QWizard::CancelButton ), SIGNAL( clicked() ), this, SLOT( cancelWizard() ) );
        #radiobutton.toggled.connect( lambda rbValue, n=valueName, i=rbNumber : self.onRadioButtonToggled( n , i, rbValue ) )

        self.button(self.CancelButton).clicked.connect( self.onCancel )
        self.button(self.FinishButton).clicked.connect( self.onFinish )
        self.currentIdChanged.connect( self.onPageChanged )




    def simpleMessage( self, msg ) :
        #btn = QtWidgets.QMessageBox.StandardButtons.ok
        global wizTitle
        mbox = QtWidgets.QMessageBox( QtWidgets.QMessageBox.Information, wizTitle, msg, QtWidgets.QMessageBox.Ok, self )
        mbox.setModal(True)
        mbox.show()
        pass
        


    def getWidgetsAreaWidth( self ) :

        selfw = self.width();
        res   = selfw - self.imageWidth - 30
        return res



    def onPageChanged( self, pageId ) :

        msg = 'Page changed to: '

        if pageId in self.pageIdToNameMap :
            msg = msg + self.pageIdToNameMap[pageId]
        else :
            msg = msg + str(pageId)

        #self.simpleMessage(msg)

        pass




    def onCancel( self ) :
        #self.simpleMessage('onCancel')
        pass



    def onFinish( self ) :
        
        global wizCaller
        global cliArgs
        global wizResultValues
        global wizardsRoot
        global wizResultValues

        self.successCompleted = True

        if (wizCaller == 'super-pumba') :

            if isVeboseMode() :
                print('wizResultValues: ')
                pp4.pprint(wizResultValues)

            cliArgs.caller = os.path.join( wizardsRoot, wizResultValues['selected-wizard'] ) + '.bat'
            wizCaller      = cliArgs.caller
            return None


        #wizResultValues  = {}
        #self.simpleMessage('onFinish')

        # !!!RENDER
        resTpl = MakoTemplate( filename=self.templateFile)

        # https://docs.makotemplates.org/en/latest/syntax.html
        renderResult = resTpl.render( wiz=wizResultValues )

        print( 'Template rendering result:' )
        print( renderResult )

        pass
    

#--------------------------------------------------
# https://docs.python.org/3/tutorial/datastructures.html
# https://snakify.org/en/lessons/dictionaries_dicts/
# dict.update( dict2 )
# dict3 = {**dict1, **dict2} 
# dict_from_class() - https://jfine-python-classes.readthedocs.io/en/latest/dict_from_class.html
# for key in A:
# for key, val in A.items():
# if 'key1' in dict:

def parseWizardryJaysonData( jaysonPath, json_data ) :

    global wizOptions
    global wizTypes
    global wizConfigValues
    global wizPageConfigs

    # https://www.programiz.com/python-programming/list

    # https://docs.python.org/3/library/os.html
    # https://pythonworld.ru/moduli/modul-os.html
    # https://pythonworld.ru/moduli/modul-os-path.html

    for key, val in json_data.items() :

        if key == 'wizard' :

            if 'icon' in val:
                if val['icon'] != '':
                    val['icon'] = os.path.abspath( os.path.join(jaysonPath, val['icon'] ) )

            if 'logo' in val :
                if val['logo'] != '':
                    val['logo'] = os.path.abspath( os.path.join(jaysonPath, val['logo'] ) )

            if 'image' in val :
                if val['image'] != '':
                    val['image'] = os.path.abspath( os.path.join(jaysonPath, val['image'] ) )

            if 'banner' in val :
                if val['banner'] != '':
                    val['banner'] = os.path.abspath( os.path.join(jaysonPath, val['banner'] ) )

            #wizOptions.update(val)
            pwutils.deepupdate(wizOptions,val)

        elif key == 'types' :
            #wizTypes.update(val)
            pwutils.deepupdate(wizTypes,val)

        elif key == 'values' :
            #wizConfigValues.update(val)
            pwutils.deepupdate(wizConfigValues,val)

        elif key == 'pages' :
            #wizPageConfigs.update(val)
            pwutils.deepupdate(wizPageConfigs,val)




#--------------------------------------------------------------------------------------------------
def readJayson( jaysonFilename ) :

    global jsonEncoding

    with open( jaysonFilename, encoding=jsonEncoding) as json_file:
        json_data = json.load(json_file)

    return json_data





#--------------------------------------------------------------------------------------------------
def parseWizardryJayson( jaysonFilename ) :

    #global jsonEncoding

    #with open( jaysonFilename, encoding=jsonEncoding) as json_file:
    #    json_data = json.load(json_file)

    jaysonPath = os.path.dirname(os.path.abspath(jaysonFilename))

    #return parseWizardryJaysonData( jaysonPath, json_data )
    return parseWizardryJaysonData( jaysonPath, readJayson(jaysonFilename) )
    




#--------------------------------------------------------------------------------------------------
def parseWizardryBuiltins( cliArgs, wizResourcesPath ) :
    # https://docs.python.org/3.4/library/os.path.html
    #####selfPath = os.path.dirname(os.path.abspath(__file__))

    global scriptPathNorm

    builtinsJaysonFileName = os.path.join(scriptPathNorm, "pumba-wizardry.builtins.json") 

    parseBuiltins = True

    if cliArgs.no_builtins == True :
        parseBuiltins = False

    if parseBuiltins :

        jaysonFilenameForOpen = os.path.abspath( os.path.join( wizResourcesPath, builtinsJaysonFileName ) )

        if cliArgs.verbose == True:
            print( "Parsing builtins from : ", jaysonFilenameForOpen )
            print()
        parseWizardryJayson(jaysonFilenameForOpen)




#--------------------------------------------------------------------------------------------------
def getWizardJaysonsList( cliArgs, wizDefJayson ) :

    wizardJaysons = []

    if cliArgs.wizard_json != None :
        wizardJaysons = cliArgs.wizard_json

    if len(wizardJaysons) == 0 :
        #wizDefJayson = wizResourcesPath + os.sep + wizRcDirName + '.json'
        wizardJaysons.append(wizDefJayson)
        if isVeboseMode() :
            print( 'Using default wizard JSON: ', wizDefJayson )
            print()

    if len(wizardJaysons)==0 :
        print("You need to take at least one jayson file as argument")
        exit()

    return wizardJaysons





#--------------------------------------------------------------------------------------------------
def parseWizardJaysons( wizardJaysons, wizResourcesPath ) :
    for jaysonFile in wizardJaysons:
        jaysonFilenameForOpen = os.path.abspath( os.path.join( wizResourcesPath, jaysonFile ) )
        if isVeboseMode() :
            print('Parsing jayson        : ', jaysonFilenameForOpen)
            print()

        parseWizardryJayson(jaysonFilenameForOpen)





#--------------------------------------------------------------------------------------------------
def createWizardPages( cliArgs, wiz ) :

    '''
    По дефолту стартовая страница носит имя 'welcome'
    Если такой страницы в наборе нет, используем первую найденную
    В builtins'ах не должно быть опции 'start-page', она может встречаться 
    только в проекте визарда
    Если в опциях есть опция 'start-page', то используется она
    Если в командной строке указан ключ --start-page, то используется его значение

    '''

    global wizPageConfigs
    global startPage

    firstPage = None
    startPageNameFound = False

    pageId = int(0)

    for pageName, pageConfig in wizPageConfigs.items() :

        pageConfig['page-id' ] = str(pageId)
        pageConfig['self-name'] = pageName

        wp = createWizardPage( wiz, pageConfig )

        wiz.setPage( pageId, wp )
        wiz.wizPages[pageName] = wp
        wiz.pageIdToNameMap[pageId] = pageName

        pageId = pageId + 1

        if firstPage==None :
            firstPage = pageName

        if startPage==pageName :
            startPageNameFound = True

        #foundFinalPage = pageName


    if not startPageNameFound :
        # Дефолтное имя стартовой страницы не найдено в наборе страниц
        # Используем имя первой найденной страницы
        startPage = firstPage

    if 'start-page' in wizOptions :
        startPage = wizOptions['start-page']

    if (cliArgs.start_page != None) and (cliArgs.start_page != '') :
        startPage = cliArgs.start_page

    startPageId = int(wizPageConfigs[startPage]['page-id'])
    wiz.setStartId(startPageId)






#--------------------------------------------------------------------------------------------------
def setWizardIcon( wiz ) :

    global wizOptions

    if 'icon' in wizOptions :
        icon = QIcon(wizOptions['icon'])
        app.setWindowIcon(icon)
        if isVeboseMode() :
            print("App icon: ", wizOptions['icon'])






#--------------------------------------------------------------------------------------------------
def fillSuperPumbaConfig( ) :

    global scriptFileName
    global scriptRealFileName
    global scriptFileNameNorm
    global scriptRealFileNameNorm

    global scriptPath
    global scriptRealPath
    global scriptPathNorm
    global scriptRealPathNorm

    global wizardFamilies

    global wizardsRoot

    json_data = {}

    #json_data['wizard'] = {}
    #json_data['types'] = {}
    #json_data['values'] = {}
    #json_data['pages'] = {}

    #wizardsRoot  = os.path.join( scriptRealPathNorm, 'wizards' )

    if isVeboseMode() :

        print( 'wizardsRoot           : ', wizardsRoot )
        print(  )

    '''
       families = {}
       families[famName]['famdir']
    '''

    wizardFamilyCandies = os.listdir(wizardsRoot)

    # iterate family subfolders
    for famCandy in wizardFamilyCandies :

        #print( 'famPath: ', famPath )
        #print( 'famName: ', os.path.basename(famPath) )

        fullFamilyCandyPath = os.path.join(wizardsRoot, famCandy)

        if not os.path.exists(fullFamilyCandyPath) or not os.path.isdir(fullFamilyCandyPath) :
            continue


        famDescriptionJayson = os.path.join( fullFamilyCandyPath, 'description.json' )

        wizardFamilies[famCandy]                     = {}
        wizardFamilies[famCandy]['name']             = famCandy
        wizardFamilies[famCandy]['path']             = fullFamilyCandyPath
        wizardFamilies[famCandy]['description-json'] = famDescriptionJayson
        wizardFamilies[famCandy]['wizards']          = {}

        # if name is a file name and file exists - try to read family jayson
        if os.path.exists(famDescriptionJayson) and os.path.isfile(famDescriptionJayson) :

            try:
                famJaysonData = readJayson( famDescriptionJayson )
                #wizardFamilies[famCandy].update(famJaysonData)
                pwutils.deepupdate( wizardFamilies[famCandy],famJaysonData)

            except:
                pass

        familyWizardsList = os.listdir(fullFamilyCandyPath)

        for wizName in familyWizardsList :

            wizFullPath = os.path.join(fullFamilyCandyPath, wizName)

            if not os.path.exists(wizFullPath) or not os.path.isdir(wizFullPath) :
                continue

            wizDescriptionJayson = os.path.join( wizFullPath, 'description.json' )

            wizardFamilies[famCandy]['wizards'][wizName]                     = {}
            wizardFamilies[famCandy]['wizards'][wizName]['name']             = wizName
            wizardFamilies[famCandy]['wizards'][wizName]['path']             = wizFullPath            
            wizardFamilies[famCandy]['wizards'][wizName]['description-json'] = wizDescriptionJayson

            if os.path.exists(wizDescriptionJayson) and os.path.isfile(wizDescriptionJayson) :

                try:
                    wizJaysonData = readJayson( wizDescriptionJayson )
                    #wizardFamilies[famCandy]['wizards'][wizName].update(wizJaysonData)
                    pwutils.deepupdate(wizardFamilies[famCandy]['wizards'][wizName],wizJaysonData)

                except:
                    pass



    # pp4.pprint(wizardFamilies)

    wizardSelectionPageValues = []


    jaysonValues = {}
    #radioChoice = []

    for wizFamily, wizFamilyConfig in wizardFamilies.items() :

        wizFamilyName         = wizFamilyConfig['name'] # same as wizFamily

        wizFamilyDisplayName = wizFamilyName
        if 'display-name' in wizFamilyConfig :
            wizFamilyDisplayName  = wizFamilyConfig['display-name']

        wizFamilyDescription = ''
        if 'description' in wizFamilyConfig :
            wizFamilyDescription  = wizFamilyConfig['description']

        if wizFamilyDisplayName!=wizFamilyName :
            wizFamilyDisplayName  = wizFamilyDisplayName + ' (' + wizFamilyName + ')'

        famWizardsDict = wizFamilyConfig['wizards']


        for wiz, wizConfig in famWizardsDict.items() :

            wizName = wizConfig['name']

            wizFullName = wizFamilyName + '/' + wizName

            jaysonValues[wizFullName] = {}

            title = wizName
            if 'display-name' in wizConfig :
                title = wizConfig['display-name']
            jaysonValues[wizFullName]['title'] = title

            description = ''
            if 'description' in wizConfig :
                description = wizConfig['description']
            jaysonValues[wizFullName]['description'] = description


            wizardSelectionPageValues.append( { 'value' : wizFullName } )


            # jaysonValues[wizFullName]['long-title']  = wizConfig['description']
            # jaysonValues[wizFullName]['description'] = wizConfig['description']
            # jaysonValues[wizFullName][''] = 

            #radioChoice.append( {} )


    #json_data['values'] = {}

    #print('JaysonValues: ', jaysonValues)
    if isVeboseMode() :
        print('JaysonValues: ')
        pp4.pprint(jaysonValues)
        print()


    json_data['values'] = jaysonValues

    json_data['pages'] = {}


    json_data['pages']['welcome'] = {}
    json_data['pages']['welcome']['next-page'] = 'super-pumba'

    json_data['pages']['super-pumba'] = {}
    json_data['pages']['super-pumba']['page-type'] = 'listsinglesel'
    json_data['pages']['super-pumba']['title']       = 'Wizard Selection'
    json_data['pages']['super-pumba']['subtitle']    = 'Wizard selection from list of installed wizards'
    json_data['pages']['super-pumba']['description'] = 'Select Wizard which your want to open:'

    json_data['pages']['super-pumba']['next-page']    = 'summary'
    json_data['pages']['super-pumba']['target-value'] = 'selected-wizard'
    json_data['pages']['super-pumba']['target-value-title'] = 'Selected wizard'

    json_data['pages']['super-pumba']['radio-choice'] = wizardSelectionPageValues # radioChoice

    if isVeboseMode() :
        print('json_data: ')
        pp4.pprint(json_data)
        print()

    return json_data







#--------------------------------------------------------------------------------------------------
def parseBasics( cliArgs ) :

    global wizCaller
    global callerFullName
    global callerFullNameNoExtList
    global callerFullNameNoExt
    
    global wizLauncher
    global wizRcDirName
    global wizFamilyName
    global wizResourcesPath

    global wizOptions
    global wizTypes
    global wizConfigValues
    global wizPageConfigs

    global scriptFileName
    global scriptRealFileName
    global scriptFileNameNorm
    global scriptRealFileNameNorm

    global scriptPath
    global scriptRealPath
    global scriptPathNorm
    global scriptRealPathNorm


    if isVeboseMode() :
        print( 'scriptRealFileName     : ', scriptRealFileName )
        print( 'scriptFileNameNorm     : ', scriptFileNameNorm )
        print( 'scriptRealFileNameNorm : ', scriptRealFileNameNorm )
        print(  )
        print( 'scriptPath             : ', scriptPath )
        print( 'scriptRealPath         : ', scriptRealPath )
        print( 'scriptPathNorm         : ', scriptPathNorm )
        print( 'scriptRealPathNorm     : ', scriptRealPathNorm )
        print(  )


    if wizCaller=='super-pumba' :

        callerFullName          = 'super-pumba'
        callerFullNameNoExtList = 'super-pumba'
        callerFullNameNoExt     = 'super-pumba'

        wizLauncher             = 'super-pumba'
        wizRcDirName            = 'super-pumba'
        wizFamilyName           = scriptRealPathNorm # os.path.dirname ( callerFullNameNoExt )
        wizResourcesPath        = os.path.join( scriptRealPathNorm, 'super-pumba' ) # os.path.join( wizFamilyName, wizRcDirName )


    else :

        callerFullName          = os.path.abspath( os.path.realpath( wizCaller ) )
        callerFullNameNoExtList = os.path.splitext(callerFullName)
        callerFullNameNoExt     = callerFullNameNoExtList[0]

        wizLauncher             = os.path.basename(callerFullName)
        wizRcDirName            = os.path.basename( callerFullNameNoExt )
        wizFamilyName           = os.path.dirname ( callerFullNameNoExt )
        wizResourcesPath        = os.path.join( wizFamilyName, wizRcDirName )


    if isVeboseMode() :
        print( "Caller                : ", callerFullName )
        print( "Caller (split by ext) : ", callerFullNameNoExtList )
        print( "Caller (w/o extention): ", callerFullNameNoExt )
        print()

    if isVeboseMode() :
        print( "Wizard launcher name  : ", wizLauncher   )
        print( "Wizard resources dir  : ", wizRcDirName  )
        print( "Wizard family root    : ", wizFamilyName )
        print( "Wizard RC full path   : ", wizResourcesPath )
        print()


    if cliArgs.caller=='super-pumba' :

        return True

    else :

        return False





#--------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    argParser  = WizArgParser.PumbaWizardArgParser()
    cliArgs    = argParser.parseArgs()
    wizCaller  = cliArgs.caller

    if cliArgs.verbose == True:
        verboseMode = True

    if isVeboseMode() :
        print()

    app = QApplication([])

    if parseBasics(cliArgs) == True :

        parseWizardryBuiltins( cliArgs, wizResourcesPath )

        wizardJaysons = [ 'super-pumba.json' ]
        parseWizardJaysons( wizardJaysons, wizResourcesPath )

        jaysonPath = wizResourcesPath
        json_data  = fillSuperPumbaConfig()

        parseWizardryJaysonData( jaysonPath, json_data )

        wiz = PumbaWizard(None)

        createWizardPages( cliArgs, wiz )
        setWizardIcon( wiz )
        wiz.show()
        app.exec_()

        if not wiz.successCompleted :
            exit(0)

        #wiz = PumbaWizard(None)

    parseBasics(cliArgs)

    parseWizardryBuiltins( cliArgs, wizResourcesPath )

    wizardJaysons = getWizardJaysonsList( cliArgs, wizResourcesPath + os.sep + wizRcDirName + '.json' )

    parseWizardJaysons( wizardJaysons, wizResourcesPath )


    # https://www.w3schools.com/python/python_ref_dictionary.asp
    # https://www.w3schools.com/python/python_dictionaries.asp

    #app = QApplication([])
    wiz = PumbaWizard(None)
    createWizardPages( cliArgs, wiz )

    if cliArgs.skip_gui == True :
        exit()

    setWizardIcon( wiz )
    wiz.show()
    app.exec_()
    exit(0)

