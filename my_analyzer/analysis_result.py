from enum import Enum


class AnalysisResult:
    """
    represents analysis result of a file
    """
    def __init__(self,classes,functions,variables,simple_symbols):
        self.classes = classes

        #redundant:info for checking analysis result
        self.functions = functions
        self.variables = variables
        self.simple_symbols = simple_symbols

class AnalysisClass:
    """
    represents a class reasembled from decls
    """

    def __init__(self, name, functions, variables):
        self.name = str(name)
        self.parent = None #TODO:add a post processor to analyze it

        self.functions = functions
        self.variables = variables


Virtualness = Enum("Virtualness", ("none", "virtual", "pure_virtual"))
DeclType = Enum("DeclType", ("function", "variable", "simple_symbol"))


class FunctionDecl:
    """
    represents a member function for a class
    """

    def __init__(self, symbol, ret_type, class_name, func_name, arguments, const, virtualness=Virtualness.none):
        self.symbol = symbol
        self.decl_type = DeclType.function

        self.ret_type = ret_type
        self.class_name = class_name
        self.func_name = func_name
        self.arguments = arguments
        self.const = const

        self.virtualness = virtualness


class VariableDecl:
    """
    represents a member variable for a class
    """

    def __init__(self, symbol, var_type, class_name, var_name):
        self.symbol = symbol
        self.decl_type = DeclType.variable

        self.var_type = var_type
        self.class_name = class_name
        self.var_name = var_name


class SimpleSymbolDecl:
    """
    represents those symbols that didnt went through mangling,unable to infer their type
    """

    def __init__(self, symbol, sym_type, name):
        self.symbol = symbol
        self.decl_type = DeclType.simple_symbol

        self.sym_type = sym_type
        self.name = name
