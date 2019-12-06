#!/usr/bin/python3

import os
import sys
import copy

from PyQt5.QtWidgets import QApplication, QWidget
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore


#--------------------------------------------------
class WizardPageSizeInfo :

    def __init__( self ) :

        self.width           = []
        self.height    : int = 0
        self.imgHeight : int = 0


#--------------------------------------------------
class WizardScreenSize :

    def __init__( self, w = None, h = None, x = None, y = None ) :

        self.width  = w
        self.height = h
        self.x      = x
        self.y      = y

        self.widenessError       : int = -1
        self.widenessNarrow      : int =  0
        self.widenessNormal      : int =  1
        self.widenessWide        : int =  2
        self.widenessSuperWide   : int =  3
        self.widenessExtraWide   : int =  4
        self.sizeAuto            : int =  5


    def getRatio( self ) :
        return self.width / self.height


    def widenessStringToEnum( self, strWideness ) :
    
        if strWideness == None :
            strWideness = ''

        strWideness = strWideness.lower()

        if strWideness == None or strWideness == '' or strWideness == 'norm' or strWideness == 'normal' :
            return self.widenessNormal
        elif strWideness == 'narrow' :
            return self.widenessNarrow
        elif strWideness == 'wide' :
            return self.widenessWide
        elif strWideness == 'super' or strWideness == 'superw' or strWideness == 'superwide' :
            return self.widenessSuperWide
        elif strWideness == 'extra' or strWideness == 'extraw' or strWideness == 'extrawide' :
            return self.widenessExtraWide
        elif strWideness == 'auto' :
            return self.sizeAuto
        else :
            return self.widenessError
            #raise ValueError('Fucking shit in params')


    def isValueAuto( self, val ) :

        if val == None :
            return True

        if isinstance( val, str ) :
            e = self.widenessStringToEnum( val )
            if e == self.sizeAuto :
                return True

        return False


    def isValueWideness( self, val ) :

        if val == None :
            return False

        if isinstance( val, str ) :
            e = self.widenessStringToEnum( val )
            if e >= self.widenessNarrow and e <= self.widenessExtraWide :
                return True

        return False


    def isValueInt( self, val ) :

        if val == None :
            return False

        if isinstance( val, int ) :
            return True

        return False


    def isWidthAuto( self ) :
        return self.isValueAuto(self.width)

    def isWidthWideness( self ) :
        return self.isValueWideness(self.width)

    def isWidthInt( self ) :
        return self.isValueInt(self.width)

    def isHeightAuto( self ) :
        return self.isValueAuto(self.height)

    def isHeightWideness( self ) :
        return self.isValueWideness(self.height)

    def isHeightInt( self ) :
        return self.isValueInt(self.height)


    def formatToString( self ) :

        s = ''

        if self.width == None :
            s = s + 'AUTO'
        #if isinstance( self.width, int ) :
        else :
            s = s + str(self.width)

        s = s + 'x'

        if self.height == None :
            s = s + 'AUTO'
        else :
            s = s + str(self.height)

        s = s + '+'

        if self.x == None :
            s = s + 'AUTO'
        else :
            s = s + str(self.x)

        s = s + '+'

        if self.y == None :
            s = s + 'AUTO'
        else :
            s = s + str(self.y)

        return s


    def makeHeightsForWidth( self, w ) :
        res = []
        res.append( int(w * (1 / 1.3) ) ) # 1.3 narrow
        res.append( int(w * (1 / 1.5) ) ) # 1.5 normal (default)
        res.append( int(w * (1 / 1.7) ) ) # 1.7 wide
        res.append( int(w * (1 / 2.0) ) ) # 2.0 superwide
        res.append( int(w * (1 / 2.5) ) ) # 2.0 extrawide
        return res


    def makeWidthsForHeight( self, h ) :
        res = []
        res.append( int(h * (1.3) ) ) # 1.3 narrow
        res.append( int(h * (1.5) ) ) # 1.5 normal (default)
        res.append( int(h * (1.7) ) ) # 1.7 wide
        res.append( int(h * (2.0) ) ) # 2.0 superwide
        res.append( int(h * (2.5) ) ) # 2.0 extrawide
        return res


    # width=ENUM, height - known
    def getScaledWidth( self ) :

        e = self.widenessStringToEnum(self.width)
        if e==self.widenessError or e==self.sizeAuto :
            e = 0

        scales = self.makeWidthsForHeight(self.height)
        return scales[e]


    # height=ENUM, width - known
    def getScaledHeight( self ) :

        e = self.widenessStringToEnum(self.height)
        if e==self.widenessError or e==self.sizeAuto :
            e = 0

        scales = self.makeHeightsForWidth(self.width)
        return scales[e]



