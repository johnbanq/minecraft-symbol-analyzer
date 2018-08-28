from class_assembler import assemble_class_def
from my_analyzer.analysis_result import AnalysisResult,AnalysisClass,FunctionDecl,Virtualness,VariableDecl,SimpleSymbolDecl
import os.path
import pickle

def prefix_classify_factory(prefix):
    return lambda clazz: clazz.name.startswith(prefix)

post_processors = [

]

classifier = [
    ("support/std",prefix_classify_factory("std::")),
    ("support/web",prefix_classify_factory("web::")),
    ("support/leveldb",prefix_classify_factory("leveldb::")),
    ("support/underscored",prefix_classify_factory("_")),
    ("support/mce",prefix_classify_factory("mce::")),
    ("support/boost",prefix_classify_factory("boost::")),
    ("support/xbox",prefix_classify_factory("xbox::")),
    ("support/UI",prefix_classify_factory("UI::")),
    ("support/pplx",prefix_classify_factory("pplx::")),
    ("support/moodycamel",prefix_classify_factory("moodycamel::")),
    ("support/RakNet",prefix_classify_factory("RakNet::")),
    ("support/createScreen",prefix_classify_factory("createScreen")),

    ("unknown",lambda clazz:True)
]

def run_post_processors(result : AnalysisClass):

    for process in post_processors:
        process(result)

def run_classifier(classes:list):

    classified = dict()

    for clazz in classes:
        for cler in classifier:
            if cler[1](clazz):
                if cler[0] not in classified:
                    classified[cler[0]] = []
                classified[cler[0]].append(clazz)
                break

    return classified

def mangle_filename(name):
    dst_name = ""
    #transform the class name so OS can accept the file
    translators = {
        #you are not gonna see class name with these
        '\\':'$',
        '/':'$',
        '|':'$',
        #but with these
        '*':'@',
        ':':'-',
        '<':'[',
        '>':']'
    }

    for ch in name[:150]:
        if ch in translators:
            dst_name+=translators[ch]
        else:
            dst_name+=ch

    return dst_name

def export_to_files(dst_dir:str,classified : dict):
    for cname,cclazz in classified.items():
        cpath = os.path.join(dst_dir,cname)
        if not os.path.exists(cpath):
            os.makedirs(cpath)

        for clazz in cclazz:
            with open(os.path.join(cpath,mangle_filename(clazz.name)+".h"),'w+') as f: #to avoid the None class
                f.write(assemble_class_def(clazz))


def main():
    data_dir = "data"
    src_analyzed = "analyzed.pk"

    analyzed = None
    with open(os.path.join(data_dir,src_analyzed),'rb') as af:
        analyzed = pickle.load(af)

    run_post_processors(analyzed)
    classified = run_classifier(analyzed.classes)
    export_to_files(os.path.join(data_dir,"decls"),classified)

if __name__ == '__main__':
    main()
            
    
    