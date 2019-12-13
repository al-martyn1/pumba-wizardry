#!/usr/bin/python3

import os
import sys
import copy

# "Text files - *.txt; All files - *"
# "Text files - *.txt; C/C++ files - *.c *.cpp *.cxx *.c++; C/C++ header files - *.h *.hpp *.hxx *.h++; All files - *"
# "Text files - *.txt; Template files - *.tpl; All files - *"




#--------------------------------------------------
class FilenameFilter :

    def __init__(self,filterString):

        self.name      = str() # display name
        self.maskList  = []
        self.splitFilter(filterString)



    def print( self ) :
        print(self.name)
        print(self.maskList)



    def splitFilter( self, filterString ) :

        nameMasks = str(filterString).split('-')

        if len(nameMasks)!=2 :
            raise ValueError('FilenameFilter invalid: ' + str(filterString))

        self.name  = nameMasks[0].strip(' ')
        filtersStr = nameMasks[1].strip(' ')

        #self.maskList = filtersStr.split(' ')

        tmpList = filtersStr.split(' ')
        self.maskList = []
        for t in tmpList :
            t = t.strip(' ') # also known as trim
            if len(t)==0 :
                continue
            #if t[0]!='.' and t!='*' :
            #    t = '.' + t
            self.maskList.append(t)

        if len(self.maskList)==0 :
            raise ValueError('FilenameFilter invalid - no masks taken: ' + str(filterString))

        pass



    def buildQtFilter( self ) :

        qFltStr = self.name + ' ('

        for mask in self.maskList :
            qFltStr = qFltStr + mask + ' '

        return qFltStr.strip(' ') + ')'




#--------------------------------------------------
class FilenameFilterSet :

    def __init__(self, filtersString):

        self.filters       = []
        self.filtersLookup = {}

        self.splitFilterString(filtersString)



    def splitFilterString( self, filtersString ) :

        filtersList = str(filtersString).split(';')

        for filterStr in filtersList :

            flt = FilenameFilter(filterStr)

            idx = len(self.filters)

            for mask in flt.maskList :
                maskLower = mask.lower()
                self.filtersLookup[maskLower] = idx

            self.filters.append(flt)



    def findFilter( self, ext ) :

        #if ext[0]!='.' :
        #    ext = '.' + ext

        ext = '*' + ext.lower()

        if ext in self.filtersLookup :
            return self.filters[self.filtersLookup[ext]]

        if '*' in self.filtersLookup :
            return self.filters[self.filtersLookup['*']]

        return None



    def findFilterByFilename( self, fname ) :
        pe = os.path.splitext(fname)
        if len(pe)<2 :
            return self.findFilter( '*' )
        return self.findFilter( pe[1] )



    def buildQtFilters( self ) :

        res = [] # str()

        for flt in self.filters :
            res.append(flt.buildQtFilter())

        return res




#--------------------------------------------------
if __name__ == '__main__':
    
    #flt = FilenameFilter()
    #flt.splitFilter('C/C++ header files - *.h    *.hpp       *.hxx *.h++')
    #flt.print()

    filterSet = FilenameFilterSet('Text files - *.txt; C/C++ files - *.c *.cpp *.cxx *.c++; C/C++ header files - *.h *.hpp *.hxx *.h++; All files - *')

    qtFilters = filterSet.buildQtFilters()
    print(qtFilters)

    print('Find \'.cxx\': ', filterSet.findFilter( '.cxx' ).buildQtFilter() )
    print('Find \'header.hpp\': ', filterSet.findFilterByFilename( 'header.hpp' ).buildQtFilter() )

    

    #for qFlt in qtFilters :
    #    print(qFlt)

    #print( filterSet.buildQtFilters() )

    #print(filterSet)
