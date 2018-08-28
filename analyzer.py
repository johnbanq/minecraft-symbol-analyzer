import pickle
import os.path
import argparse

from my_analyzer.analyzer import analyze
from my_analyzer.analysis_result import AnalysisResult,AnalysisClass,DeclType,FunctionDecl,VariableDecl,SimpleSymbolDecl


def analyze_decls(decls: list):
    """run analysis on declarations using a homebrewed analyzer

    Arguments:
        decls {list} -- list of symbols 

    Returns:
        AnalysisResult
    """
    done_decls = dict()
    for decl in decls:
        d = analyze(decl)
        if d.decl_type not in done_decls:
            done_decls[d.decl_type] = []
        done_decls[d.decl_type].append(d)
    
    #assemble to classes
    classes = dict()
    for func in done_decls[DeclType.function]:
        if func.class_name not in classes:
            classes[func.class_name] = AnalysisClass(func.class_name,[],[])
        classes[func.class_name].functions.append(func)
    
    for var in done_decls[DeclType.variable]:
        if var.class_name not in classes:
            classes[var.class_name] = AnalysisClass(var.class_name,[],[])
        classes[var.class_name].variables.append(var) 

    result = AnalysisResult(
        list(classes.values()),
        done_decls[DeclType.function],
        done_decls[DeclType.variable],
        done_decls[DeclType.simple_symbol]
        )   

    return result


def main():
    parser = argparse.ArgumentParser(description="analyze the text decls into decl objects")
    parser.add_argument("-d","--data_dir",help="name/path of the data directory",default="data")
    parser.add_argument("-s","--src_decls",help="name of the symbol pickle file",default="declarations.pk")
    parser.add_argument("-r","--result",help="name of the analyzed pickle file",default="analyzed.pk")
    args = parser.parse_args()

    decls_path = os.path.join(args.data_dir,args.src_decls)
    result_path = os.path.join(args.data_dir,args.result)

    with open(decls_path,'rb') as df,open(result_path,'wb') as rf:
        symbol_list = pickle.load(df)
        analysis_result = analyze_decls(symbol_list)
        pickle.dump(analysis_result,rf)

if __name__ == '__main__':
    main()
