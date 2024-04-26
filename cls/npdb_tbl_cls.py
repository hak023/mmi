import sys
import time
import datetime
import commands
import pexpect

from mmi.cmd import *
from mmi.conf import *

SECTION_MAIN = 'MAIN'
SECTION_NPDB = 'NPDB_'

FILIED_NPDB_CNT = 'NPDB_NUM'

FILIED_NAME = 'NAME'
FILIED_PFX = 'PFX'
FILIED_DOM = 'DOMAIN'
FILIED_OP = 'OP'
     
class NpdbTblCommand(MMICommand):
    
    def __init__(self, type):
        self.exception = None
        self.config = MMIConfig()
        self.cmdconf = CmdConfig()
        
        self.isIdxSearch = -1
        self.type = type

        self.getCnt = ''
        self.getName = ''
        self.getPfx = ''
        self.getDom = ''
        self.getOp = ''

        self.delchgIndex = -1

        self.setCnt = ''
        self.setName = ''
        self.setPfx = ''
        self.setDom = ''
        self.setOp = ''
  
        self.filepath = '../config/env/npdb_table.cfg'

    def printInputMessage(self):
        print ""
        if self.delchgIndex != -1:
            print "\t" "%12s = %d" % ('INDEX', int(self.delchgIndex)+1)
        if self.setName != '':
            print "\t" "%12s = %s" % ('NAME', self.setName)
        if self.setPfx != '':
            print "\t" "%12s = %s" % ('RN', self.setPfx)
        if self.setDom != '':
            print "\t" "%12s = %s" % ('DOMAIN', self.setDom)
        if self.setOp != '':
            print "\t" "%12s = %s" % ('OP', self.setOp)

    def printMessage(self):
        self.printHeader()
        print "[INPUT]"
        print "%-10s : %s" % ('COMMAND', self.getCommandName())
        print ""
        print "%-12s %s" % ('', self.getCommandDesc())
        print ""        
        try:
            self.printInputMessage()
        except Exception:
            print "%-10s : %s" % ('ARGS', repr(sys.argv[1:]))
            
        print ""
        print "[OUTPUT]"
        print ""
        if(self.exception is None) :

            try:
                cfg = ConfigParser()
                cfg.optionxform = str
                cfg.read(self.filepath)
                
                if self.type == "DIS":
                    if self.isIdxSearch <= 0:
                        self.printAllSection(cfg)
                    else:
                        strSection = SECTION_NPDB
                        strSection = strSection + str(self.isIdxSearch-1)
                        self.printSection(cfg, self.isIdxSearch, strSection, self.isIdxSearch)
                elif self.type == "CRTE":
                    self.insertSection(cfg)
                elif self.type == "CHG":
                    if(self.checkIndex(cfg)):
                        self.changeSection(cfg)      
                elif self.type == "DEL":
                    if(self.checkIndex(cfg)):
                        self.deleteSection(cfg)

                print "%-10s = %s" % ('RESULT', 'OK')
                self.printTail()
                
            except Exception:
                print "%-10s = %s" % ('RESULT', 'NOK')
                print "%-10s = %s" % ('REASON', self.exception)
                self.printTail()
            
        else :
            print "%-10s = %s" % ('RESULT', 'NOK')
            print "%-10s = %s" % ('REASON', self.exception)
            self.printTail()
    
    def setCurCount(self, cfg, newCnt):
        cfg.set(SECTION_MAIN, FILIED_NPDB_CNT, str(newCnt))
        with open(self.filepath, 'wb') as configfile:
            cfg.write(configfile)
    
    def getCurCount(self, cfg):
        if cfg.has_option(SECTION_MAIN, FILIED_NPDB_CNT) == True:
            self.getCnt = cfg.get(SECTION_MAIN, FILIED_NPDB_CNT)
        
        nCount = int(self.getCnt)
        return nCount 
    
    def checkIndex(self, cfg):
        nCount = self.getCurCount(cfg)

        if self.delchgIndex >= nCount:
           self.exception = "INDEX ERROR"
           raise Exception
        else:
            return True
    
    def printTitle(self):
        print "\t", "%5s %15s %20s %15s %10s" % ('INDEX', 'NAME', 'RN', 'DOMAIN', 'OP')
        print "\t", " --------------------------------------------------------------------"
            
    def printAllSection(self, cfg):
        if cfg.has_option(SECTION_MAIN, FILIED_NPDB_CNT) == True:
            self.getCnt = cfg.get(SECTION_MAIN, FILIED_NPDB_CNT)
        else:    
           self.exception = "NPDB_NUM KEY NOT FOUND"
           raise Exception
        
        nCount = int(self.getCnt)

        self.printTitle()

        for i in range(0, nCount):
           strSection = SECTION_NPDB
           strSection = strSection + str(i)
           self.printSection(cfg, i, strSection, 0)

        print ""   
        print "%-10s = %d" % ('TBL_CNT', nCount)
        print ""
    
    def printSection(self, cfg, index, sectionName, type):
        strSection = sectionName

        if cfg.has_option(strSection, FILIED_NAME) == True:
            self.getName = cfg.get(strSection, FILIED_NAME)
        else:
            self.exception = "INDEX NOT FOUND"
            raise Exception   
              
        if cfg.has_option(strSection, FILIED_PFX) == True:
            self.getPfx = cfg.get(strSection, FILIED_PFX)
            
        if cfg.has_option(strSection, FILIED_DOM) == True:
            self.getDom = cfg.get(strSection, FILIED_DOM)            

        if cfg.has_option(strSection, FILIED_OP) == True:
            self.getOp = cfg.get(strSection, FILIED_OP)
        
        if type == 0:  
            print "\t", "%5d %15s %20s %15s %10s" % (index+1, self.reprNameShorter(self.getName, 15, 11), 
                                                    self.reprNameShorter(self.getPfx, 20, 16), 
                                                    self.reprNameShorter(self.getDom, 15, 11),
                                                    self.reprNameShorter(self.getOp, 10, 6)
                                                    )
        else:
            print "\t" "%12s = %s" % ('NAME', self.getName)
            print "\t" "%12s = %s" % ('RN', self.getPfx)
            print "\t" "%12s = %s" % ('DOMAIN', self.getDom)
            print "\t" "%12s = %s" % ('OP', self.getOp)
            print ""

    def insertSection(self, cfg):
        index = self.getCurCount(cfg)
        NEW_SECTION = SECTION_NPDB + str(index)
        
        cfg.add_section(NEW_SECTION)
        cfg.set(NEW_SECTION, FILIED_NAME, str(self.setName))
        cfg.set(NEW_SECTION, FILIED_PFX, str(self.setPfx))
        cfg.set(NEW_SECTION, FILIED_DOM, str(self.setDom))
        cfg.set(NEW_SECTION, FILIED_OP, str(self.setOp))
        
        with open(self.filepath, 'ab') as configfile:
            cfg.write(configfile)
        
        self.printTitle()
        self.printSection(cfg, index, NEW_SECTION, 0)
        print ""
        self.setCurCount(cfg, index+1)
        
    def changeSection(self, cfg):
        CHG_SECTION = SECTION_NPDB + str(self.delchgIndex)

        if self.setName != '':
           cfg.set(CHG_SECTION, FILIED_NAME, str(self.setName))
        if self.setPfx != '':
           cfg.set(CHG_SECTION, FILIED_PFX, str(self.setPfx))
        if self.setDom != '':
           cfg.set(CHG_SECTION, FILIED_DOM, str(self.setDom))           
        if self.setOp != '':
           cfg.set(CHG_SECTION, FILIED_OP, str(self.setOp))
      
        with open(self.filepath, 'wb') as configfile:
           cfg.write(configfile)
           
        self.printTitle()
        self.printSection(cfg, self.delchgIndex, CHG_SECTION, 0)
        print ""
        
    def deleteSection(self, cfg):
        curCnt = self.getCurCount(cfg)
        DEL_SECTION = SECTION_NPDB + str(self.delchgIndex)
        
        cfg.remove_section(DEL_SECTION)
        
        with open(self.filepath, 'wb') as configfile:
            cfg.write(configfile)
        
        self.relocateSection(cfg, self.delchgIndex, curCnt)
            
        self.setCurCount(cfg, curCnt-1)
        
    def relocateSection(self, cfg, startIndex, curCnt):
        for index in range(startIndex, curCnt):
            ORG_SECTION = SECTION_NPDB + str(index)
            TEMP_SECTION = SECTION_NPDB + str(index+1)
           
            if cfg.has_option(TEMP_SECTION, FILIED_NAME) == True:
                name = cfg.get(TEMP_SECTION, FILIED_NAME)
                pfx = cfg.get(TEMP_SECTION, FILIED_PFX)
                dom = cfg.get(TEMP_SECTION, FILIED_DOM)
                op = cfg.get(TEMP_SECTION, FILIED_OP)

                cfg.remove_section(TEMP_SECTION)

                cfg.add_section(ORG_SECTION)
                cfg.set(ORG_SECTION, FILIED_NAME, str(name))
                cfg.set(ORG_SECTION, FILIED_PFX, str(pfx))
                cfg.set(ORG_SECTION, FILIED_DOM, str(dom))
                cfg.set(ORG_SECTION, FILIED_OP, str(op))

        with open(self.filepath, 'wb') as configfile:
            cfg.write(configfile)

    def reprNameShorter(self, name, chklen, cutlen):
        if len(name) > int(chklen):
            value = name[0:int(cutlen)]
            value = value + " ..."
        else:
            value = name
        return value

    def printExcecption(self, e):
        if type(e) is MMICommandParamException:
            self.printUsage()
        else :
            self.exception = e
            self.printMessage()
    
    def execute(self):
       self.printMessage()
