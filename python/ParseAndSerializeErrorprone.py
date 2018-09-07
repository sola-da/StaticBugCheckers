'''

Created on Nov. 23, 2017

@author Andrew Habib

'''

import json
import os
import re
import sys

from Util import DataReader, ErrorproneMsg, CustomEncoder, \
                get_cls_name_from_file_path, NO_WARNING

'''
Currently, the errorprone output files may contain 
analysis results of more than one .java file.
This happens in cases where analyzed bug involves 
more than one .java file.
'''


def parse_errorprone_output(proj, report):
    pattern_raw_message = re.compile("^((/[^/ ]*)+/?):([0-9]+): (warning|error): \[([a-zA-Z]+)\] (.*)")
        
    reports = []
    
    # Case where report file is empty 
    if len(report) == 0:
        reports.append(ErrorproneMsg(proj, "", "", NO_WARNING, "", "", "", -1))
        return reports
    
    # Case where report file is NOT empty
    i = 0
    while i < len(report):
        line = report[i]        
        match = pattern_raw_message.match(line)
        
        if match:
            raw_message = match.groups()[0:6]
        
            cls_path = raw_message[0]
            cls = get_cls_name_from_file_path(cls_path)
#             if '/com/' in cls_path:
#                 cls = 'com.' + cls_path.split('/com/')[1].replace('/', '.').replace('.java', '')
#             elif '/org/' in cls_path:
#                 cls = 'org.' + cls_path.split('/org/')[1].replace('/', '.').replace('.java', '')
            
            line = raw_message[2]
            typ = raw_message[3]
            cat = raw_message[4]
            msg = raw_message[5]
            code = report[i + 1].replace('\n', '')
            mark = report[i + 2].replace('\n', '')
        
            parsed_msg = ErrorproneMsg(proj, cls, typ, cat, msg, code, mark, line)
            reports.append(parsed_msg)

            i += 3
        else:
            i += 1

    return reports
        

'''
Takes only one argument: path to errorprone raw data
'''    

if __name__ == '__main__':
    
    location_to_data = os.path.join(os.getcwd(), sys.argv[1])
    list_of_data = sorted(os.listdir(location_to_data))
    
    data_paths = list(map(lambda f: os.path.join(location_to_data, f), list_of_data))

    parsed_reports_per_project = []
    
    for proj, report in DataReader(data_paths):
        parsed_reports_per_project.extend(parse_errorprone_output(proj, report))
            
#     time_stamp = time.strftime("%Y%m%d-%H%M%S")
    time_stamp = ''
    parsed_output_file_name = "ep_parsed" + time_stamp + ".json"
    with open(parsed_output_file_name, "w") as file:
        json.dump(parsed_reports_per_project, file, cls=CustomEncoder, indent=4)
