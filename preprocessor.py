# -*- coding: UTF-8 -*-
import re
import pickle
import argparse
import os.path

def make_symbol(addr,link_type,name,mangled_name):
    """
    symbol is a tuple of address,link_type(a char represents link),unmangled name and mangled names
    """
    return addr,link_type,name,mangled_name


def preprocess(src,src_mangled):
    """preprocesses the list of lines from nm output,filter away addr&linktype, vtables etc.
    
    Arguments:
        src_file {Iterable} -- list consists the list of unmangled symbols from nm tool
        src_mangled_file {Iterable} -- list consists the list of mangled symbols from nm tool
    
    Return:
        two list of symbols: decl,non_decl represents declaration and non-declaration
    """
    non_declaration = ("typeinfo","vtable","non-virtual thunk","virtual thunk","VTT","guard variable")
    splitter = re.compile("([0-9a-f]* | *)(\S) (.*)")

    decl,non_decl = [],[]
    
    for line,mangled_line in zip(src,src_mangled):
        mangled_line = mangled_line.strip()

        resplit = splitter.match(line)
        addr,link_type,name = resplit.groups()

        resplit = splitter.match(mangled_line)
        _,_,name_mangled = resplit.groups()

        if name.startswith(non_declaration):
            non_decl.append(make_symbol(addr,link_type,name,name_mangled))
        else:
            decl.append(make_symbol(addr,link_type,name,name_mangled))
    
    return decl,non_decl


def main():

    parser = argparse.ArgumentParser(description="preprocess the nm output into decl & nondecls")
    parser.add_argument("-d","--data_dir",help="name/path of the data directory",default="data")
    parser.add_argument("-s","--src_unmangled",help="name of the unmangled symbols file",default="symbols_unmangled.txt")
    parser.add_argument("-S","--src_mangled",help="name of the mangled symbols file",default="symbols_mangled.txt")
    parser.add_argument("-r","--result_decls",help="name of the target declaration file",default="declarations.pk")
    parser.add_argument("-R","--result_nondecls",help="name of the target non-declaration file",default="non_declarations.pk")
    args = parser.parse_args()
    
    path_unmangled = os.path.join(args.data_dir,args.src_unmangled)
    path_mangled = os.path.join(args.data_dir,args.src_mangled)
    path_decls = os.path.join(args.data_dir,args.result_decls)
    path_nondecls = os.path.join(args.data_dir,args.result_nondecls)

    if not os.path.exists(args.data_dir):
        os.mkdir(args.data_dir,777)

    with open(path_unmangled,'r') as src_file, open(path_mangled,'r') as src_mangled_file:
        with open(path_decls,'wb') as decl_file, open(path_nondecls,'wb') as non_decl_file:
            decl_result,nondecl_result = preprocess(src_file,src_mangled_file)
            pickle.dump(decl_result,decl_file)
            pickle.dump(nondecl_result,non_decl_file)


if __name__ == '__main__':
    main()

