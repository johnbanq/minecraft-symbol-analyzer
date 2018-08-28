"""
quickhand places to check and export stuff after preprocessing
"""
import pickle
import argparse
import os.path

default_decl_filename = "declarations.pk"
default_nondecl_filename = "non_declarations.pk"

def symbol_to_string(sym):
    addr,stype,unmangled,mangled = sym
    return "%s"% unmangled # addr,type,unmangled,mangled

def dump(srcpath,dstpath):
    with open(srcpath,'rb') as sf,open(dstpath,'w') as df:
        symlist = pickle.load(sf)
        for sym in symlist:
            df.write(symbol_to_string(sym)+'\n')        

def main():

    parser = argparse.ArgumentParser(description="turns the parsed symbols back to text files for checking")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d","--decl",help="output the result of preprocessed decls in default decl file",action="store_true")
    group.add_argument("-n","--nondecl",help="output the result of preprocessed nondecls in default nondecl file",action="store_true")
    group.add_argument("-f","--file",help="specify other symbol list pickle file")
    
    parser.add_argument("-D","--data_dir",help="name/path of the data directory",default="data")
    parser.add_argument("-r","--result_file",help="filename of the result file",default="viewing.txt")
    args = parser.parse_args()

    src = None
    if args.decl:
        src = os.path.join(args.data_dir,default_decl_filename)
    elif args.nondecl:
        src = os.path.join(args.data_dir,default_nondecl_filename)
    else:
        src = os.path.join(args.data_dir,args.file)
    
    dump(src,os.path.join(args.data_dir,args.result_file))

if __name__ == '__main__':
    main()
