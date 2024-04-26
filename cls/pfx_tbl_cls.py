import sys
import time
import datetime
import commands
import pexpect

from mmi.cmd import *
from mmi.conf import *

SECTION_MAIN = 'MAIN'
SECTION_PFX = 'PFX_'

FILIED_PFX_CNT = 'PFX_NUM'

FILIED_NAME = 'NAME'
FILIED_PFX = 'PFX'
FILIED_CODETYPE = 'CODETYPE'
FILIED_TEL_IOR_OPT = 'TEL_IOR_OPT'
FILIED_MIN = 'MIN'
FILIED_MAX = 'MAX'
FILIED_OVRT_OPT = 'OVRT_OPT'
FILIED_DOM = 'DOMAIN'
FILIED_OP = 'OP'
     
class PfxTblCommand(MMICommand):
    
    def __init__(self, type):
        self.exception = None
        self.config = MMIConfig()
        self.cmdconf = CmdConfig()
        
        self.isIdxSearch = -1
        self.type = type

        self.getCnt = ''

        self.getName = ''
        self.getPfx = ''
        self.getCodeType = ''
        self.getTelIorOpt = ''
        self.getMin = ''
        self.getMax = ''
        self.getOvrtOpt = ''
        self.getDom = ''
        self.getOp = ''

        self.delchgIndex = -1

        self.setCnt = ''

        self.setName = ''
        self.setPfx = ''
        self.setCodeType = ''
        self.setTelIorOpt = ''
        self.setMin = ''
        self.setMax = ''
        self.setOvrtOpt = ''
        self.setDom = ''
        self.setOp = ''
  
        self.filepath = '../config/env/pfx_table.cfg'

    def printInputMessage(self):
        print ""
        if self.delchgIndex != -1:
            print "\t" "%12s = %d" % ('INDEX', int(self.delchgIndex)+1)
        if self.setName != '':
            print "\t" "%12s = %s" % ('NAME', self.setName)
        if self.setPfx != '':
            print "\t" "%12s = %s" % ('PFX', self.setPfx)
        if self.setCodeType != '':
            print "\t" "%12s = %s" % ('CODETYPE', self.setCodeType)
        if self.setTelIorOpt != '':
            print "\t" "%12s = %s" % ('TEL_IOR_OPT', self.setTelIorOpt)
        if self.setMin != '':
            print "\t" "%12s = %s" % ('MIN', self.setMin)
        if self.setMax != '':
            print "\t" "%12s = %s" % ('MAX', self.setMax)
        if self.setOvrtOpt != '':
            print "\t" "%12s = %s" % ('OVRT_OPT', self.setOvrtOpt)
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
                        strSection = SECTION_PFX
                        strSection = strSection + str(self.isIdxSearch-1)
                        self.printSection(cfg, self.isIdxSearch, strSection, self.isIdxSearch)
                elif self.type == "CRTE":
                    self.insertSection(cfg)
                elif self.type == "CHG":
                    if(self.checkIndex(cfg)):
                        self.checkTelIorOptType(cfg)
                        self.checkCodeType(cfg)
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
        cfg.set(SECTION_MAIN, FILIED_PFX_CNT, str(newCnt))
        with open(self.filepath, 'wb') as configfile:
            cfg.write(configfile)
    
    def getCurCount(self, cfg):
        if cfg.has_option(SECTION_MAIN, FILIED_PFX_CNT) == True:
            self.getCnt = cfg.get(SECTION_MAIN, FILIED_PFX_CNT)
        
        nCount = int(self.getCnt)
        return nCount 
    
    def checkIndex(self, cfg):
        nCount = self.getCurCount(cfg)

        if self.delchgIndex >= nCount:
           self.exception = "INDEX ERROR"
           raise Exception
        else:
            return True
    
    def checkCodeType(self, cfg):
        if not (str(self.setCodeType) and str(self.setTelIorOpt)):
            ORG_SECTION = SECTION_PFX + str(self.delchgIndex)
            if cfg.has_option(ORG_SECTION, FILIED_NAME) == True:
                org_tel_ior_opt = cfg.get(ORG_SECTION, FILIED_TEL_IOR_OPT)
                if org_tel_ior_opt != 'NONE':
                    if str(self.setCodeType):
                        if self.setCodeType != 'NPDB':
                            self.exception = '"' + self.setCodeType + '"' + ' CODETYPE is not Allow ' + '"' + org_tel_ior_opt + '"' + ' TEL_IOR_OPT (C)'
                            raise Exception                       
        
    def checkTelIorOptType(self, cfg):
        if not (str(self.setCodeType) and str(self.setTelIorOpt)):
            ORG_SECTION = SECTION_PFX + str(self.delchgIndex)
            if cfg.has_option(ORG_SECTION, FILIED_NAME) == True:
                org_codec = cfg.get(ORG_SECTION, FILIED_CODETYPE)
                if org_codec != 'NPDB':
                    if str(self.setTelIorOpt):
                        if self.setTelIorOpt != 'NONE':
                           self.exception = '"' + org_codec + '"' + ' CODETYPE is not Allow ' + '"' + self.setTelIorOpt + '"' + ' TEL_IOR_OPT (D)'
                           raise Exception
    
    def printTitle(self):
        print "\t", "%5s %10s %15s %13s %12s %7s %7s %9s %15s %10s" % ('INDEX', 'NAME', 'PFX', 'CODETYPE', 'TEL_IOR_OPT', 'MIN', 'MAX', 'OVRT_OPT', 'DOMAIN', 'OP')
        print "\t", " ---------------------------------------------------------------------------------------------------------------"
            
    def printAllSection(self, cfg):
        if cfg.has_option(SECTION_MAIN, FILIED_PFX_CNT) == True:
            self.getCnt = cfg.get(SECTION_MAIN, FILIED_PFX_CNT)
        else:
           self.exception = "PFX_NUM KEY NOT FOUND"
           raise Exception  
        
        nCount = int(self.getCnt)

        self.printTitle()

        for i in range(0, nCount):
           strSection = SECTION_PFX
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

        if cfg.has_option(strSection, FILIED_CODETYPE) == True:
            self.getCodeType = cfg.get(strSection, FILIED_CODETYPE)

        if cfg.has_option(strSection, FILIED_TEL_IOR_OPT) == True:
            self.getTelIorOpt = cfg.get(strSection, FILIED_TEL_IOR_OPT)

        if cfg.has_option(strSection, FILIED_MIN) == True:
            self.getMin = cfg.get(strSection, FILIED_MIN)

        if cfg.has_option(strSection, FILIED_MAX) == True:
            self.getMax = cfg.get(strSection, FILIED_MAX)

        if cfg.has_option(strSection, FILIED_OVRT_OPT) == True:
            self.getOvrtOpt = cfg.get(strSection, FILIED_OVRT_OPT)

        if cfg.has_option(strSection, FILIED_DOM) == True:
            self.getDom = cfg.get(strSection, FILIED_DOM)

        if cfg.has_option(strSection, FILIED_OP) == True:
            self.getOp = cfg.get(strSection, FILIED_OP)

        if type == 0:
            print "\t", "%5d %10s %15s %13s %12s %7s %7s %9s %15s %10s" % (index+1, self.reprNameShorter(self.getName, 10, 6),
                                                                           self.reprNameShorter(self.getPfx, 15, 11), 
                                                                           self.getCodeType,
                                                                           self.getTelIorOpt,
                                                                           self.getMin, self.getMax, self.getOvrtOpt,
                                                                           self.reprNameShorter(self.getDom, 15, 11), 
                                                                           self.reprNameShorter(self.getOp, 10, 6)
                                                                           )
        else:
            print "\t" "%12s = %s" % ('NAME', self.getName)
            print "\t" "%12s = %s" % ('PFX', self.getPfx)
            print "\t" "%12s = %s" % ('CODETYPE', self.getCodeType)
            print "\t" "%12s = %s" % ('TEL_IOR_OPT', self.getTelIorOpt)
            print "\t" "%12s = %s" % ('MIN', self.getMin)
            print "\t" "%12s = %s" % ('MAX', self.getMax)
            print "\t" "%12s = %s" % ('OVRT_OPT', self.getOvrtOpt)
            print "\t" "%12s = %s" % ('DOMAIN', self.getDom)
            print "\t" "%12s = %s" % ('OP', self.getOp)
            print ""
    
    def insertSection(self, cfg):
        index = self.getCurCount(cfg)
        NEW_SECTION = SECTION_PFX + str(index)
        
        cfg.add_section(NEW_SECTION)
        cfg.set(NEW_SECTION, FILIED_NAME, str(self.setName))
        cfg.set(NEW_SECTION, FILIED_PFX, str(self.setPfx))
        cfg.set(NEW_SECTION, FILIED_CODETYPE, str(self.setCodeType))
        cfg.set(NEW_SECTION, FILIED_TEL_IOR_OPT, str(self.setTelIorOpt))
        cfg.set(NEW_SECTION, FILIED_MIN, str(self.setMin))
        cfg.set(NEW_SECTION, FILIED_MAX, str(self.setMax))
        cfg.set(NEW_SECTION, FILIED_OVRT_OPT, str(self.setOvrtOpt))
        cfg.set(NEW_SECTION, FILIED_DOM, str(self.setDom))
        cfg.set(NEW_SECTION, FILIED_OP, str(self.setOp))
        
        with open(self.filepath, 'ab') as configfile:
            cfg.write(configfile)  
        
        self.printTitle()
        self.printSection(cfg, index, NEW_SECTION, 0)
        print ""
        self.setCurCount(cfg, index+1)
        
    def changeSection(self, cfg):
        CHG_SECTION = SECTION_PFX + str(self.delchgIndex)

        if self.setName != '':
           cfg.set(CHG_SECTION, FILIED_NAME, str(self.setName))
        if self.setPfx != '':
           cfg.set(CHG_SECTION, FILIED_PFX, str(self.setPfx))
        if self.setCodeType != '':
           cfg.set(CHG_SECTION, FILIED_CODETYPE, str(self.setCodeType))
        if self.setTelIorOpt != '':
           cfg.set(CHG_SECTION, FILIED_TEL_IOR_OPT, str(self.setTelIorOpt))
        if self.setMin != '':
           cfg.set(CHG_SECTION, FILIED_MIN, str(self.setMin))
        if self.setMax != '':
           cfg.set(CHG_SECTION, FILIED_MAX, str(self.setMax))
        if self.setOvrtOpt != '':
           cfg.set(CHG_SECTION, FILIED_OVRT_OPT, str(self.setOvrtOpt))
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
        DEL_SECTION = SECTION_PFX + str(self.delchgIndex)

        cfg.remove_section(DEL_SECTION)
        
        with open(self.filepath, 'wb') as configfile:
            cfg.write(configfile)
        
        self.relocateSection(cfg, self.delchgIndex, curCnt)
            
        self.setCurCount(cfg, curCnt-1)
        
    def relocateSection(self, cfg, startIndex, curCnt):
        for index in range(startIndex, curCnt):
            ORG_SECTION = SECTION_PFX + str(index)
            TEMP_SECTION = SECTION_PFX + str(index+1)
           
            if cfg.has_option(TEMP_SECTION, FILIED_NAME) == True:
                name = cfg.get(TEMP_SECTION, FILIED_NAME)
                pfx = cfg.get(TEMP_SECTION, FILIED_PFX)
                codec = cfg.get(TEMP_SECTION, FILIED_CODETYPE)
                ior = cfg.get(TEMP_SECTION, FILIED_TEL_IOR_OPT)
                min = cfg.get(TEMP_SECTION, FILIED_MIN)
                max = cfg.get(TEMP_SECTION, FILIED_MAX)
                ovrt = cfg.get(TEMP_SECTION, FILIED_OVRT_OPT)
                dom = cfg.get(TEMP_SECTION, FILIED_DOM)
                op = cfg.get(TEMP_SECTION, FILIED_OP)

                cfg.remove_section(TEMP_SECTION)

                cfg.add_section(ORG_SECTION)
                cfg.set(ORG_SECTION, FILIED_NAME, str(name))
                cfg.set(ORG_SECTION, FILIED_PFX, str(pfx))
                cfg.set(ORG_SECTION, FILIED_CODETYPE, str(codec))
                cfg.set(ORG_SECTION, FILIED_TEL_IOR_OPT, str(ior))
                cfg.set(ORG_SECTION, FILIED_MIN, str(min))
                cfg.set(ORG_SECTION, FILIED_MAX, str(max))
                cfg.set(ORG_SECTION, FILIED_OVRT_OPT, str(ovrt))
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
