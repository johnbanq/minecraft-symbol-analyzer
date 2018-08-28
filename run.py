import argparse
import os

from preprocessor import preprocess
from analyzer import analyze_decls
from postprocessor import run_post_processors,run_classifier,export_to_files


def main():

    parser = argparse.ArgumentParser(description="runs the entire chain")
    parser.add_argument("-d","--data_dir",help="name/path of the data directory",default="data")
    parser.add_argument("-s","--src_unmangled",help="name of the unmangled symbols file",default="symbols_unmangled.txt")
    parser.add_argument("-S","--src_mangled",help="name of the mangled symbols file",default="symbols_mangled.txt")
    args = parser.parse_args()

    mangled_path = os.path.join(args.data_dir,args.src_mangled)
    unmangled_path = os.path.join(args.data_dir,args.src_unmangled)

    print("Running Preprocessor")
    decl_result,nondecl_result = None,None
    try:
        with open(unmangled_path,'r') as src_file, open(mangled_path,'r') as src_mangled_file:
                decl_result,nondecl_result = preprocess(src_file,src_mangled_file)
    except Exception as e:
        print("Unable to read symbol file: %s & %s : "%(mangled_path,unmangled_path)+str(e))
        exit()

    print("Running Analyzer")
    analyzed = analyze_decls(decl_result)

    print("Running Postprocessor & Classifier")
    run_post_processors(analyzed)
    classified = run_classifier(analyzed.classes)
    print("Classified %i classes into %i categories:"%(len(analyzed.classes),len(classified.keys())))
    for k,v in classified.items():
        print("%s    %i classes"%(k,len(v)))

    print("Exporting to files")
    if os.path.exists(os.path.join(args.data_dir,"decls")):
        os.rmdir(os.path.join(args.data_dir,"decls"))
    export_to_files(os.path.join(args.data_dir,"decls"),classified)

if __name__ == '__main__':
    main()