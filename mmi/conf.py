
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

class MMIConfig(ConfigParser):
    
    SECTION_COMMON = 'COMMON'

    def __init__(self):
        ConfigParser.__init__(self)
        ConfigParser.read(self, '/home/vfras/mmi/conf/mmi.cfg')

    def getbooleanCommon(self, option, default=None):
        value = default
        try :
            value = self.getboolean(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value
    
    def getCommon(self, option, default=None):
        value = default
        try :
            value = self.get(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value

    def getintCommon(self, option, default=None):
        value = default
        try :
            value = self.getint(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass

        return value

    def getfloatCommon(self, option, default=None):
        value = default
        try :
            value = self.getfloat(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value
    
    def getLocal(self, cmd, option, default=None, raw=False):
        value = default
        try :
            value = self.get(cmd.getCommandFileName(), option, raw)
        except NoSectionError:
            pass
        except NoOptionError:
            pass

        return value

    def getintLocal(self, cmd, option, default=None, raw=False):
        value = default
        try :
            value = self.getint(cmd.getCommandFileName(), option, raw)
        except NoSectionError:
            pass
        except NoOptionError:
            pass

        return value

    def getfloatLocal(self, cmd, option, default=None, raw=False):
        value = default
        try :
            value = self.getfloat(cmd.getCommandFileName(), option, raw)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value
    
 #################################################################################################   

class CmdConfig(ConfigParser):

    def __init__(self):
        ConfigParser.__init__(self)
        ConfigParser.read(self, '/home/vfras/mmi/conf/cmd.cfg')

    def getbooleanCommon(self, option, default=None):
        value = default
        try :
            value = self.getboolean(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value
    
    def getCommon(self, option, default=None):
        value = default
        try :
            value = self.get(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value

    def getintCommon(self, option, default=None):
        value = default
        try :
            value = self.getint(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass

        return value

    def getfloatCommon(self, option, default=None):
        value = default
        try :
            value = self.getfloat(MMIConfig.SECTION_COMMON, option)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value
    
    def getLocal(self, cmd, option, default=None, raw=False):
        value = default
        try :
            value = self.get(cmd.getCommandFileName(), option, raw)
        except NoSectionError:
            pass
        except NoOptionError:
            pass

        return value

    def getintLocal(self, cmd, option, default=None, raw=False):
        value = default
        try :
            value = self.getint(cmd.getCommandFileName(), option, raw)
        except NoSectionError:
            pass
        except NoOptionError:
            pass

        return value

    def getfloatLocal(self, cmd, option, default=None, raw=False):
        value = default
        try :
            value = self.getfloat(cmd.getCommandFileName(), option, raw)
        except NoSectionError:
            pass
        except NoOptionError:
            pass
        
        return value

