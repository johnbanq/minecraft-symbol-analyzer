"""quick place to checkout the result of analysis
"""
import pickle
from pprint import pprint
from my_analyzer.analysis_result import AnalysisResult, AnalysisClass, FunctionDecl, VariableDecl, SimpleSymbolDecl


def view_my_analyzed(analyzed: AnalysisResult):
    for var in analyzed.variables:
        print(var.class_name+' '+var.symbol[2])
    pprint("total of %i variables"%len(analyzed.variables))

def main():
    with open("data/analyzed.pk", 'rb') as af:
        result = pickle.load(af)
        view_my_analyzed(result)


if __name__ == '__main__':
    main()
