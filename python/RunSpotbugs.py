'''

Created on Dec. 15, 2017

@author Andrew Habib

'''

import os
import subprocess
import sys

from joblib import Parallel, delayed

from Util import prepare_tool


def run_sb_on_proj(proj, path, path_out, path_sb):
    log = open(os.path.join(os.getcwd(), 'sb_log'), 'a')

    log.write("Runnning SpotBugs on: " + proj + "\n\n")

    proj_src, proj_cp, proj_javac_opts, proj_buggy_files, proj_buggy_classes = prepare_tool(path, proj)
    
    for buggy_f in proj_buggy_files:
        if proj_javac_opts:
            cmd = ['javac'] + proj_javac_opts.split(' ') + ['-cp', proj_cp, buggy_f]
        else:
            cmd = ['javac'] + ['-cp', proj_cp, buggy_f]
        
        log.write(" ".join(cmd) + "\n\n")
        
        p = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out, _) = p.communicate()
        
        log.write(out + "\n")
        log.write("*"*24 + "\n\n")
        
    cmd = ['java', '-jar', path_sb,
               '-textui', '-xml:withMessages',
               '-output', os.path.join(path_out, proj) + '.xml',
               '-auxclasspath', proj_cp,
               '-onlyAnalyze', ','.join(cl for cl in proj_buggy_classes),
               proj_src]
    
    log.write(" ".join(cmd) + "\n\n")
    
    p = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out, _) = p.communicate()
    
    log.write(out + "\n")
    
    log.write("#"*212 + "\n\n")
    log.close()
    

if __name__ == '__main__':
    path_sb = os.path.join(os.getcwd(), sys.argv[1])
    path_d4j_projects = os.path.join(os.getcwd(), sys.argv[2])
    jobs = int(sys.argv[3])
    
    path_out = os.path.join(os.getcwd(), 'sb_output')
    if not os.path.isdir(path_out):
        os.makedirs(path_out)
    
    projects = sorted(os.listdir(path_d4j_projects))
    
    # Use a cmd is_filter to debug specific projects
    is_filter = False
    if len(sys.argv) > 4:
        is_filter = True
        with open(sys.argv[4]) as file:
            filter_list = file.read().splitlines()
    if is_filter:
        projects = sorted(list(i for i in projects if i in filter_list))

    Parallel(n_jobs=jobs)(delayed(run_sb_on_proj)
                          (p, path_d4j_projects, path_out, path_sb)
                          for p in projects)
