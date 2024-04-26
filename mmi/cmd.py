
import sys
from getopt import getopt
from mmi.conf import MMIConfig
from mmi.conf import CmdConfig
import __main__
import os
from mmi import argfmt, argpsr
from mmi.argfmt import MMIArgValueException
from mmi.argpsr import createArgParser, _ARGPARSER_ARG_DELIM
import traceback

MMI_COMMAND_RESULT_SUCCESS = 1
MMI_COMMAND_RESULT_FAILURE = 0
MMI_COMMAND_RESULTS = ['NOK','OK']

MMI_COMMAND_TYPE_INTERNAL = "internal"
MMI_COMMAND_TYPE_EXTERNAL = "external"
MMI_COMMAND_TYPE_OAM = "oam"


class MMICommandException(Exception):
    # Subclasses that define an __init__ must call Exception.__init__
    # or define self.args.  Otherwise, str() will fail.
    pass

class MMICommandParamException(MMICommandException):
    pass

class MMIMessage(object):
    pass

class MMIInputMessage(MMIMessage):
    pass

class MMIOutputMessage(MMIMessage):
    def __init__(self, result=MMI_COMMAND_RESULT_FAILURE, reason=None):
        self.result = MMI_COMMAND_RESULT_FAILURE
        self.reason = reason

