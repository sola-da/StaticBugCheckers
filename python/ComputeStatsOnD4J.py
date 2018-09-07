'''

Created on Jan. 24, 2018

@author Andrew Habib

'''

import os
import re
import sys
import subprocess
import numpy

from joblib.parallel import delayed, Parallel

from collections import Counter

from Util import load_parsed_ep, load_parsed_inf, load_parsed_sb

def how_many_warnings_per_bug(warnings):
    bugs = [w.proj for w in warnings]
    return(Counter(bugs))

def get_files_locs_diffs_per_bug(proj_b, proj_f):
    with open(os.path.join(proj_b, 'prop-source-dir')) as file:
        src_dir = file.readline()
    
    with open(os.path.join(proj_b, 'prop-buggy-classes')) as file:
        changed_classes = file.read().splitlines()
        changed_files = map(lambda f: os.path.join(src_dir, f.replace('.', '/') + '.java'), changed_classes)
            
    pattern_loc = re.compile("Java +([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+)")
    pattern_mod = re.compile("modified +([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+)")
    pattern_new = re.compile("added +([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+)")
    pattern_del = re.compile("removed +([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+)")
    
    proj = os.path.split(proj_b)[1]
    loc = []
    diff = []

    for _, changed_file in zip(changed_classes, changed_files):
        buggy_file_name = os.path.join(proj_b, changed_file)
        fixed_file_name = os.path.join(proj_f, changed_file)
#         print(buggy_file_name)
#         print(fixed_file_name)
        
        cmd = cloc + ' ' + buggy_file_name
        out, _ = subprocess.Popen(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE).communicate()
        loc.append(int(pattern_loc.search(out).groups()[3]))
#         print(out)
#         print(pattern_loc.search(out).groups()[3])
        
        cmd = cloc + ' --diff ' + buggy_file_name + ' ' + fixed_file_name
        out, _ = subprocess.Popen(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE).communicate()
        diff.append(int(pattern_mod.search(out).groups()[3]) + int(pattern_new.search(out).groups()[3]) + int(pattern_del.search(out).groups()[3]))
#         print(out)
#         print(pattern_mod.search(out).groups()[3])
#         print(pattern_new.search(out).groups()[3])
#         print(pattern_del.search(out).groups()[3])
#         input("")

    return proj, len(changed_classes), sum(loc), sum(diff)

    
if __name__ == '__main__':
    
    ''' Aggregated numbers of modified files, LoCs, diff-size '''
    
    location_to_d4j_b = os.path.join(os.getcwd(), sys.argv[1])
    location_to_d4j_f = os.path.join(os.getcwd(), sys.argv[2])
    cloc = os.path.join(os.getcwd(), sys.argv[3])

    list_d4j_b = sorted(os.listdir(location_to_d4j_b))
    list_d4j_f = sorted(os.listdir(location_to_d4j_f))
     
    list_d4j_b = list(map(lambda f: os.path.join(location_to_d4j_b, f), list_d4j_b))
    list_d4j_f = list(map(lambda f: os.path.join(location_to_d4j_f, f), list_d4j_f))
 
    out = Parallel(n_jobs=30)(delayed(get_files_locs_diffs_per_bug)
                        (proj_b, proj_f)
                            for proj_b, proj_f in zip(list_d4j_b, list_d4j_f))
    projects, files, locs, diffs = zip(*out)
    

    print("\nBins of # of modified files\n")    
    bin_files = Counter(files)
    for (k,v) in bin_files.items():
        print(k,v)
    
    print("\nBins of LoC\n")
    hist, edges = numpy.histogram(locs, [1, 100, 1000, 2000, 3000, 4000, 5000, 10000, 20000])
    for i in range(len(hist)):
        print(edges[i], edges[i+1]-1, hist[i])
    
    print("\nMin and Max of LoC per bug", min(locs), max(locs))
    
    print("\nSum of all LoC of all bugs", sum(locs))
    
    print("\nBins of Diffs\n")
    hist, edges = numpy.histogram(diffs, [1, 5, 10, 15, 20, 25, 50, 75, 100, 200, 2000])
    for i in range(len(hist)):
        print(edges[i], edges[i+1]-1, hist[i])
        
    print("\nMin and Max of diff per bug", min(diffs), max(diffs))
    
    
    ''' D4J stats per bug per tool '''
        
    print("\nStats per bug\n")
    ep_all_b = load_parsed_ep('./b/ep_parsed.json')
    ep_b = how_many_warnings_per_bug(ep_all_b)
    ep_all_f = load_parsed_ep('./f/ep_parsed.json')
    ep_f = how_many_warnings_per_bug(ep_all_f)
    
    inf_all_b = load_parsed_inf('./b/inf_parsed.json')
    inf_b = how_many_warnings_per_bug(inf_all_b)
    inf_all_f = load_parsed_inf('./f/inf_parsed.json')
    inf_f = how_many_warnings_per_bug(inf_all_f)
    
    sb_all_b = load_parsed_sb('./b/sb_parsed.json')
    sb_b = how_many_warnings_per_bug(sb_all_b)
    sb_all_f = load_parsed_sb('./f/sb_parsed.json')
    sb_f = how_many_warnings_per_bug(sb_all_f)
    
    print("Bug Files LoC Diff Ep Inf Sb (from buggy versions)")
    for (p, f, l, d) in out:
        print(p, f, l, d, 
              ep_b[p], inf_b[p], sb_b[p])
