#!/usr/bin/env python

##Copyright (C) 2010 Louis Taylor                                         
##This program is free software: you can redistribute it and/or modify         
##it under the terms of the GNU General Public License as published by         
##the Free Software Foundation, either version 3 of the License, or            
##(at your option) any later version.                                          
##                                                                             
##This program is distributed in the hope that it will be useful,              
##but WITHOUT ANY WARRANTY; without even the implied warranty of               
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
##GNU General Public License for more details.                                 
##                                                                            
##You should have received a copy of the GNU General Public License            
##along with this program.  If not, see http://www.gnu.org/licenses/gpl-3.0.txt  

import os, subprocess, time

def compile(latexfile, pdfdir='/tmp', rmlog=False, movepdf=False, usebibtex=False, latextype='xelatex'):
    '''compiles latex document, saves it to the directory
    specified in *pdfdir* and returns any error messages it can find'''
    path = os.path.split(os.path.abspath(latexfile))
    texfile = path[1]
    directory = path[0]
    
    rawname = os.path.splitext(texfile)[0]
    
    logfile = os.path.splitext(texfile)[0]+'.log'
    logpath = os.path.join(pdfdir, logfile)
    
    pdffile = os.path.splitext(texfile)[0]+'.pdf'
    pdfpath = os.path.join(pdfdir, pdffile)
    
    os.chdir(directory) #change cwd to the dir to place all latex files
    
    #os.system('bibtex %s' % rawname) #this will be replaced by the new function
    bibtex_error = False
    if usebibtex == True:
        bib_err = bibtex(rawname, pdfdir)
        if bib_err != '':
            #get an error message
            bibtex_error = ['error', 'BibTeX error', '', bib_err]
    
           #using xelatex by default, because I prefer XeTeX now :p
           #TODO: Add an option to change between xelatex, pdflatex and latex.
    cmd = [latextype, '--halt-on-error', '-output-directory', pdfdir, texfile]
    latex = subprocess.Popen(cmd, shell=False,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    message = latex.communicate()[0] #get the stdout, latex.communicate()[1] gives stderr
    #set the data to be returned on success
    returned = ['success', pdfpath]

    if '\n!' in message:
        name = False
        ln = False
        error_msg = ''
        error_ln = ''
        quote = ''
        
        for line in message.split('\n'):
            if line == '':
                pass #pass if the line is blank
            
            elif line[0] == '!' and not name:
                #find error message line
                name = True
                error_msg = line.replace('!', '').strip()
                                        #remove all whitespace around string
                
            elif line[0] == 'l' and name and not ln:
                #find line number and quote.
                #only come to this line if:
                #the-- first character is an 'l', there has just been an error
                #line and there has not been a line number before.
                ln = True
                string = line.split(' ')
                error_ln = string[0].replace('l.', '')
                quote = line.replace(string[0], '')
                
            else:
                pass
    
    #repeat the BibTeX command, as requested by Peter Flynn
    if usebibtex == True:
        bib_err = bibtex(rawname, pdfdir)
        if bib_err != '':
            #get an error message
            bibtex_error = ['error', 'BibTeX error', '', bib_err]
        else:
            pass
        
    else:        
        #set the data to be returned on error
        try:
            returned = ['error', error_msg, error_ln, quote, pdffile]
        except UnboundLocalError:
            returned = ['success', pdfpath]
        
    if rmlog:
        try:
            os.remove(logpath)
        except OSError:
            pass
        
    if movepdf:
        #bit of a quick hack, use cp to do the work:
            #use python to do this?
        os.system('cp "%s" "%s"' % (pdfpath, movepdf))

    if returned == ['success', pdfpath] and bibtex_error == False:
        '''return normal traceback if everything went ok'''
        return returned
    if returned != ['success', pdfpath] and bibtex_error == False:
        '''return latex error message'''
        return returned
    if returned == ['success', pdfpath] and bibtex_error != False:
        '''return bibtex error'''
        return bibtex_error
    if returned != ['success', pdfpath] and bibtex_error != False:
        '''let the latex error have preference over bibtex error'''
        return returned
        
def bibtex(rawtexname, directory):
    #os.chdir(directory)
    
    cmd = ['bibtex', rawtexname]
    bibtex = subprocess.Popen(cmd, shell=False,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    message = bibtex.communicate()[0] #get the stdout, bibtex.communicate()[1] gives stderr
    print message
    
    error = ''
    for line in message.split('\n'):
        if error != '':
            #if we already have the first bibtex error message
            break
        else:
            #if we do not have an error message yet
            words = line.split()
            if line == '':
                break
            elif line[0] == 'I':
                #if line is one of the variations on "I couldn't..."
                if words[1] == 'found':
                    error = line.replace('I', '').replace('---', ' ').strip()
                elif words[1] == "couldn't":
                    error = line.replace('I', '').strip()
                    
            elif 'Warning--' in line:
                error = line.replace('Warning--I ', '')
    return error
    
if __name__ == '__main__':
    #small self test
    error = compile('/home/louis/Desktop/tex/text.tex', '/home/louis/Desktop/tex', True, movepdf=False, usebibtex=True)
    print error
    
    