class MMICommand(object):
    
    _OPTS_SHORT="cnfvuhdtp"
    _OPTS_LONG = ["category", "name", "file", "version", "usage", "help", "document", "type", "parameters"]
    
    '''
    MMICommand
    '''
    def __init__(self):
        self.exception = None
        self.config = MMIConfig()
        self.cmdconf = CmdConfig()

        ####################################################################################
        # values
        ####################################################################################
        self.replaceFlag = 0
        self.saveStr = ''
        ####################################################################################
        
    def getCommandFileName(self):
        fileName, _fileExt = os.path.splitext(os.path.basename(__main__.__file__))
        return fileName

    def getCommandName(self):
        cmd = self.cmdconf.getLocal(self, 'command.name')
        if cmd is None:
            cmd = 'Not configured : command.name'
        return cmd

    def getCommandDesc(self):
        cmd = self.cmdconf.getLocal(self, 'command.desc')
        if cmd is None:
            cmd = 'Not configured : command.desc'
        return cmd

    def getParametersFormat(self):
        return self.cmdconf.getLocal(self, 'command.parameters')
       
    def printHeader(self):
        print ""
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

    def printTail(self):
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    
    def printCategory(self):
        self.printHeader()
        category = self.cmdconf.getLocal(self, 'command.category').encode('euc-kr')
        if category is None:
            print 'Not configured'
        else :
            print category
        self.printTail()

    def printCommandName(self):
        self.printHeader()
        print self.getCommandName()
        self.printTail()

    def printCommandDesc(self):
        self.printHeader()
        print self.getCommandDesc()
        self.printTail()

    def printVersion(self):
        self.printHeader()
        print "SHAPSHOT"
        self.printTail()
    
    def printParameters(self):
        self.printHeader()
        parameters = self.cmdconf.getLocal(self, 'command.parameters').encode('euc-kr')
        if parameters is None:
            print 'Not configured : command.parameters'
        else :
            print parameters
        self.printTail()
    
    def printUsage(self):
        self.printHeader()
        parameters = self.cmdconf.getLocal(self, 'command.parameters').encode('euc-kr')
        if parameters is None:
            parameters = ''
        print 'USAGE :', self.getCommandName(), parameters
        self.printTail()

    def printHelp(self):
        self.printHeader()
        _help = self.cmdconf.getLocal(self, 'command.help').encode('euc-kr')
        if _help is None:
            print 'Not configured command.help'
        else :
            print _help
        self.printTail()

    def printDocument(self):
        self.printHeader()
        doc = self.cmdconf.getLocal(self, 'command.document').encode('euc-kr')
        if doc is None:
            print 'Not configured command.document'
        else :
            print doc
        self.printTail()

    def printType(self):
        self.printHeader()
        _type = self.cmdconf.getLocal(self, 'command.type').encode('euc-kr')
        if _type is None:
            _type = self.cmdconf.getCommon('command.type.default', MMI_COMMAND_TYPE_EXTERNAL)
        print _type
        self.printTail()

    def printMessage(self, imsg, omsg):
        self.printHeader()
        print "[INPUT]"
        print "%-10s : %s" % ('COMMAND', self.getCommandName())
        #print ""
        #print "%-12s %s" % ('', self.getCommandDesc()) 
                
        try:
            self.printInputMessage(imsg)
        except Exception:
            print "%-10s : %s" % ('ARGS', repr(sys.argv[1:]))
            
        print ""
        print "[OUTPUT]"
        
        if(self.exception is None) : 
            print "%-10s : %s" % ('RESULT', MMI_COMMAND_RESULTS[omsg.result])
            if omsg.result == MMI_COMMAND_RESULT_FAILURE :
                print "%-10s : %d" % ('REASON', omsg.reason)
            
            try:
                self.printOutputMessage(omsg)
            except Exception:
                pass
            
        else :
            print "%-10s : %s" % ('RESULT', MMI_COMMAND_RESULTS[MMI_COMMAND_RESULT_FAILURE])
            print "%-10s : %s" % ('REASON', self.exception)
        self.printTail()
        
        if(self.cmdconf.getbooleanCommon('debug.printexception', False) is True) :
            traceback.print_exc(file=sys.stdout)

    
    def printInputMessage(self, imsg):
        pass

    def printOutputMessage(self, omsg):
        pass

    def execute(self):
        pass

    def validateArgs(self, args):

        argfmts = argfmt.parseArguments(self.getParametersFormat())

        if argfmts == None:
            if args is not None and len(args) > 0 :
                raise MMIArgValueException('Command arguments are not required : ' + repr(args))
            else:
                return []
            
        else :

            _argstring = _ARGPARSER_ARG_DELIM.join(args)

            ####################################################################################
            # find qouta string and replace to pipe sign 
            ####################################################################################

            '''
            if len(_argstring) > 0:
               temp = []
               remove_args = []
               temp = _argstring.split(",")
            
               for string in temp: 
                   remove_args.append(string.replace("\"", ""))
                   remove_args.append(",")
            
               _argstring = ''.join(remove_args)

            if self.replaceFlag > 0:
                quota_idx_1 = _argstring.find("\"", 0, len(_argstring))
                quota_idx_2 = _argstring.find("\"", quota_idx_1+1, len(_argstring))
      
                tempStr_1 = _argstring[0:quota_idx_1]
                tempStr_2 = _argstring[quota_idx_2+1:]
                
                _argstring = tempStr_1 + "|" + tempStr_2
            '''   
            ####################################################################################

            parser = createArgParser(_argstring)
            parser.parse(_argstring)

            _argList = parser.toArgList(argfmts)
            argfmts.validate(','.join(_argList))
           
            ####################################################################################
            # replace pipe sign to real string
            ####################################################################################
            '''
            if self.replaceFlag > 0:
                for k in range(len(_argList)):
                    if _argList[k] == "|":
                        _argList[k] = self.saveStr    
            '''
            ####################################################################################          
            
            return _argList
    
    def getopt(self, args=sys.argv[1:]):
        
        ####################################################################################
        # find qouta string save.. 
        ####################################################################################
        
        '''
        chk_str = ''.join(args)
        comma_check = chk_str.find("\"", 0, len(chk_str))

        if comma_check > -1:
            self.replaceFlag = 1
                       
            tempStr = ''
            for _str in args:
                tempStr = tempStr + _str + " "
            
            temp = tempStr.split("\"")
            self.saveStr = temp[1]
        
        #print self.saveStr
        '''
        ####################################################################################
        
        if len(args) > 0 and args[0].startswith('-') and len(args[0]) > 1 and args[0][1].isdigit():
           args.insert(0, '--')

        _opts, _args = getopt(args, MMICommand._OPTS_SHORT, MMICommand._OPTS_LONG)      
        
        if _args is None or len(_args) is 0:
            return _opts, []
        
        _argstr = ' '.join(_args)
        
        _args = _argstr.split(self.cmdconf.getCommon('command.args.sep', argpsr._ARGPARSER_ARG_DELIM))
        
        for i in range(len(_args)):
            _args[i] = _args[i].strip()

        return _opts, _args
    
    def processOptions(self, opts):
        for (o, _args) in opts:
            if o in ("-c", "--category"):
                self.printCategory()
            elif o in ("-n", "--name"):
                self.printCommandName()
            elif o in ("-f", "--file"):
                print __file__
            elif o in ("-v", "--version"):
                self.printVersion()
            elif o in ("-u", "--usage"):
                self.printUsage()
            elif o in ("-h", "--help"):
                self.printHelp()
            elif o in ("-d", "--document"):
                self.printDocument()
            elif o in ("-t", "--type"):
                self.printType()
            elif o in ("-p", "--parameters"):
                self.printParameters()
            else:
                self.printUsage()
            break
        
        return o

    def printExcecption(self, e):
        pass
