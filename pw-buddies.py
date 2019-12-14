#!/usr/bin/python3

import os
import sys
import copy

# "*-buddies":"+.user,.user",


#--------------------------------------------------
def generateBuddies( fileName, buddiesListStr ) :

    buddiesList = []
    buddiesList.append(fileName)

    if buddiesListStr==None or buddiesListStr=='' :
        return buddiesList


    resNames = fileName
    pe = os.path.splitext(fileName)
    fileNameNoExt = pe[0]

    buddiesExtList = buddiesListStr.split(',')

    for buddyExt in buddiesExtList :

        buddyExt = buddyExt.strip(' ')
        if len(buddyExt)==0 :
            continue

        appendMode = False

        if buddyExt[0]=='+' :
            appendMode = True
            buddyExt = buddyExt[1:]
        
        if len(buddyExt)==0 :
            continue

        if buddyExt[0]!='.' :
            buddyExt = '.' + buddyExt

        if appendMode==True :
            buddiesList.append( fileName + buddyExt )
        else : # replace mode
            buddiesList.append( fileNameNoExt + buddyExt )

    return buddiesList



#--------------------------------------------------
if __name__ == '__main__':
    
    print('Buddies: ', generateBuddies( '.\some-file.vc', '+.app,.rep') )