class WizardSizeManager :


    #-------
    def __init__( self ) :

        self.widenessError       : int = -1
        self.widenessNarrow      : int =  0
        self.widenessNormal      : int =  1
        self.widenessWide        : int =  2
        self.widenessSuperWide   : int =  3
        self.widenessExtraWide   : int =  4
        self.sizeAuto            : int =  5


    #-------
    def intDistance( self, v1 : int, v2 : int ) :
        d : int = v1 - v2
        if d<0 :
            d = -d
        return d


    #--------------------------------------------------
    def findNearestIntegerValue( self, v : int, fixedVals, prefferLower ) :
    
        leftVal = None
    
        for rightVal in fixedVals :
    
            if leftVal==None :
                continue
    
            leftDistance   = self.intDistance( v, leftVal  )
            rightDistance  = self.intDistance( v, rightVal )
    
            if leftDistance == rightDistance :
                if prefferLower==True :
                    return leftVal
                else :
                    return rightVal
    
            if leftDistance < rightDistance :
                return leftVal
            else :
                return rightVal
    

    #--------------------------------------------------
    def roundImpl( self, x : int, d : int ) :
        denominated = x // d
        reminder    = x  % d
    
        if reminder >= int(d/2) :
            return int( (denominated+1) * d )
        else :
            return int(  denominated    * d )


    #--------------------------------------------------
    def round10( self, x : int ) :
        return self.roundImpl( x, int(10) )
    


    #--------------------------------------------------
    def widenessStringToEnum( self, strWideness ) :
    
        if strWideness == None :
            strWideness = ''

        strWideness = strWideness.lower()

        if strWideness == None or strWideness == '' or strWideness == 'norm' or strWideness == 'normal' :
            return self.widenessNormal
        elif strWideness == 'narrow' :
            return self.widenessNarrow
        elif strWideness == 'wide' :
            return self.widenessWide
        elif strWideness == 'super' or strWideness == 'superw' or strWideness == 'superwide' :
            return self.widenessSuperWide
        elif strWideness == 'extra' or strWideness == 'extraw' or strWideness == 'extrawide' :
            return self.widenessExtraWide
        elif strWideness == 'auto' :
            return self.sizeAuto
        else :
            return self.widenessError
            #raise ValueError('Fucking shit in params')
    
    
    #--------------------------------------------------
    def makeScreenHeightsForWidth( self, w ) :
        res = []
        res.append( int(w * (1 / 1.3) ) ) # 1.3 narrow
        res.append( int(w * (1 / 1.5) ) ) # 1.5 normal (default)
        res.append( int(w * (1 / 1.7) ) ) # 1.7 wide
        res.append( int(w * (1 / 2.0) ) ) # 2.0 superwide
        res.append( int(w * (1 / 2.5) ) ) # 2.0 extrawide
        return res
    

    #--------------------------------------------------
    def getScreenSize( self, widget ) :

        #wiz = QtWidgets.QWizard()
        desktopWidget  = QtWidgets.QDesktopWidget()
        screenGeometry = desktopWidget.screenGeometry( widget )
        #qTscrRect        = ScreenSize( screenGeometry.height() , screenGeometry.width() )
        screenSize = WizardScreenSize( screenGeometry.width(), screenGeometry.height(), screenGeometry.x(), screenGeometry.y() )
        #screenRect = ScreenRect()
        return screenSize
        #pass

    def getRatioEnum( self, r ) :

        if r <= 1.3 :
            return self.widenessNarrow
        elif r <= 1.5 :
            return self.widenessNormal
        elif r <= 1.7 :
            return self.widenessWide
        elif r <= 2.0 :
            return self.widenessSuperWide
        else :
            return self.widenessExtraWide


    def getRatioEnumName( self, r ) :

        if r == self.widenessNarrow :
            return 'NARROW'
        elif r == self.widenessNormal :
            return 'NORMAL'
        elif r == self.widenessWide :
            return 'WIDE'
        elif r == self.widenessSuperWide :
            return 'SUPERWIDE'
        elif r == self.widenessExtraWide :
            return 'AUTO'
        elif r == self.sizeAuto :
            return 'AUTO'
        else : 
            return 'ERROR'


    #--------------------------------------------------
    def parseWizardRectString( self, screenRectStr ) :

         wsz = WizardScreenSize()
         wsz.x      = None
         wsz.y      = None
         wsz.width  = None
         wsz.height = None

         # https://docs.python.org/3/library/stdtypes.html#string-methods
         # https://www.w3schools.com/python/python_ref_string.asp

         sizeAndOffsetStrings = screenRectStr.split('+')

         # Size

         if len(sizeAndOffsetStrings) > 0 :

             sizeStrings = sizeAndOffsetStrings[0].split('x')

             if len(sizeStrings) > 1 : # XxY taken both

                 yStr = sizeStrings[1]

                 if yStr == '' :
                     pass
                 elif yStr.isdecimal() :
                     wsz.height = int(yStr)
                 else :
                     yEnum = self.widenessStringToEnum(yStr)
                     if yEnum == self.widenessError :
                         raise ValueError('Invalid Height')
                     else :
                         wsz.height = yStr # store as string

             if len(sizeStrings) > 0 : # at least X size was taken

                 xStr = sizeStrings[0]

                 if xStr == '' :
                     pass
                 elif xStr.isdecimal() :
                     wsz.width = int(xStr)
                 else :
                     xEnum = self.widenessStringToEnum(xStr)
                     if xEnum == self.widenessError :
                         raise ValueError('Invalid Width')
                     else :
                         wsz.width = xStr # store as string

         # Position

         if len(sizeAndOffsetStrings) > 1 :

             #offsetStrings = sizeAndOffsetStrings[1].split('+')
             xStr = sizeAndOffsetStrings[1]

             if xStr == '' :
                 pass
             elif xStr.isdecimal() :
                 wsz.x = int(xStr)
             else :
                 xEnum = self.widenessStringToEnum(xStr)
                 if xEnum != self.sizeAuto :
                     raise ValueError('Invalid X Position')
                 else :
                     wsz.x = xStr # store as string

         if len(sizeAndOffsetStrings) > 2 :

             yStr = sizeAndOffsetStrings[2]

             if yStr == '' :
                 pass
             elif yStr.isdecimal() :
                 wsz.y = int(yStr)
             else :
                 yEnum = self.widenessStringToEnum(yStr)
                 if yEnum != self.sizeAuto :
                     raise ValueError('Invalid Y Position')
                 else :
                     wsz.y = yStr # store as string

         return wsz


    #--------------------------------------------------
    def mergeWizardScreenSize( self, wszMergeTo, wszMergeFrom ) :

        wsz = WizardScreenSize()

        if wszMergeTo.width != None :
            wsz.width = wszMergeTo.width
        else :
            wsz.width = wszMergeFrom.width

        if wszMergeTo.height != None :
            wsz.height = wszMergeTo.height
        else :
            wsz.height = wszMergeFrom.height

        if wszMergeTo.x != None :
            wsz.x = wszMergeTo.x
        else :
            wsz.x = wszMergeFrom.x

        if wszMergeTo.y != None :
            wsz.y = wszMergeTo.y
        else :
            wsz.y = wszMergeFrom.y

        return wsz


    def chooseHeight( self, screenSize ) :

        if screenSize.height <= 500 :    # 500*0.93 = 465
            return int(screenSize.height*0.93)

        elif screenSize.height <= 700 :  # 700*0.85 = 595
            return int(screenSize.height*0.85)

        elif screenSize.height <= 1000 : # 1000*0.7 = 700
            return int(screenSize.height*0.7)

        elif screenSize.height <= 1200 : # 1200*0.6 = 720
            return int(screenSize.height*0.6)

        else:
            return int(screenSize.height*0.5)
    


    def makeScreenConfigForWindow( self, wszConfigOrg, wnd ) :

        screenSize = self.getScreenSize( wnd )
        wszConfig  = wszConfigOrg

        scrRatio         = screenSize.getRatio()
        scrRatioEnum     = self.getRatioEnum( scrRatio )
        scrRatioEnumName = self.getRatioEnumName(scrRatioEnum)


        if wszConfig.isWidthWideness() and wszConfig.isHeightWideness() :
            raise ValueError('Width and Height are both wideness')

        # 640 x  350 - min screen size
        if wszConfig.isWidthInt() and wszConfig.width < 400 :
            wszConfig.width = 400

        if wszConfig.isHeightInt() and wszConfig.height < 300 :
            wszConfig.height = 300

        # scale = 0.936
        scale = 0.8

        
        if wszConfig.isWidthInt() and wszConfig.width > screenSize.width*scale :
            wszConfig.width  = int(screenSize.width*scale)
            wszConfig.height = scrRatioEnumName

        if wszConfig.isHeightInt() and wszConfig.height > screenSize.height*scale :
            wszConfig.height  = int(screenSize.height*scale)
            wszConfig.width   = scrRatioEnumName


        '''

        Задаются размеры окна, а не экрана

        И W и H могут быть как AUTO, так один из enum'ов
        Оба не могут быть enum'ами

        W           H

 [x]    N           N           - координаты заданы
 [ ]    WIDENESS    N           - W - вычисляем
 [ ]    AUTO        N           - W - вычисляем, как WIDENESS, при этом WIDENESS берем от экрана

 [ ]    N           WIDENESS    - H - вычисляем
 [x]    WIDENESS    WIDENESS    - запрещено
 [ ]    AUTO        WIDENESS    - выбираем W, H - вычисляем

 [ ]    N           AUTO        - H - вычисляем, как WIDENESS, при этом WIDENESS берем от экрана
 [ ]    WIDENESS    AUTO        - выбираем H, W - вычисляем
 [ ]    AUTO        AUTO        - аналогично AUTO        WIDENESS
        
        '''

        if wszConfig.isWidthInt() :

            if wszConfig.isHeightInt() :         # N  N
                pass

            elif wszConfig.isHeightWideness() :  # N  WIDENESS
                wszConfig.height = wszConfig.getScaledHeight()

            else : # auto                        # N  AUTO
                wszConfig.height = scrRatioEnumName
                wszConfig.height = wszConfig.getScaledHeight()

        elif wszConfig.isWidthWideness() :

            if wszConfig.isHeightInt() :         # WIDENESS  N
                wszConfig.width = wszConfig.getScaledWidth()

            elif wszConfig.isWidthWideness() :   # not allowed
                pass

            else : # auto                        # WIDENESS AUTO
                # выбираем H, W - вычисляем
                wszConfig.height = wszConfig.chooseHeight(screenSize)
                wszConfig.width  = wszConfig.getScaledWidth() # WIDENESS  N

            self.width = self.getScaledWidth()

        else : # auto

            if wszConfig.isHeightInt() :         # AUTO  N
                wszConfig.width = wszConfig.getScaledWidth()

            elif wszConfig.isWidthWideness() :   # AUTO  WIDENESS
                # выбираем W, H - вычисляем
                # схитрим и сделаем наоборот
                wszConfig.width  = wszConfig.height
                wszConfig.height = self.chooseHeight(screenSize)
                # wszConfig.width  = #scrRatioEnumName
                wszConfig.width  = wszConfig.getScaledWidth()

            else : # auto                        # AUTO  AUTO
                # аналогично AUTO  WIDENESS
                # выбираем W, H - вычисляем
                wszConfig.width  = wszConfig.height
                wszConfig.height = self.chooseHeight(screenSize)
                #wszConfig.width  = scrRatioEnumName
                wszConfig.width  = wszConfig.getScaledWidth()


        if wszConfig.x == None :
            wszConfig.x = int( (screenSize.width - wszConfig.width) / 2 )

        if wszConfig.y == None :
            wszConfig.y = int( (screenSize.height - wszConfig.height) / 2 )

        if ( wszConfig.x+wszConfig.width) > screenSize.width :
            wszConfig.x = screenSize.width - wszConfig.width

        if ( wszConfig.y+wszConfig.height) > screenSize.height :
            wszConfig.y = screenSize.height - wszConfig.height

        return wszConfig


    def generateImageHeightCandidates( self, wszConfig ) :

        imgHeight = wszConfig.height - 160
        if (imgHeight<0) :
            return []

        imgHeight = self.round10(imgHeight)

        maxValUnder = int(imgHeight / 10)
        minValUnder = int(maxValUnder - 10)
        if minValUnder < 8 :
            minValUnder = int(8)

        rangeValUnder = int(maxValUnder - minValUnder)
        if rangeValUnder < 0 : 
            rangeValUnder = int(0)

        rangeValUpper = 19

        if imgHeight > 3000 :
            rangeValUpper = 49
            rangeValUnder = 24
        elif imgHeight > 2200 :
            rangeValUpper = 39
            rangeValUnder = 19
        elif imgHeight > 1500 :
            rangeValUpper = 29
            rangeValUnder = 15

        under = [ int(imgHeight-i*10) for i in range(rangeValUnder) ]
        upper = [ int(imgHeight+(i+1)*10) for i in range(rangeValUpper) ]
        return [ *under, *upper ]

        #imgs = [ rh-i*10 for i in range(0, 15) ]


    def findBestWizardImage( self, imgFullFilenameOrg, wszConfig ) :

        # imgFullFilename = os.path.normpath(imgFullFilenameOrg)
        imgFullFilename = imgFullFilenameOrg

        hlst = self.generateImageHeightCandidates( wszConfig )

        if len(hlst) == 0:
            return None

        nameParts = os.path.splitext(imgFullFilename)

        # names = []

        for no in hlst :

            name = ''

            if len(nameParts) > 0 and nameParts[0] != None :
                name = nameParts[0]
            name = name + '_' + str(no)

            if len(nameParts) > 1 and nameParts[1] != None :
                name = name + nameParts[1]

            if os.path.exists(name) and os.path.isfile(name) :
                return name

        if os.path.exists(imgFullFilename) and os.path.isfile(imgFullFilename) :
            return imgFullFilename

        return None






