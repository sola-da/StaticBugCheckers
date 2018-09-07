'''

Created on Nov. 30, 2017

@author Andrew Habib

'''

import json
import os
import sys

from Util import load_parsed_diffs, load_parsed_sb, find_msg_by_proj_and_cls, \
                LineMatchesToMessages, CustomEncoder


def match_diff_sb(d, sb_list):
    matches = []
    lines_matches = []
    for inst in sb_list:
        sb_lines = inst.unrollLines()
        if d.lines.intersection(sb_lines):
            matches.append(inst)
            lines_matches.extend(d.lines.intersection(sb_lines))
    return matches, set(lines_matches)


def get_hits_diffs_sb(diffs, sb_res):
    sb_count = 0    
    sb_all_matches = []
    diffs_match_sb = []
    for d in diffs:
        
        proj = d.proj
        cls = d.cls
        
        sb_list = find_msg_by_proj_and_cls(proj, cls, sb_res)
        diff_sb, lines = match_diff_sb(d, sb_list)
        if diff_sb:
            sb_count += len(diff_sb)
            sb_all_matches.append(LineMatchesToMessages(lines, diff_sb))
            diffs_match_sb.extend(diff_sb)

#     print(sb_count)

#     return sb_all_matches
    return diffs_match_sb


if __name__ == '__main__':

    """Get lines matches between each tool and  bug fixes diffs"""

    diffs_file = os.path.join(os.getcwd(), sys.argv[1])
    diffs = load_parsed_diffs(diffs_file)
      
    sb_file = os.path.join(os.getcwd(), sys.argv[2])
    sb_res = load_parsed_sb(sb_file)
  
    diffs_sb = get_hits_diffs_sb(diffs, sb_res)

    output_file_name = "sb_diffs_warnings.json"
    with open(output_file_name, "w") as file:
        json.dump(diffs_sb, file, cls=CustomEncoder, indent=4)
