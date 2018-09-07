'''

Created on Dec. 28, 2017

@author Andrew Habib

'''

import json
import os
import sys

from Util import JsonDataReader, InferIssue, InferMsg, CustomEncoder, \
                get_cls_name_from_file_path, NO_WARNING


def parse_infer_json_output(proj, json_issue):
    # Case where report file is NOT empty 
    if json_issue:
        issue = InferIssue(*list(json_issue[k] for k in InferIssue.keys))
        cls = get_cls_name_from_file_path(issue.file) 
        lines = extract_lines_from_issue(issue)
        infer_msg = InferMsg(proj, cls, issue.bug_class, issue.kind, issue.bug_type, issue.qualifier,
                             issue.severity, issue.visibility, lines, issue.procedure)
    # Case where report file is empty
    else:
        infer_msg = InferMsg(proj, "", "", "", NO_WARNING, "", "", "", "", "")
    return infer_msg
    

def extract_lines_from_issue(issue):
    src_file = issue.file
    trace_lines = []
    trace_lines.append(issue.line)
    for t in issue.bug_trace:
        if t.filename == src_file:
            trace_lines.append(t.line)
    return set(trace_lines)

    
'''
Takes only one argument: path to infer json files
'''

if __name__ == '__main__':
    
    location_to_data = os.path.join(os.getcwd(), sys.argv[1])
    list_of_data = sorted(os.listdir(location_to_data))
    
    data_paths = list(map(lambda f: os.path.join(location_to_data, f), list_of_data))

    parsed_reports_per_project = []
    
    for proj, json_issue in JsonDataReader(data_paths):
        msg = parse_infer_json_output(proj, json_issue)
        if msg:
            parsed_reports_per_project.append(msg)
        
#     time_stamp = time.strftime("%Y%m%d-%H%M%S")
    time_stamp = ''
    parsed_output_file_name = "inf_parsed" + time_stamp + ".json"
    with open(parsed_output_file_name, "w") as file:
        json.dump(parsed_reports_per_project, file, cls=CustomEncoder, indent=4)
