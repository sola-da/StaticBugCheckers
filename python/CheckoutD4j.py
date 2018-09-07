'''

Created on Dec. 15, 2017

@author Andrew Habib

'''

import os
import subprocess
import sys

from joblib import Parallel, delayed


def exec_cmd(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def check_out_each_project(d4j_binary, dist, proj, ver, ver_type):
    print("Checkingout:", proj, ver, ver_type)
    ver = str(ver)
    proj_dist = dist + '/' + proj + '-' + ver
    
    cmd = [d4j_binary, 'checkout', '-p', proj, '-v', ver + ver_type, '-w', proj_dist]
    exec_cmd(cmd)
    
    print("Getting properties:", proj, ver, ver_type)
    os.chdir(proj_dist)
    
    cmd = [d4j_binary, 'export', '-p', 'classes.modified', '-o', 'prop-buggy-classes']
    exec_cmd(cmd)
 
    cmd = [d4j_binary, 'export', '-p', 'dir.src.classes', '-o', 'prop-source-dir']
    exec_cmd(cmd)
 
    cmd = [d4j_binary, 'export', '-p', 'cp.compile', '-o', 'prop-compile-path']
    exec_cmd(cmd)

    print("Compiling:", proj, ver, ver_type)
    cmd = [d4j_binary, 'compile']
    exec_cmd(cmd)

if __name__ == '__main__':
    
    path_d4j = sys.argv[1] if sys.argv[1].startswith("/") else os.path.join(os.getcwd(), sys.argv[1])
    ver_type = sys.argv[2]
    jobs = int(sys.argv[3])
    
    d4j_binary = os.path.join(path_d4j, 'framework/bin/defects4j')
    dist = os.path.join(path_d4j, 'projects', ver_type)
    
    print(dist)
    if not os.path.isdir(dist):
        os.makedirs(dist)
        
    projects = {
        'Chart': 26,
        'Closure': 133,
        'CommonsCodec': 22,
        'CommonsCLI': 24,
        'CommonsCsv': 12,
        'CommonsJXPath': 14,
        'Guava': 9,
        'JacksonCore': 13,
        'JacksonDatabind': 39,
        'JacksonXml': 5,
        'Jsoup': 64,
        'Lang': 65,
        'Math': 106,
        'Mockito': 38,
        'Time': 27
        }
    
    Parallel(n_jobs=jobs)(delayed(check_out_each_project)
                          (d4j_binary, dist, proj, ver, ver_type) 
                            for proj, count in projects.items() 
                            for ver in range(1, count + 1))
