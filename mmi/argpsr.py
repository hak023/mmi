
from mmi.argfmt import MMIArgValueException

_ARGPARSER_ARG_DELIM = ','
_ARGPARSER_KV_DELIM = '='

class ArgParser(object):
    def __init__(self):
        '''
        Constructor
        '''
        pass
    def parse(self, argstring):
        pass
    def toArgList(self, argfmts):
        pass
    

class KeyValueArgParser(ArgParser):
    
    _ARGPARSER_IGNORE_EMPTY_KV = False

    def __init__(self):
        self.argmap = None
    
    def parse(self, argstring):
        self.argmap = dict()

        if argstring is None:
            return

        _lst = argstring.split(_ARGPARSER_ARG_DELIM)
        
        for _pair in _lst:
            if len(_pair.strip()) == 0:
                continue

            _arrPair = _pair.split(_ARGPARSER_KV_DELIM, 1)
            
            if len(_arrPair) != 2:
                raise MMIArgValueException('Unparsable key=value argument : ' + _pair)

            _k = _arrPair[0].strip()
            _v = _arrPair[1].strip()
            
            if KeyValueArgParser._ARGPARSER_IGNORE_EMPTY_KV is True:
                if len(_k) is 0 or len(_v) is 0:
                    continue
            else:
                if len(_k) is 0:
                    raise MMIArgValueException('Empty key argument : ' + _pair)
                if len(_v) is 0:
                    raise MMIArgValueException('Empty value argument : ' + _pair)
                
            self.argmap[_k] = _v

    def toArgList(self, argfmts):
        _lst = list()

        # Check if unknown arguments are found
        for _key in self.argmap.iterkeys():
            _validKey = False
            
            for i in range(len(argfmts.fmts)):
                if argfmts.fmts[i].argName == _key:
                    _validKey = True
                    break
            
            if _validKey is False:
                raise MMIArgValueException('Unknown argument name : ' + _key)
        
        for i in range(len(argfmts.fmts)):
            _lst.append(self.argmap.get(argfmts.fmts[i].argName, ''))
            
        return _lst
    
class OrderedArgParser(ArgParser):
    def __init__(self):
        self.arglist = None
    
    def parse(self, argstring):
        _lst = argstring.split(_ARGPARSER_ARG_DELIM)
                
        for i in range(len(_lst)):
            _lst[i] = _lst[i].strip()

        self.arglist = _lst

    def toArgList(self, argfmts):
        _lst = list('' for _i in range(len(argfmts.fmts)))
        
        for _i in range(len(self.arglist)):
            _lst[_i] = self.arglist[_i]
            
        return _lst

def createArgParser(argstring):
    _delidx = str(argstring).find(_ARGPARSER_KV_DELIM)
    if _delidx > -1:
        return KeyValueArgParser()
    else:
        return OrderedArgParser()

if __name__ == "__main__":
    print repr(createArgParser(''))
    print type('abc=3'.split('='))
    print repr(createArgParser('1,2,3,4 ,   4,'))
    print repr(createArgParser('3,2,4,5,'))
    print repr(createArgParser('a=2,b=3,c=4'))
