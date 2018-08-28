from .analysis_result import SimpleSymbolDecl,FunctionDecl,VariableDecl

def pick_closing_interval(decl:str,end_position,token_end,token_begin):
    """
        try to pick a closing interval from end_position to start of string (inclusive)
        eg : "A(()(()))",len(the_string_on_the_left)-1,")","(") -> "(()(()))"
    """

    if decl[end_position] != token_end:
        raise ValueError

    level = 0
    end_pos = -1
    for pos in range(end_position,-1,-1):
        if decl[pos] == token_end:
            level+=1
        elif decl[pos] == token_begin:
            level-=1
            if level == 0:
                end_pos = pos
                break
    else:
        raise ValueError

    return decl[end_pos:end_position+1]


def substr_argument_at_end(decl:str):
    """
    pick the argument list from declaration end
    """
    return pick_closing_interval(decl,len(decl)-1,')','(')


def substr_identifier_at_end(decl:str,colon_allowed=True,space_allowed=False):
    """
    pick the identifier (the potentially superlong class_name::func_name's func_name) out from declaration end

    the colon_allowed param is to extract func_name from class_name
    the space allowed is to extract funcname as a desperate measure
    """
    pos = len(decl)-1

    #handle the nasty case,avoid operator> etc...
    prescan_pos = pos
    while (not decl[prescan_pos].isalpha()) and prescan_pos>=0:
        prescan_pos-=1
    
    if decl.endswith("operator",0,prescan_pos+1):
        pos = prescan_pos

    while pos >= 0:
        if decl[pos] == '>':
            templ_string = pick_closing_interval(decl,pos,'>','<')
            pos -= len(templ_string)
            continue

        if decl[pos] == ')':
            templ_string = pick_closing_interval(decl,pos,')','(')
            pos -= len(templ_string)
            continue
        
        if ((not space_allowed) and decl[pos] == ' ') or ((not colon_allowed) and decl[pos] == ':'):
            #we have reached the end of identifier
            return decl[pos+1:]
        else:
            pos-=1 #proceed
    else:
        return decl #reached -1,the entire string is the thing!


def split_class_declname_from_identifier(ident):
    func_name = substr_identifier_at_end(ident,colon_allowed=False,space_allowed=True)
    class_name = ident[:-len(func_name)-2]
    return class_name,func_name


def analyze(symbol :tuple):
    """run analysis on a symbol.
    
    Arguments:
        symbol: the symbol to analyze
    
    Returns:
        a decl,can know it's type by .decl_type
    """
    
    decl = symbol[2]
    #strip const identifier
    const = False
    if decl.endswith("const"):
        const = True
        decl = decl[:-len("const")].strip()
    
    if(decl.endswith(')')):
        #its a function!

        #parse argument
        args = substr_argument_at_end(decl)
        decl = decl[:-len(args)]
        
        #parse class::function_name
        decl = decl.strip()
        func_name = substr_identifier_at_end(decl,colon_allowed=False,space_allowed=True)
        decl = decl[:-len(func_name)]

        class_name = None
        if decl.endswith('::'):
            class_name = substr_identifier_at_end(decl)[:-2]
            decl = decl[:-len(class_name)-2]

        #parse potential return type
        decl = decl.strip()
        ret = None
        if decl:
            ret = substr_identifier_at_end(decl)

        return FunctionDecl(symbol,ret,class_name,func_name,args,const)
    else:
        #consider it to be a variable or simple symbol

        #parse the identifier
        var_ident = substr_identifier_at_end(decl,colon_allowed=False)
        decl = decl[:-len(var_ident)]

        if decl.endswith("::"):
            #its a member variable
            decl = decl[:-2].strip()
            
            prefix = ""
            if decl.endswith("const"): # we consider static vars in func as "class members" too
                prefix = " const"
                decl = decl[:-len("const")].strip()
            
            class_ident = substr_identifier_at_end(decl)

            #parse the potential type
            var_type = None
            if decl:
                var_type = substr_identifier_at_end(decl)

            return VariableDecl(symbol,var_type,class_ident+prefix,var_ident)

        else:
            #its a simple symbol 
            decl = decl.strip()
            #parse the potential type
            var_type = None
            if decl:
                var_type = substr_identifier_at_end(decl)
            
            return SimpleSymbolDecl(symbol,var_type,var_ident)

