'''

Created on Nov. 30, 2017

@author Andrew Habib

'''

import json
import os
import sys

from Util import load_parsed_sb, CustomEncoder


def match_sb_msg_no_lines(msg, msgs):
    for msg2 in msgs:
        if (msg.proj == msg2.proj and msg.cls == msg2.cls and
            msg.cat == msg2.cat and msg.abbrev == msg2.abbrev and 
            msg.typ == msg2.typ and msg.prio == msg2.prio and
            msg.rank == msg2.rank and msg.msg == msg2.msg and
            msg.mth == msg2.mth and msg.field == msg2.field):
        
            return True
        
    return False


def get_removed_warnings_sb(sb_b, sb_f):
    removed_warnings = []
    for b_msg in sb_b:
        if not match_sb_msg_no_lines(b_msg, sb_f):
            removed_warnings.append(b_msg)
            
    return removed_warnings


if __name__ == '__main__':
    
    """Get errors/warnings that disappeared in fixed versions"""

    sb_file = os.path.join(os.getcwd(), sys.argv[1])
    sb_res_b = load_parsed_sb(sb_file)
       
    sb_file = os.path.join(os.getcwd(), sys.argv[2])
    sb_res_f = load_parsed_sb(sb_file)
       
    warnings = get_removed_warnings_sb(sb_res_b, sb_res_f)

    output_file_name = "sb_removed_warnings.json"
    with open(output_file_name, "w") as file:
        json.dump(warnings, file, cls=CustomEncoder, indent=4)
