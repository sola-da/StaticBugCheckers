'''

Created on Dec. 15, 2017

@author Andrew Habib

'''

import os
import subprocess
import sys

from joblib import Parallel, delayed


def try_compile(proj, path, d4j_binary):
    print()
    print("Trying to compile:", proj)
    print()
    
    proj_dir = os.path.join(path, proj)

    os.chdir(proj_dir)
    
    # Compiling using the build-in d4j compile command
    # Moved to Checkoutd4j.
#     cmd = [d4j_binary, 'compile']
#     p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#     p.communicate()
#     print(proj, p.returncode)
    
    # Compiling using brute-force, trying different compilation commands
    cmd1 = ['ant', 'compile']
    cmd2 = ['mvn', 'compile']
    cmd3 = ['gradle', 'build']
    
    p = subprocess.Popen(cmd1, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    p.communicate()
    print(proj, p.returncode)
    
    p = subprocess.Popen(cmd2, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    p.communicate()
    print(proj, p.returncode)
    
    p = subprocess.Popen(cmd3, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    p.communicate()
    print(proj, p.returncode)    


if __name__ == '__main__':
    
    path_d4j_projects = str(sys.argv[1])
    path_d4j = str(sys.argv[2])
    jobs = int(sys.argv[3])
    
    d4j_binary = os.path.join(path_d4j, 'framework/bin/defects4j')
    projects = sorted(os.listdir(path_d4j_projects))
    
    # Use a cmd filter to debug specific projects
    is_filter = False
    if len(sys.argv) > 3:
        is_filter = True
        with open(sys.argv[3]) as file:
            filter_list = file.read().splitlines()
    if is_filter:
        projects = sorted(list(i for i in projects if i in filter_list))

    Parallel(n_jobs=jobs)(delayed(try_compile)
                          (p, path_d4j_projects, d4j_binary)
                          for p in projects)
    
