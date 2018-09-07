'''

Created on Jan. 4, 2018

@author Andrew Habib

'''

import json
import os
import sys

from Util import load_parsed_diffs, load_parsed_inf, find_msg_by_proj_and_cls, \
                LineMatchesToMessages, CustomEncoder


def match_diff_inf(d, inf_list):
    matches = []
    lines_matches = []
    for inst in inf_list:
        for l in inst.lines:
            if l in d.lines:
                matches.append(inst)
                lines_matches.append(l)
                break
    return matches, set(lines_matches)


def get_hits_diffs_inf(diffs, inf_res):
    inf_count = 0
    inf_all_matches = []
    diffs_match_inf = []
    for d in diffs:
        
        proj = d.proj
        cls = d.cls
        
        ep_list = find_msg_by_proj_and_cls(proj, cls, inf_res)
        diff_inf, lines = match_diff_inf(d, ep_list)
        if diff_inf:
            inf_count += len(diff_inf)
            inf_all_matches.append(LineMatchesToMessages(lines, diff_inf))
            diffs_match_inf.extend(diff_inf)

#     print(inf_count)

#     return inf_all_matches
    return diffs_match_inf


if __name__ == '__main__':

    """Get lines matches between each tool and  bug fixes diffs"""

    diffs_file = os.path.join(os.getcwd(), sys.argv[1])
    diffs = load_parsed_diffs(diffs_file)
      
    inf_file = os.path.join(os.getcwd(), sys.argv[2])
    inf_res = load_parsed_inf(inf_file)
  
    diffs_inf = get_hits_diffs_inf(diffs, inf_res)

    output_file_name = "inf_diffs_warnings.json"
    with open(output_file_name, "w") as file:
        json.dump(diffs_inf, file, cls=CustomEncoder, indent=4)
