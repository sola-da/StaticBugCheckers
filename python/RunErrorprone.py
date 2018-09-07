'''

Created on Dec. 15, 2017

@author Andrew Habib

'''

import os
import subprocess
import sys

from joblib import Parallel, delayed

from Util import prepare_tool


def run_ep_on_proj(proj, path, path_out, path_ep):
    log = open(os.path.join(os.getcwd(), 'ep_log'), 'a')

    log.write("Running Errorprone on: " + proj + "\n\n")
            
    _, proj_cp, proj_javac_opts, proj_buggy_files, _ = prepare_tool(path, proj)
    
    f = open(os.path.join(path_out, proj), 'w')
    for buggy_f in proj_buggy_files:
        cmd = ['java', '-Xbootclasspath/p:' + path_ep,
               'com.google.errorprone.ErrorProneCompiler',
               '-implicit:none'] 
        if proj_javac_opts:
            cmd = cmd + proj_javac_opts.split(' ') + ['-cp', proj_cp, buggy_f]
        else:
            cmd = cmd + ['-cp', proj_cp, buggy_f]
        
        log.write(" ".join(cmd) + "\n\n")
        
        p = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (cmd_out, _) = p.communicate()
        
        f.write(cmd_out)
        
        log.write(cmd_out + "\n")
        log.write("*"*24 + "\n\n")        

    log.write("#"*212 + "\n\n")
    log.close()
        

if __name__ == '__main__':
    path_ep = os.path.join(os.getcwd(), sys.argv[1])
    path_d4j_projects = os.path.join(os.getcwd(), sys.argv[2])
    jobs = int(sys.argv[3])
    
    path_out = os.path.join(os.getcwd(), 'ep_output')
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
        
    Parallel(n_jobs=jobs)(delayed(run_ep_on_proj)
                          (p, path_d4j_projects, path_out, path_ep)
                          for p in projects)
