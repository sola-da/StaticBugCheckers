'''

Created on Nov. 30, 2017

@author Andrew Habib

'''

import json
import os
import sys

from Util import load_parsed_ep, CustomEncoder


def match_ep_msg_no_lines(msg, msgs):
    for msg2 in msgs:
        if (msg.proj == msg2.proj and msg.cls == msg2.cls and
            msg.typ == msg2.typ and msg.cat == msg2.cat and
            msg.msg == msg2.msg and msg.code == msg2.code):
        
            return True
        
    return False


def get_removed_warnings_ep(ep_b, ep_f):
    removed_warnings = []
    for b_msg in ep_b:
        if not match_ep_msg_no_lines(b_msg, ep_f):
            removed_warnings.append(b_msg)
    
    return removed_warnings


if __name__ == '__main__':
    
    """Get errors/warnings that disappeared in fixed versions"""
    
    ep_file = os.path.join(os.getcwd(), sys.argv[1])
    ep_res_b = load_parsed_ep(ep_file)
      
    ep_file = os.path.join(os.getcwd(), sys.argv[2])
    ep_res_f = load_parsed_ep(ep_file)
      
    warnings = get_removed_warnings_ep(ep_res_b, ep_res_f)
    
    output_file_name = "ep_removed_warnings.json"
    with open(output_file_name, "w") as file:
        json.dump(warnings, file, cls=CustomEncoder, indent=4)
