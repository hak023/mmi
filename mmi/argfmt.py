
import datetime

_ARG_FORMAT_DELIM = ' '
_ARG_FORMAT_COMMA = ','

_ARG_FORMAT_STRING = 'S'
_ARG_FORMAT_EXSTRING = 'X'
_ARG_FORMAT_INTEGER = 'I'
_ARG_FORMAT_DATE = 'D'
_ARG_FORMAT_SUPPORT = set([_ARG_FORMAT_STRING, _ARG_FORMAT_INTEGER, _ARG_FORMAT_DATE, _ARG_FORMAT_EXSTRING])

_ARG_FORMAT_TYPE_DELIM = ':'
_ARG_FORMAT_OR = '|'
_ARG_FORMAT_RANGE = '~'


class MMIArgException(Exception):
    pass

class MMIArgFormatException(MMIArgException):
    pass

class MMIArgValueException(MMIArgException):
    pass

class ArgFmtElement(object):
    '''
    ArgFmtElement Interface. Composite Pattern
    '''
    def __init__(self):
        pass

    def validate(self, val):
        pass

class ArgFmt(ArgFmtElement):
    def __init__(self, argName, argType, argValues, optional=False):
        self.argName = argName
        self.argType = argType
        self.argValues = argValues
        self.optional = optional

    def validate(self, val):
        if val is None or val == '':
            if self.optional == False:
                raise MMIArgValueException(self.argName + ' is required')
            else:
                return
        
        for arg in self.argValues:
            if arg.includes(val) == True:
                return
        
        raise MMIArgValueException(self.argName + ' is invalid :' + val)
    
    def __str__(self, *args, **kwargs):
        return self.__class__.__name__                                      \
            + '[argName=' + self.argName + ', argType=' + self.argType      \
            + ', argValues=' + str(self.argValues) + ', optional=' + str(self.optional) + ']'

class ArgFmts(ArgFmtElement):
    def __init__(self, fmts=None):
        if fmts is None:
            fmts = []
        self.fmts = fmts

    def validate(self, val):
        
        values = [None for _x in range(len(self.fmts))]
        vals = []
        if val is not None:
            vals = val.split(_ARG_FORMAT_COMMA)
        
        if len(vals) > len(self.fmts):
            raise MMIArgValueException('Too many argument values : ' + val)
        
        for i in range(len(vals)):
            values[i] = vals[i]
        
        for i in range(len(values)):
            self.fmts[i].validate(values[i])

class ArgValue(object):
    def includes(self, value):
        pass

class StringArgValue(ArgValue):
    def includes(self, value):
        if value is None:
            return False
        
        if type(value) is not str:
            value = repr(value)
            
        return (len(value) > 0) 

class EqualArgValue(ArgValue):
    """
    Deprecated
    For single String or Integer value
    """
    def __init__(self, value):
        self.value = value
        
    def includes(self, value): 
        return self.value == value

class IntegerArgValue(ArgValue):
    def includes(self, value):
        if value is None:
            return False

        if type(value) is not int:
            try :
                value = int(value)
            except ValueError:
                return False
        
        return True

class IntegerRangeArgValue(ArgValue):
    """
    For single String or Integer value
    """
    def __init__(self, fromInt, toInt):
        self.fromInt = fromInt
        self.toInt = toInt

    def includes(self, value):
        if value is None:
            return False

        if type(value) is not int:
            try :
                value = int(value)
            except ValueError:
                return False

        return (value >= self.fromInt and value <= self.toInt)

class StringSetArgValue(ArgValue):
    def __init__(self, values):
        self.values = values
    def includes(self, value): 
        if value is None:
            return False

        return value in self.values

class IntegerSetArgValue(ArgValue):
    def __init__(self, values):
        self.values = values
    def includes(self, value): 
        if value is None:
            return False

        if type(value) is not int:
            try :
                value = int(value)
            except ValueError:
                return False
        
        return value in self.values

class DateArgValue(ArgValue):
    def includes(self, value):
        if value is None:
            return False

        try :
            datetime.datetime.strptime(value, '%y%m%d%H%M')
        except ValueError:
            return False

        return True

