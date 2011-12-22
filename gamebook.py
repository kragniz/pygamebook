#!/usr/bin/env python
import re, sys, os, latex
from random import choice
import random
class pygamebook(object):
    def __init__(self):
        self.storyFileName = ''
        self.texFileName = 'output.tex'
        self.storyFileContents = ''
        self.codeBlocks = []
        self.dataBlocks = [] #these are used to store information such as title
                             #and name of author
        self.latexFilename = ''
        
        self.mainData = {}
        self.extraData = {}
        
        self.author = ''
        self.title = ''
        
        self.skills = ['skl', 'sta']
        
        self.LATEX_HEADER = ''
        self.LATEX_PARAGRAPH = ''
        self.LATEX_OPTION = ''
        self.LATEX_GOTO = ''
        self.LATEX_FOOTER = ''
        
        self.numberOfBrokenLinks = 0
        self.numberOfEnemies = 0
        
    def __str__(self):
        '''returns the string representation of the
        data stored in an instance of the class'''
        value = ''
        for block in self.mainData:
            value += block
            value += ' - ' + str(self.mainData[block]['paragraphNumber']) + '\n'
        return value
    
    def make(self):
        self.loadStoryFile()
        self.separateCodeBlocks()
        self.parseCodeBlocks()
        self.parseDataBlocks()
        self.savePdfFile()
        
    def setStoryFile(self, storyFileName):
        '''sets the file to read instructions on
        writing the gamebook'''
        self.storyFileName = storyFileName
        
    def setLatexSource(self, filename):
        '''sets the source for the parts of LaTeX
        code. This means the user can change the basic
        style of the gamebook. Take a look at the example
        which should be in the same directory as this file'''
        self.latexsource = filename
        
    def importLatexSource(self):
        '''Does the importing and saving of the data stored
        within the user defined python module containing bits
        of LaTeX code'''
        #importString = "from %s import HEADER, PARAGRAPH, OPTION, GOTO, FOOTER, SINGLE_ENEMY" % self.latexsource
        importString = "from %s import *" % self.latexsource
        exec importString
        self.LATEX_HEADER = HEADER
        self.LATEX_PARAGRAPH = PARAGRAPH
        self.LATEX_OPTION = OPTION
        self.LATEX_GOTO = GOTO
        self.LATEX_FOOTER = FOOTER
        self.LATEX_BACKGROUND = BACKGROUND
        
        self.LATEX_SINGLE_ENEMY = SINGLE_ENEMY
        self.LATEX_ENEMY_WIN = ENEMY_WIN
        self.LATEX_ENEMY_LOSE = ENEMY_LOSE
        self.LATEX_MULTIPLE_ENEMY_HEADER = MULTIPLE_ENEMY_HEADER
        self.LATEX_MULTIPLE_ENEMY_NAME_AND_STATS = MULTIPLE_ENEMY_NAME_AND_STATS
        self.LATEX_MULTIPLE_ENEMY_FOOTER = MULTIPLE_ENEMY_FOOTER
        
    def createEnemyTable(self, paragraph):
        '''Creates and returns a sort of alright
        LaTeX table of the name and stats of one or
        more enemies'''
        self.numberOfEnemies += len(paragraph['enemy'])
        if len(paragraph['enemy']) > 1:
            enemyStr = self.LATEX_MULTIPLE_ENEMY_HEADER
            for i in range(len(paragraph['enemy'])):
                enemyStr += self.LATEX_MULTIPLE_ENEMY_NAME_AND_STATS % (
                                                      paragraph['enemy'][i]['name'].upper(),
                                                      paragraph['enemy'][i]['stats'][self.skills[0]],
                                                      paragraph['enemy'][i]['stats'][self.skills[1]])
            enemyStr += self.LATEX_MULTIPLE_ENEMY_FOOTER
        else:
            enemyStr = self.LATEX_SINGLE_ENEMY % (paragraph['enemy'][0]['name'].upper(),
                                                  paragraph['enemy'][0]['stats'][self.skills[0]],
                                                  paragraph['enemy'][0]['stats'][self.skills[1]])
        return enemyStr
        
    def createParagraph(self, paragraph):
        '''Does the brunt of creating a chunk of LaTeX code
        for one paragraph. Returns a string.'''
        paragraphStr = paragraph['text']
        if paragraph['options']:
            for option in paragraph['options']:
                try:
                    optionStr = self.LATEX_OPTION % (option[0],
                                self.mainData[option[1]]['paragraphNumber'])
                    paragraphStr += optionStr
                except KeyError:
                    print 'Warning! The paragraph "%s" was not found!' % option[1]
                    self.numberOfBrokenLinks += 1
                    paragraphStr += self.LATEX_OPTION % (option[0], '??')
        elif paragraph['goto'] != None:
            try:
                paragraphStr += self.LATEX_GOTO % self.mainData[paragraph['goto']]['paragraphNumber']
            except KeyError:
                print 'Warning! The paragraph "%s" was not found!' % paragraph['goto']
                self.numberOfBrokenLinks += 1
        if len(paragraph['enemy']) > 0:
            enemyStr = self.createEnemyTable(paragraph)
            paragraphStr += enemyStr
            if paragraph['enemy'][0]['winCase'] != None:
                winParagraph = paragraph['enemy'][0]['winCase'] 
                try:
                    winStr = self.LATEX_ENEMY_WIN % (self.mainData[winParagraph]['paragraphNumber'])
                    paragraphStr += winStr
                except KeyError:
                    print 'Warning! The paragraph "%s" was not found!' % winParagraph
                    self.numberOfBrokenLinks += 1
                    paragraphStr += self.LATEX_ENEMY_WIN % '??'
                    
                if paragraph['enemy'][0]['loseCase'] != None:
                    loseParagraph = paragraph['enemy'][0]['loseCase'] 
                    try:
                        loseStr = self.LATEX_ENEMY_LOSE % (self.mainData[loseParagraph]['paragraphNumber'])
                        paragraphStr += loseStr
                    except KeyError:
                        print 'Warning! The paragraph "%s" was not found!' % loseParagraph
                        self.numberOfBrokenLinks += 1
                        paragraphStr += self.LATEX_ENEMY_LOSE % '??'
                else:
                    paragraphStr += '.' #finish the winning case.
            
        return self.LATEX_PARAGRAPH % paragraphStr
    
    def generateTex(self):
        '''generate the entire LaTeX document.
        Returns a string'''
        latexOut = ''        
        self.importLatexSource()
        latexOut += self.LATEX_HEADER % (self.extraData['author'], self.extraData['title'].title())
        if self.extraData['background'] != None:
            latexOut += self.LATEX_BACKGROUND % self.extraData['background']
        
        i = 1
        j = 0
        paragraphs = [s for s in self.mainData]
        
        while paragraphs:
            if self.mainData[paragraphs[j]]['paragraphNumber'] == i:
                latexOut += self.createParagraph(self.mainData[paragraphs[j]])
                paragraphs.pop(j)
                i += 1
                j = 0
            else:
                j += 1
            
        latexOut += self.LATEX_FOOTER
        return latexOut
    
    def saveTexFile(self, texFileName=None):
        '''Saves the LaTeX file to disk.'''
        if texFileName == None:
            texFileName = self.texFileName
        texFile = open(texFileName, 'w')
        texFile.write(self.generateTex())
        texFile.close()
        
    def savePdfFile(self):
        self.saveTexFile()
        texDirectory = os.path.split(os.path.abspath(self.texFileName))[0]
        errors = latex.compile(self.texFileName, pdfdir=texDirectory)
        if errors[0] != 'success':
            print errors
        
    def loadStoryFile(self):
        '''Load the users .story document'''
        storyFile = open(self.storyFileName, 'r')
        self.storyFileContents = storyFile.read()
        storyFile.close()
        
    def separateCodeBlocks(self):
        '''Divide the .story document into usable chunks'''
        matches = re.findall('\<.*?\>', self.storyFileContents, re.DOTALL)
        self.codeBlocks = []
        for codeBlock in matches:
            refinedBlock = codeBlock[1:-1].strip()
            if (refinedBlock.split()[0] == 'data') or (refinedBlock.split()[0] == 'background'):
                self.dataBlocks += [refinedBlock]
            else:
                self.codeBlocks += [refinedBlock] #remove the first and the last character
    
    def error(self, line=None):
        '''Error handling. Not very nicly done, but I rather
        fancied creating my own class inherited from Exception'''
        if line == None:
            raise parsingError('An error has occured')
        else:
            raise parsingError('An error has occured parsing this line:\n'+line)
        
    def parseDataBlocks(self):
        self.extraData['background'] = None
        self.extraData['title'] = None
        self.extraData['author'] = None
        for block in self.dataBlocks:
            blockLines = block.split('\n')
            
            if blockLines[0].lower() == 'background':
                self.extraData['background'] = blockLines[1:][0]
            elif blockLines[0].lower() == 'data':
                for line in blockLines[1:]: #ignore the first line
                    if len(line) > 0:
                        words = line.split()
                        if words[0][0] == '*':
                            if words[0][1:] == 'author':
                                self.extraData['author'] = r' '.join(words[1:])
                            elif words[0][1:] == 'title':
                                self.extraData['title'] = r' '.join(words[1:])
                
    def parseCodeBlocks(self):
        '''Does all the work to process the document. Parses
        the document and stores all of the data in self.mainData.
        There are far too many regular expressions'''
        self.mainData = {}
        numberOfBlocks = len(self.codeBlocks)
        #build a list of all the paragraph numbers
        numberList = [i+1 for i in range(numberOfBlocks)]
            
        for block in self.codeBlocks:
            blockLines = block.split('\n')
            blockData = {}
            
            blockData['text'] = ''
            blockData['options'] = []
            blockData['goto'] = None
            blockData['enemy'] = []
            
            if blockLines[0].lower() == 'start':
                blockData['paragraphNumber'] = 1
            else:
                blockData['paragraphNumber'] =  choice(numberList)    
            numberList.remove(blockData['paragraphNumber'])
            
            for line in blockLines[1:]: #ignore the first line
                if len(line) > 0:
                    words = line.split()
                    if words[0][0] == '*':
                        if words[0][1:] == 'goto':
                            match = re.search('(?<=goto).*?\[.*?\]', line)
                            blockData['goto'] = match.group(0).strip()[1:-1]
                        elif words[0][1:] == 'option':
                            try:
                                descriptionMatch = re.search('(?<=option).*?\[', line)
                                description = descriptionMatch.group(0).strip()[:-1].strip()
                            except AttributeError:
                                self.error(line)
                            try:
                                paragraphMatch = re.search('\[.*?\]', line)
                                paragraph = paragraphMatch.group(0)[1:-1]
                            except AttributeError:
                                self.error(line)
                            option = [description, paragraph]
                            blockData['options'] += [option]
                        elif words[0][1:] == 'enemy':
                            nameMatch = re.search('(?<=enemy).*?\[', line)
                            name = nameMatch.group(0)[1:-1].strip()
                            
                            try:
                                '''Crazy variable regex'''
                                variablePartOfStatRegex = '(%s|%s)' % (self.skills[0], 
                                                                       self.skills[1])
                                statRegex = '\[xx\s*-?\d+\s*xx\s*-?\d+\]'.replace('xx', variablePartOfStatRegex)
                                statMatch = re.search(statRegex, line)
                                #statMatch = re.search('\[[a-z 0-9]+?\]', line) #This is the old one, a bit simpler :P
                                statsList = statMatch.group(0)[1:-1].split()
                                stats = {}
                            except AttributeError:
                                self.error('Could not find the stats of %s, are you sure you typed them correctly?' % name)
                            
                            for skill in self.skills:
                                stats[skill] = statsList[statsList.index(skill)+1]
                            
                            winCaseMatch = re.search('(?<=win ).*?\[.+?\]', line)
                            if winCaseMatch is not None:
                                winCase = winCaseMatch.group(0).strip()[1:-1].strip()
                            else:
                                winCase = None
                                
                            loseCaseMatch = re.search('(?<=lose ).*?\[.+?\]', line)
                            if loseCaseMatch is not None:
                                loseCase = loseCaseMatch.group(0).strip()[1:-1].strip()
                            else:
                                loseCase = None
                                
                            #save all the data about the enemy in another dictionary
                            blockData['enemy'] += [{'name':name,
                                                'stats':stats, 
                                                'winCase':winCase,
                                                'loseCase':loseCase}]
                    elif line[0] == '#':
                        pass #it's a comment. Yes, you can have them in a .story
                    else:
                        blockData['text'] += line + '\n' #add newline to be on the safe side
            #Save all this data in the main dictionary. You the paragaph name as the key
            self.mainData[blockLines[0]] = blockData 

            
class parsingError(Exception):
    def __init__(self, message):
        '''Do some funky exceptions'''
        self.message = message
    def __str__(self):
        return self.message
    

if __name__ == '__main__':
    book = pygamebook()
    arguments = sys.argv
    if len(arguments) > 1:
        book.setLatexSource('example_latex')
        if os.path.isfile(arguments[1]):
            book.setStoryFile(arguments[1])
            book.make()
        else:
            print '''the file '%s' could not be found''' % arguments[1]
    else:
        print '''
Usage:
    %s [story file] [tex/pdf filename = output]
''' % os.path.split(arguments[0])[1]
