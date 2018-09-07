'''

Created on Nov. 29, 2017

@author Andrew Habib

'''

import json
import os
import subprocess
import sys

from Util import FileDiff, CustomEncoder


def compute_proj_diff(proj_b, proj_f):
    with open(os.path.join(proj_b, 'prop-source-dir')) as file:
        src_dir = file.readline()
    
    with open(os.path.join(proj_b, 'prop-buggy-classes')) as file:
        changed_classes = file.read().splitlines()
        changed_files = map(lambda f: os.path.join(src_dir, f.replace('.', '/') + '.java'), changed_classes)
    
    file_diffs = []
    
    proj = os.path.split(proj_b)[1]
    for changed_class, changed_file in zip(changed_classes, changed_files):
        buggy_file_name = os.path.join(proj_b, changed_file)
        fixed_file_name = os.path.join(proj_f, changed_file)
        print(buggy_file_name)
        print(fixed_file_name)
        
        '''
        Get modified or deleted lines from old file
        '''
        command = 'diff --unchanged-line-format="" --old-line-format="%dn\n" --new-line-format="" ' + buggy_file_name + ' ' + fixed_file_name
        out, _ = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE).communicate()
        mod_or_del_lines = set(map(lambda l: int(l), list(out.split('\n')[:-1])))

        '''
        Get new lines inserted in new files; but it also returns modified lines as new lines
        '''
        command = 'diff --unchanged-line-format="" --old-line-format="" --new-line-format="%dn\n" ' + buggy_file_name + ' ' + fixed_file_name
        out, _ = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE).communicate()
        new_lines = set(map(lambda l: int(l), list(out.split('\n')[:-1])))

        '''
        Compute set difference before approximating true_new_lines to exclude modified lines
        '''
        true_new_lines = new_lines.difference(mod_or_del_lines)

        '''old changed lines'''
#             changed_lines.extend(mod_or_del_lines).extend(new_lines)            
        
        '''
        changed_lines is approximation of inserted(new) lines 
        and deleted or modified lines
        '''
        approx_lines = set([line + i for line in true_new_lines for i in [-1,0, 1]])

        changed_lines = sorted(approx_lines.union(mod_or_del_lines))

        file_diff = FileDiff(proj, changed_class, changed_lines)
        file_diffs.append(file_diff)

    return file_diffs


'''
Takes two arguments: paths to d4j buggy and fixed projects 
in this order: buggy_path fixed_path
'''    

if __name__ == '__main__':
    
    location_to_d4j_b = os.path.join(os.getcwd(), sys.argv[1])
    location_to_d4j_f = os.path.join(os.getcwd(), sys.argv[2])
    
    list_d4j_b = sorted(os.listdir(location_to_d4j_b))
    list_d4j_f = sorted(os.listdir(location_to_d4j_f))
    
    list_d4j_b = list(map(lambda f: os.path.join(location_to_d4j_b, f), list_d4j_b))
    list_d4j_f = list(map(lambda f: os.path.join(location_to_d4j_f, f), list_d4j_f))
    
    parsed_projects_diffs = []
        
    for proj_b, proj_f in zip(list_d4j_b, list_d4j_f):
        parsed_projects_diffs.extend(compute_proj_diff(proj_b, proj_f))
         
#     time_stamp = time.strftime("%Y%m%d-%H%M%S")
#     time_stamp = ''
#     parsed_output_file_name = "diffs_parserd_" + time_stamp + ".json"
    parsed_output_file_name = "diffs_parsed" + ".json"
    with open(parsed_output_file_name, "w") as file:
        json.dump(parsed_projects_diffs, file, cls=CustomEncoder, indent=4)
        
