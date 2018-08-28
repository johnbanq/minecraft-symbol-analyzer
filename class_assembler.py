from my_analyzer.analysis_result import AnalysisResult,AnalysisClass,FunctionDecl,Virtualness,VariableDecl,SimpleSymbolDecl

def assemble_class_def(clazz:AnalysisClass):
    
    head,tail = "",""
    if clazz.name:
        head = "class %s %s {\n" % (clazz.name,((":public "+clazz.parent) if clazz.parent else ""))
        tail = "};"

    decls = []
    underscored_decls = []
    for func in clazz.functions:
        if func.func_name.startswith("_"):
            underscored_decls.append(assemble_function_decl(func))
        else:
            decls.append(assemble_function_decl(func))

    decls.sort()
    decls.append(" ")
    underscored_decls.sort()
    decls+=underscored_decls

    decls.append(" ")

    for var in clazz.variables:
        decls.append(assemble_variable_decl(var))
    decls.append(" ")
    

    return head+"\n".join(decls)+"\n"+tail

def assemble_function_decl(func:FunctionDecl,mbed_symbol=False):

    result = "    "
    if func.ret_type:
        result += func.ret_type

    if func.virtualness != Virtualness.none:
        result += "virtual "

    result += " %s%s" % (func.func_name,func.arguments)
    if func.const:
        result+=" const"

    if func.virtualness == Virtualness.pure_virtual:
        result += "=0"
        
    result+=';'

    #assemble the comments
    if mbed_symbol:
        result +="""
            //mangled: %s
            //symbol_type: %s
            """ % (func.mangled,func.symbol_type)#,func.line_num)

    return result

def assemble_variable_decl(var:VariableDecl,mbed_symbol=False):
    result = "    static %s;" %(var.var_name)
    if mbed_symbol:
        result +="""
            /*
            * mangled: %s
            * symbol_type: %s
            * line_num_in_declarations.txt: %s
            * type: %s
            */ """ % (var.mangled,var.symbol_type,var.line_num,var.type)
    return result