#--------------------------------------------------
if __name__ == '__main__':
    
    #class WizardSizeInfo

    #help(__import__)
    #print('------------------------')
    help(os)
    print('------------------------')
    help(os.path)
    print('------------------------')

    sizeManager = WizardSizeManager()

    # lists - https://otus.ru/nest/post/585/
    # tuples - https://realpython.com/python-lists-tuples/#python-tuples
    
    widths      = [ 640 , 720 , 768 , 800 , 832 , 854 , 864 , 900 , 960 , 1024, 1120, 1152, 1080, 1152, 1200, 1280, 1366, 1440, 1536, 1600, 1680, 1800, 1920, 2048, 2160, 2400, 2560, 2880, 3200, 3840, 4096, 4320, 4800, 5120, 6400, 7680 ]
    resolutions = [ ( 160, 200   ), ( 256, 192   ), ( 320, 200   ), ( 320, 240   ), ( 320, 256   ), ( 400, 240   ), ( 400, 288   ), ( 640, 200   ), ( 480, 272   ), ( 512, 256   ), ( 466, 288   ), ( 480, 320   ), ( 640, 256   ), ( 640, 256   ), ( 640, 272   ), ( 512, 342   ), ( 640, 288   ), ( 512, 384   ), ( 640, 350   ), ( 720, 348   ), ( 720, 350   ), ( 640, 400   ), ( 720, 360   ), ( 640, 480   ), ( 640, 512   ), ( 800, 480   ), ( 854, 466   ), ( 854, 480   ), ( 800, 600   ), ( 784, 640   ), ( 800, 640   ), ( 960, 540   ), ( 960, 544   ), ( 1024, 576  ), ( 960, 640   ), ( 1024, 600  ), ( 1152, 648  ), ( 1024, 768  ), ( 1152, 720  ), ( 1200, 720  ), ( 1152, 768  ), ( 1280, 720  ), ( 1120, 832  ), ( 1280, 768  ), ( 1152, 864  ), ( 1280, 800  ), ( 1152, 900  ), ( 1366, 768  ), ( 1280, 854  ), ( 1280, 960  ), ( 1600, 768  ), ( 1440, 900  ), ( 1280, 1024 ), ( 1536, 864  ), ( 1440, 960  ), ( 1600, 900  ), ( 1400, 1050 ), ( 1440, 1080 ), ( 1600, 1024 ), ( 1680, 1050 ), ( 1600, 1200 ), ( 1920, 1080 ), ( 2048, 1080 ), ( 1920, 1200 ), ( 2048, 1152 ), ( 1920, 1280 ), ( 1920, 1440 ), ( 2048, 1536 ), ( 2560, 1080 ), ( 2560, 1440 ), ( 2560, 1600 ), ( 2880, 1800 ), ( 2560, 2048 ), ( 3200, 2048 ), ( 3280, 2048 ), ( 3200, 2400 ), ( 3840, 2160 ), ( 3840, 2400 ), ( 5120, 4096 ), ( 6400, 4096 ), ( 6400, 4800 ), ( 7680, 4320 ), ( 7680, 4800 ) ] 

    app = QApplication([])
    wiz = QtWidgets.QWizard()
    screenSize = sizeManager.getScreenSize( wiz )

    scrRatio         = screenSize.getRatio()
    scrRatioEnum     = sizeManager.getRatioEnum( scrRatio )
    scrRatioEnumName = sizeManager.getRatioEnumName( scrRatioEnum )
    print('Screen size: ', screenSize.width, ' x ', screenSize.height, ', pos: ', screenSize.x, ' x ', screenSize.y )
    print('Ratio: ', "{0:.1f}".format( scrRatio ) )
    print('Ratio enum: ', scrRatioEnum )
    print('Ratio name: ', scrRatioEnumName )

    print('------------------------')

    wszStr1 = '800x600+50'
    wszStr2 = '800++50'
    wszStr3 = '800'
    wszStr4 = 'xEXTRA+100'
    wszStr5 = 'AUTO'

    print('Wsz 1: ', wszStr1 )
    print('Wsz 2: ', wszStr2 )
    print('Wsz 3: ', wszStr3 )
    print('Wsz 4: ', wszStr4 )
    print('Wsz 5: ', wszStr5 )

    print('-----')


    wsz1 = sizeManager.parseWizardRectString(wszStr1)
    wsz2 = sizeManager.parseWizardRectString(wszStr2)
    wsz3 = sizeManager.parseWizardRectString(wszStr3)
    wsz4 = sizeManager.parseWizardRectString(wszStr4)
    wsz5 = sizeManager.parseWizardRectString(wszStr5)

    print('Parsed 1: ', wsz1.formatToString() )
    print('Parsed 2: ', wsz2.formatToString() )
    print('Parsed 3: ', wsz3.formatToString() )
    print('Parsed 4: ', wsz4.formatToString() )
    print('Parsed 5: ', wsz5.formatToString() )

    print('-----')

    wsz34 = sizeManager.mergeWizardScreenSize( wsz3, wsz4 )
    print('Merged 34: ', wsz34.formatToString() )

    print('-----')

    #makeScreenConfigForWindow( self, wszConfigOrg, wnd ) :

    wszWin1 = sizeManager.makeScreenConfigForWindow( wsz1, wiz )
    wszWin2 = sizeManager.makeScreenConfigForWindow( wsz2, wiz )
    wszWin3 = sizeManager.makeScreenConfigForWindow( wsz3, wiz )
    wszWin4 = sizeManager.makeScreenConfigForWindow( wsz4, wiz )
    wszWin5 = sizeManager.makeScreenConfigForWindow( wsz5, wiz )

    bn = 'F:/_rtc/wizardry/wizards/rdlc-wizard/rdlc_img.png'

    print('Actuated 1: ', wszWin1.formatToString(), ' image candidates: ', sizeManager.generateImageHeightCandidates(wszWin1), ', best: ', sizeManager.findBestWizardImage(bn,wszWin1) )
    print('Actuated 2: ', wszWin2.formatToString(), ' image candidates: ', sizeManager.generateImageHeightCandidates(wszWin2), ', best: ', sizeManager.findBestWizardImage(bn,wszWin2) )
    print('Actuated 3: ', wszWin3.formatToString(), ' image candidates: ', sizeManager.generateImageHeightCandidates(wszWin3), ', best: ', sizeManager.findBestWizardImage(bn,wszWin3) )
    print('Actuated 4: ', wszWin4.formatToString(), ' image candidates: ', sizeManager.generateImageHeightCandidates(wszWin4), ', best: ', sizeManager.findBestWizardImage(bn,wszWin4) )
    print('Actuated 5: ', wszWin5.formatToString(), ' image candidates: ', sizeManager.generateImageHeightCandidates(wszWin5), ', best: ', sizeManager.findBestWizardImage(bn,wszWin5) )

    print('------------------------')
    sizeManager.findBestWizardImage( bn, wszWin4 )

    print('------------------------')

    # def mergeWizardScreenSize( self, wszMergeTo, wszMergeFrom ) :
    # formatToString
    # parseWizardRectString


    resolutionsCount = 0

    for r in resolutions :

        # https://docs.python.org/3/library/stdtypes.html#str.format
        # https://docs.python.org/3/library/string.html#formatstrings
        # Three conversion flags are currently supported: '!s' which calls str() on the value, '!r' which calls repr() and '!a' which calls ascii().
        s = str(r[0]).rjust(4,' ') + ' x ' + str(r[1]).rjust(4,' ') + ', ratio: ' + "{0:.1f}".format( r[0] / r[1] )
        print(s)

        resolutionsCount = resolutionsCount + 1


    print('-----')
    print('Total misc resolutions: ' , resolutionsCount )
    print('------------------------')

    
    heightsSet = {}
    
    totalSizesCount = 0
    
    for w in widths :
    
        #w11 = int(w/1.05)
        w11 = int(w*0.936)
    
        heighs = sizeManager.makeScreenHeightsForWidth( w11 )
    
        for h in heighs :
            rw = sizeManager.round10(w11)
            rh = sizeManager.round10(h)
            rh160 = rh - 160
            if rh160 < 0 :
                rh160 = 0
    
            #heightsSet[ int(rh) ] = rh160
            #heightsSet[ int(rh) ] = WizardPageSizeInfo( rh, rh160 )
    
            if int(rh) not in heightsSet:
                heightsSet[ int(rh) ] = WizardPageSizeInfo()
    
            heightsSet[ int(rh) ].width.append(rw)
            heightsSet[ int(rh) ].height    = rh
            heightsSet[ int(rh) ].imgHeight = rh160

            print( rw, ' x ', rh, '    (', w11, ' x ', h , '), required image size: ', rh160 ) #imgs
    
            totalSizesCount = totalSizesCount+1
    
    print('-----')
    print('Total misc sizes: ' , totalSizesCount)
    
    '''
    Sorting
    
    https://stackoverflow.com/questions/22264956/how-to-sort-dictionary-by-key-in-numerical-order-python
    
    for key, value in sorted(docs_info.items()): # Note the () after items!
        print(key, value)
    
    not  working
    int_docs_info = { int(k) : v for k, v in docss_info.items()}
    
    https://thispointer.com/python-how-to-sort-a-dictionary-by-key-or-value/
    
    '''
    
    heightsSetSorted = { int(k) : v for k, v in heightsSet.items() }
    
    print('------------------------')
    print('Page size ordered by value')
    print('--------')
    
    maxLen = 0
    
    for h, si in sorted(heightsSet.items()) :
        s = ''
        for w in si.width :
            if s=='' :
                s = str(w)
            else :
                s = s + '/' + str(w)
    
        l = len(s)
        if l > maxLen :
            maxLen = l
    
    
    # string methods - http://python-ds.com/python-3-string-methods
    # https://www.tutorialspoint.com/python3/string_len.htm
    
    prevImgHeight      = 0
    totalImgSizesCount = 0
    
    for h, si in sorted(heightsSet.items()) :
    
        s = ''
        for w in si.width :
            if s=='' :
                s = str(w)
            else :
                s = s + '/' + str(w)
    
        s = s.rjust( maxLen, ' ' )
        s = s + ' x ' + str(si.height).rjust( 4, ' ' ) + ', image size: ' + str(si.imgHeight).rjust( 4, ' ' )
    
        if prevImgHeight!=0 :
            s =  s + '  +' + str( si.imgHeight - prevImgHeight )
    
        print( s )
    
        prevImgHeight = si.imgHeight
    
        totalImgSizesCount = totalImgSizesCount+1
    
    
    print('-----')
    print('Total img sizes: ' , totalImgSizesCount)
    
   