def parseArguments(formats):
    if formats is None or len(formats) == 0:
        return None
    
    _argfmts = ArgFmts()
    
    format_list = formats.split(_ARG_FORMAT_DELIM)

    for _fmt in format_list:
        _argfmts.fmts.append(parseArgument(_fmt))
    
    return _argfmts
        
def parseArgument(argformat):
    
    if argformat is None or len(argformat) == 0:
        return None

    fmtstr = argformat
    
    optional = False
    if fmtstr.startswith('[') != fmtstr.endswith(']'):
        raise MMIArgFormatException("Optional argument must be starts with '[' and ends with ']' : " + argformat)

    if fmtstr.startswith('[') and fmtstr.endswith(']') :
        # optional
        optional = True
        fmtstr = fmtstr.replace('[', '', 1)
        fmtstr = fmtstr.replace(']', '', 1)
    
    #argName
    (argName, _x, arg_type_value) = fmtstr.partition(_ARG_FORMAT_TYPE_DELIM)
    arg_value = None
    
    # argType
    if len(arg_type_value) == 1:
        argType = arg_type_value
    elif len(arg_type_value) > 1:
        argType = arg_type_value[0]
        arg_value = arg_type_value[1:]
    else: 
        raise MMIArgFormatException('Argument type ommitted : ' + argformat)

    if argType not in _ARG_FORMAT_SUPPORT:
        raise MMIArgFormatException('Argument type must be one of ' + _ARG_FORMAT_SUPPORT + ": " + argformat)

    if arg_value is not None:
        if len(arg_value) > 2:
            if arg_value.startswith('(') and arg_value.endswith(')'):
                arg_value = arg_value.replace('(', '', 1)
                arg_value = arg_value.replace(')', '', 1)
            else:
                raise MMIArgFormatException("Argument value must be starts with '(' and ends with ')' : " + argformat)
        else :
            raise MMIArgFormatException("Argument value must be starts with '(VALUES)' : " + argformat)

    #argValues
    argValues = parseArgumentValue(argType, arg_value)

    return ArgFmt(argName, argType, argValues, optional)
    
    

def parseArgumentValue(argtype, valfmt):
    
    if valfmt is None or len(valfmt) == 0:
        if argtype == _ARG_FORMAT_STRING:
            return [StringArgValue()]
        elif argtype == _ARG_FORMAT_EXSTRING:
            return [StringArgValue()]        
        elif argtype == _ARG_FORMAT_INTEGER:
            return [IntegerArgValue()]
        elif argtype == _ARG_FORMAT_DATE:
            return [DateArgValue()]
        else:
            raise MMIArgFormatException('Unknown argument type :' + argtype)
    else :
        if argtype == _ARG_FORMAT_STRING:
            _values = valfmt.split(_ARG_FORMAT_OR)
            if '' in _values:
                raise MMIArgFormatException('Invalid String format :' + valfmt)
            return [StringSetArgValue(_values)]

        elif argtype == _ARG_FORMAT_EXSTRING:
            _values = valfmt.split(_ARG_FORMAT_OR)
            if '' in _values:
                raise MMIArgFormatException('Invalid ExString format :' + valfmt)
            return [StringSetArgValue(_values)]
            
        elif argtype == _ARG_FORMAT_INTEGER:
            strs = valfmt.split(_ARG_FORMAT_OR)
            argValues = []
            values = []
            for _str in strs:
                try :
                    if _str.find(_ARG_FORMAT_RANGE) > -1:
                        fromInt, toInt = _str.split(_ARG_FORMAT_RANGE)
                        argValues.append(IntegerRangeArgValue(int(fromInt), int(toInt)))
                        
                    else:
                        values.append(int(_str))
                        
                except ValueError:
                    raise MMIArgFormatException('Invalid Integer argument :' + _str)
            
            if len(values) > 0:
                argValues.append(IntegerSetArgValue(values))
            
            return argValues
        
        elif argtype == _ARG_FORMAT_DATE:
            raise MMIArgFormatException('Date argument must has no values format :' + valfmt)
        
        else:
            raise MMIArgFormatException('Unknown argument type :' + argtype)
        

        
