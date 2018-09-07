'''

Created on Jan. 24, 2018

@author Andrew Habib

'''

from statistics import mean
from collections import Counter
import os 

from Util import load_parsed_ep, load_parsed_inf, load_parsed_sb, load_json_list, get_list_of_uniq_jsons


def display_min_max_avg_warnings_per_bug_total():
    print("\nMin, Max, Avg (warnings per bug) and Total number of warnings")
    print("\nBuggy versions:\n")
    rel_path = './b/'
    ep_all = load_parsed_ep(rel_path + 'ep_parsed.json')
    inf_all = load_parsed_inf(rel_path + 'inf_parsed.json')
    sb_all = load_parsed_sb(rel_path + 'sb_parsed.json')
    print("Tool Min. Max. Avg. Total")
    print("Errorprone", get_min_max_avg_warnings_per_bug_total(ep_all))
    print("Infer", get_min_max_avg_warnings_per_bug_total(inf_all))
    print("Spotbugs", get_min_max_avg_warnings_per_bug_total(sb_all))
    print("\nTotal number of warnings by all tools:",
          get_min_max_avg_warnings_per_bug_total(ep_all)[3] + get_min_max_avg_warnings_per_bug_total(inf_all)[3] + get_min_max_avg_warnings_per_bug_total(sb_all)[3])
    ''''''
    print("\nFixed versions:\n")
    rel_path = './f/'
    ep_all = load_parsed_ep(rel_path + 'ep_parsed.json')
    inf_all = load_parsed_inf(rel_path + 'inf_parsed.json')
    sb_all = load_parsed_sb(rel_path + 'sb_parsed.json')
    print("Tool Total Min. Max. Avg.")
    print("Errorprone", get_min_max_avg_warnings_per_bug_total(ep_all))
    print("Infer", get_min_max_avg_warnings_per_bug_total(inf_all))
    print("Spotbugs", get_min_max_avg_warnings_per_bug_total(sb_all))
    print("\nTotal number of warnings by all tools:",
          get_min_max_avg_warnings_per_bug_total(ep_all)[3] + get_min_max_avg_warnings_per_bug_total(inf_all)[3] + get_min_max_avg_warnings_per_bug_total(sb_all)[3])


def get_min_max_avg_warnings_per_bug_total(warnings):
    count = [w.proj for w in warnings]
    counter = Counter(count)
    return min(counter.values()), max(counter.values()), mean(counter.values()), len(count)


def get_warnings_bugs_from_each_approach():
    print("\nWarnings and bugs from each automatic matching approach")
    print("** warnings for combined approach are not unique (duplicates exist) **\n")
    rel_path = './diffs_warnings/'
    ep_res1 = load_parsed_ep(rel_path + "ep_warnings.json") 
    inf_res1 = load_parsed_inf(rel_path + "inf_warnings.json")
    sb_res1 = load_parsed_sb(rel_path + "sb_warnings.json")
    rel_path = './removed_warnings/'
    ep_res2 = load_parsed_ep(rel_path + "ep_warnings.json")
    inf_res2 = load_parsed_inf(rel_path + "inf_warnings.json")
    sb_res2 = load_parsed_sb(rel_path + "sb_warnings.json")
    _all_b = []
    print("Tool Diff-based Fixed-based Combined")
    print("     W        B W         B W      B")
    all_b = []
    b_diff = get_bugs_from_warnings(ep_res1)
    b_fixed = get_bugs_from_warnings(ep_res2)
    all_b.extend(b_diff)
    all_b.extend(b_fixed)
    _all_b.extend(all_b)
    print("Error Prone   ", len(ep_res1), len(b_diff), len(ep_res2), len(b_fixed), len(ep_res1) + len(ep_res2), len(b_diff | b_fixed))
 
    all_b = []
    b_diff = get_bugs_from_warnings(inf_res1)
    b_fixed = get_bugs_from_warnings(inf_res2)
    all_b.extend(b_diff)
    all_b.extend(b_fixed)
    _all_b.extend(all_b)
    print("Infer         ", len(inf_res1), len(b_diff), len(inf_res2), len(b_fixed), len(inf_res1) + len(inf_res2), len(b_diff | b_fixed))
    
    all_b = []
    b_diff = get_bugs_from_warnings(sb_res1)
    b_fixed = get_bugs_from_warnings(sb_res2)
    all_b.extend(b_diff)
    all_b.extend(b_fixed)
    _all_b.extend(all_b)
    print("SpotBugs      ", len(sb_res1), len(b_diff), len(sb_res2), len(b_fixed), len(sb_res1) + len(sb_res2), len(b_diff | b_fixed))
    
    print("\nUnique warnings from each approachcombined approach:\n")
    rel_path = './diffs_warnings/'
    ep_res1 = load_json_list(rel_path + "ep_warnings.json") 
    inf_res1 = load_json_list(rel_path + "inf_warnings.json")
    sb_res1 = load_json_list(rel_path + "sb_warnings.json")    
    rel_path = './removed_warnings/'
    ep_res2 = load_json_list(rel_path + "ep_warnings.json")
    inf_res2 = load_json_list(rel_path + "inf_warnings.json")
    sb_res2 = load_json_list(rel_path + "sb_warnings.json")
    
    print("Ep ", len(ep_res1), len(ep_res2), len(get_list_of_uniq_jsons(ep_res1 + ep_res2)))
    print("Inf", len(inf_res1), len(inf_res2), len(get_list_of_uniq_jsons(inf_res1 + inf_res2)))
    print("Sb ", len(sb_res1), len(sb_res2), len(get_list_of_uniq_jsons(sb_res1 + sb_res2)))

    print("\nUnique bugs from combined approach: ", len(set(_all_b)))


def get_bugs_from_warnings(warnings):
    bugs = set(w.proj for w in warnings)
    return bugs


def count_bugs_from_warnings(warnings):
    bugs = set(w.proj for w in warnings)
    return(len(bugs))


def get_manually_inspected_warnings_bugs():
    print("\nManual inspection of warnings aggregated on warnings and bugs levels")
    print("\nDiffs-based approach:\n")
    rel_path = './diffs_warnings/'
    ep_res = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part = load_parsed_ep(rel_path + "ep_part.json")
    ep_fail = load_parsed_ep(rel_path + "ep_fail.json")
    inf_res = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part = load_parsed_inf(rel_path + "inf_part.json")
    inf_fail = load_parsed_inf(rel_path + "inf_fail.json")
    sb_res = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part = load_parsed_sb(rel_path + "sb_part.json")
    sb_fail = load_parsed_sb(rel_path + "sb_fail.json")
    print("Warnings:\n")
    print('Tool "Full match" "Partial match" Mismatch Total')
    print('"Error Prone"', len(ep_succ), len(ep_part), len(ep_fail), len(ep_res))
    print("Infer", len(inf_succ), len(inf_part), len(inf_fail), len(inf_res))
    print("Spotbugs", len(sb_succ), len(sb_part), len(sb_fail), len(sb_res))
    print("\nBugs:\n")
    print('Tool "Full match" "Partial match" Mismatch Total')
    print('"Error Prone"', count_bugs_from_warnings(ep_succ), count_bugs_from_warnings(ep_part), count_bugs_from_warnings(ep_fail), count_bugs_from_warnings(ep_res))
    print("Infer", count_bugs_from_warnings(inf_succ), count_bugs_from_warnings(inf_part), count_bugs_from_warnings(inf_fail), count_bugs_from_warnings(inf_res))
    print("Spotbugs", count_bugs_from_warnings(sb_succ), count_bugs_from_warnings(sb_part), count_bugs_from_warnings(sb_fail), count_bugs_from_warnings(sb_res))

    print("\nFixed warnings approach\n")
    rel_path = './removed_warnings/'
    ep_res = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part = load_parsed_ep(rel_path + "ep_part.json")
    ep_fail = load_parsed_ep(rel_path + "ep_fail.json")
    inf_res = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part = load_parsed_inf(rel_path + "inf_part.json")
    inf_fail = load_parsed_inf(rel_path + "inf_fail.json")
    sb_res = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part = load_parsed_sb(rel_path + "sb_part.json")
    sb_fail = load_parsed_sb(rel_path + "sb_fail.json")
    print("Warnings:\n")
    print('Tool "Full match" "Partial match" Mismatch Total')
    print('"Error Prone"', len(ep_succ), len(ep_part), len(ep_fail), len(ep_res))
    print("Infer", len(inf_succ), len(inf_part), len(inf_fail), len(inf_res))
    print("Spotbugs", len(sb_succ), len(sb_part), len(sb_fail), len(sb_res))
    print("\nBugs:\n")
    print('Tool "Full match" "Partial match" Mismatch Total')
    print('"Error Prone"', count_bugs_from_warnings(ep_succ), count_bugs_from_warnings(ep_part), count_bugs_from_warnings(ep_fail), count_bugs_from_warnings(ep_res))
    print("Infer", count_bugs_from_warnings(inf_succ), count_bugs_from_warnings(inf_part), count_bugs_from_warnings(inf_fail), count_bugs_from_warnings(inf_res))
    print("Spotbugs", count_bugs_from_warnings(sb_succ), count_bugs_from_warnings(sb_part), count_bugs_from_warnings(sb_fail), count_bugs_from_warnings(sb_res))

    get_manually_inspected_warnings_bugs_combined_approach()


def get_manually_inspected_warnings_bugs_combined_approach():
    print("\nCombined approach\n")
    rel_path = './diffs_warnings/'
    ep_succ1 = load_json_list(rel_path + "ep_succ.json")
    ep_part1 = load_json_list(rel_path + "ep_part.json")
    ep_fail1 = load_json_list(rel_path + "ep_fail.json")
     
    inf_succ1 = load_json_list(rel_path + "inf_succ.json")
    inf_part1 = load_json_list(rel_path + "inf_part.json")
    inf_fail1 = load_json_list(rel_path + "inf_fail.json")
     
    sb_succ1 = load_json_list(rel_path + "sb_succ.json")
    sb_part1 = load_json_list(rel_path + "sb_part.json")
    sb_fail1 = load_json_list(rel_path + "sb_fail.json")
    
    rel_path = './removed_warnings/'
    ep_succ2 = load_json_list(rel_path + "ep_succ.json")
    ep_part2 = load_json_list(rel_path + "ep_part.json")
    ep_fail2 = load_json_list(rel_path + "ep_fail.json")
     
    inf_succ2 = load_json_list(rel_path + "inf_succ.json")
    inf_part2 = load_json_list(rel_path + "inf_part.json")
    inf_fail2 = load_json_list(rel_path + "inf_fail.json")
     
    sb_succ2 = load_json_list(rel_path + "sb_succ.json")
    sb_part2 = load_json_list(rel_path + "sb_part.json")
    sb_fail2 = load_json_list(rel_path + "sb_fail.json")

    # comnined data #
    ep_succ = get_list_of_uniq_jsons(ep_succ1 + ep_succ2)
    ep_part = get_list_of_uniq_jsons(ep_part1 + ep_part2)
    ep_fail = get_list_of_uniq_jsons(ep_fail1 + ep_fail2)
    
    inf_succ = get_list_of_uniq_jsons(inf_succ1 + inf_succ2)
    inf_part = get_list_of_uniq_jsons(inf_part1 + inf_part2)
    inf_fail = get_list_of_uniq_jsons(inf_fail1 + inf_fail2)
    
    sb_succ = get_list_of_uniq_jsons(sb_succ1 + sb_succ2)
    sb_part = get_list_of_uniq_jsons(sb_part1 + sb_part2)
    sb_fail = get_list_of_uniq_jsons(sb_fail1 + sb_fail2)
    
    print("Warnings:\n")
    print('Tool "Full match" "Partial match" Mismatch Total')
    print('"Error Prone"', len(ep_succ), len(ep_part), len(ep_fail), len(ep_succ) + len(ep_part) + len(ep_fail))
    print('Infer', len(inf_succ), len(inf_part), len(inf_fail), len(inf_succ) + len(inf_part) + len(inf_fail))
    print('SpotBugs', len(sb_succ), len(sb_part), len(sb_fail), len(sb_succ) + len(sb_part) + len(sb_fail))
    
    print("\nBugs:\n")
    print('Tool "Full match" "Partial match" Mismatch Total')
    b_succ, b_part, b_fail = len(Counter(p[' Proj'] for p in ep_succ)), len(Counter(p[' Proj'] for p in ep_part)), len(Counter(p[' Proj'] for p in ep_fail))
    print('"Error Prone"', b_succ, b_part, b_fail, b_succ + b_part + b_fail)
    
    b_succ, b_part, b_fail = len(Counter(p['      Proj'] for p in inf_succ)), len(Counter(p['      Proj'] for p in inf_part)), len(Counter(p['      Proj'] for p in inf_fail))
    print('Infer', b_succ, b_part, b_fail, b_succ + b_part + b_fail)
    
    b_succ, b_part, b_fail = len(Counter(p['    Proj'] for p in sb_succ)), len(Counter(p['    Proj'] for p in sb_part)), len(Counter(p['    Proj'] for p in sb_fail))
    print('SpotBugs', b_succ, b_part, b_fail, b_succ + b_part + b_fail)     


def get_cand_detected_bugs_tools_sets():
    print("\nCandidate and detected bugs by each tool and each approach")
    rel_path = './diffs_warnings/'
    ep_res1 = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ1 = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part1 = load_parsed_ep(rel_path + "ep_part.json")
     
    inf_res1 = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ1 = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part1 = load_parsed_inf(rel_path + "inf_part.json")
     
    sb_res1 = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ1 = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part1 = load_parsed_sb(rel_path + "sb_part.json")
    
    rel_path = './removed_warnings/'
    ep_res2 = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ2 = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part2 = load_parsed_ep(rel_path + "ep_part.json")
     
    inf_res2 = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ2 = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part2 = load_parsed_inf(rel_path + "inf_part.json")
     
    sb_res2 = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ2 = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part2 = load_parsed_sb(rel_path + "sb_part.json")
    
    print("\nCandidate bugs:\n")
    print("Tool Diff-based Fixed-based Both")
    ep_cand_diff = get_bugs_from_warnings(ep_res1)
    ep_cand_fixed = get_bugs_from_warnings(ep_res2)
    print('"Error Prone"', len(ep_cand_diff), len(ep_cand_fixed), len(ep_cand_diff & ep_cand_fixed))
    inf_cand_diff = get_bugs_from_warnings(inf_res1)
    inf_cand_fixed = get_bugs_from_warnings(inf_res2)
    print("Infer", len(inf_cand_diff), len(inf_cand_fixed), len(inf_cand_diff & inf_cand_fixed))
    sb_cand_diff = get_bugs_from_warnings(sb_res1)
    sb_cand_fixed = get_bugs_from_warnings(sb_res2)
    print("Spotbugs", len(sb_cand_diff), len(sb_cand_fixed), len(sb_cand_diff & sb_cand_fixed))
    
    print("\nTrue bugs (fully or partially flagged)\n")
    print("Tool Diff-based Fixed-based Both")
    ep_succ_diff = get_bugs_from_warnings(ep_succ1) | get_bugs_from_warnings(ep_part1)
    ep_succ_fixed = get_bugs_from_warnings(ep_succ2) | get_bugs_from_warnings(ep_part2)
    print('"Error Prone"', len(ep_succ_diff), len(ep_succ_fixed), len(ep_succ_diff & ep_succ_fixed))
    inf_succ_diff = get_bugs_from_warnings(inf_succ1) | get_bugs_from_warnings(inf_part1)
    inf_succ_fixed = get_bugs_from_warnings(inf_succ2) | get_bugs_from_warnings(inf_part2)
    print("Infer", len(inf_succ_diff), len(inf_succ_fixed), len(inf_succ_diff & inf_succ_fixed))
    sb_succ_diff = get_bugs_from_warnings(sb_succ1) | get_bugs_from_warnings(sb_part1)
    sb_succ_fixed = get_bugs_from_warnings(sb_succ2) | get_bugs_from_warnings(sb_part2)
    print("Spotbugs", len(sb_succ_diff), len(sb_succ_fixed), len(sb_succ_diff & sb_succ_fixed))
    
    print("\nTrue bugs found by all tools\n")
    ep_succ = get_bugs_from_warnings(ep_succ1) | get_bugs_from_warnings(ep_succ2) | get_bugs_from_warnings(ep_part1) | get_bugs_from_warnings(ep_part2)
    print("Ep:", len(ep_succ))
     
    inf_succ = get_bugs_from_warnings(inf_succ1) | get_bugs_from_warnings(inf_succ2) | get_bugs_from_warnings(inf_part1) | get_bugs_from_warnings(inf_part2)
    print("Inf:", len(inf_succ))
     
    sb_succ = get_bugs_from_warnings(sb_succ1) | get_bugs_from_warnings(sb_succ2) | get_bugs_from_warnings(sb_part1) | get_bugs_from_warnings(sb_part2)
    print("Sb:", len(sb_succ))
     
    print("Ep & Inf:", len(ep_succ & inf_succ))
    print("Ep & Sb:", len(ep_succ & sb_succ))
    print("Inf & Sb:", len(inf_succ & sb_succ))
    print("Ep & Inf & Sb:", len(ep_succ & inf_succ & sb_succ))


def get_cand_detected_bugs_tools_table():
    print("\nAll candidate and detected bugs by each tool and each approach\n")
    rel_path = './diffs_warnings/'
    ep_res1 = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ1 = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part1 = load_parsed_ep(rel_path + "ep_part.json")
    ep_fail1 = load_parsed_ep(rel_path + "ep_fail.json")
     
    inf_res1 = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ1 = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part1 = load_parsed_inf(rel_path + "inf_part.json")
    inf_fail1 = load_parsed_inf(rel_path + "inf_fail.json")
     
    sb_res1 = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ1 = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part1 = load_parsed_sb(rel_path + "sb_part.json")
    sb_fail1 = load_parsed_sb(rel_path + "sb_fail.json")
    
    rel_path = './removed_warnings/'
    ep_res2 = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ2 = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part2 = load_parsed_ep(rel_path + "ep_part.json")
    ep_fail2 = load_parsed_ep(rel_path + "ep_fail.json")
     
    inf_res2 = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ2 = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part2 = load_parsed_inf(rel_path + "inf_part.json")
    inf_fail2 = load_parsed_inf(rel_path + "inf_fail.json")
     
    sb_res2 = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ2 = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part2 = load_parsed_sb(rel_path + "sb_part.json")
    sb_fail2 = load_parsed_sb(rel_path + "sb_fail.json")

    bugs = []
    
    bugs.extend(w.proj for w in ep_res1)
    bugs.extend(w.proj for w in inf_res1)
    bugs.extend(w.proj for w in sb_res1)
    
    bugs.extend(w.proj for w in ep_res2)
    bugs.extend(w.proj for w in inf_res2)
    bugs.extend(w.proj for w in sb_res2)
    
    bugs = sorted(list(set(bugs)))
    
    print("        Removed Warnings    Diffs-based         Combined")
    print("Tool       Ep Inf SB         Ep Inf SB          Ep Inf SB")
    for b in bugs:
        entry = b + " "
        #####################################
        if b in get_bugs_from_warnings(ep_succ1):
            entry += "& F "
        elif b in get_bugs_from_warnings(ep_part1):
            entry += "& P "
        elif b in get_bugs_from_warnings(ep_fail1):
            entry += "& M "
        else:
            entry += "& - "
        
        if b in get_bugs_from_warnings(inf_succ1):
            entry += "& F "
        elif b in get_bugs_from_warnings(inf_part1):
            entry += "& P "
        elif b in get_bugs_from_warnings(inf_fail1):
            entry += "& M "
        else:
            entry += "& - "
            
        if b in get_bugs_from_warnings(sb_succ1):
            entry += "& F "
        elif b in get_bugs_from_warnings(sb_part1):
            entry += "& P "
        elif b in get_bugs_from_warnings(sb_fail1):
            entry += "& M "
        else:
            entry += "& - "
        
        #####################################
        if b in get_bugs_from_warnings(ep_succ2):
            entry += "& F "
        elif b in get_bugs_from_warnings(ep_part2):
            entry += "& P "
        elif b in get_bugs_from_warnings(ep_fail2):
            entry += "& M "
        else:
            entry += "& - "
        
        if b in get_bugs_from_warnings(inf_succ2):
            entry += "& F "
        elif b in get_bugs_from_warnings(inf_part2):
            entry += "& P "
        elif b in get_bugs_from_warnings(inf_fail2):
            entry += "& M "
        else:
            entry += "& - "
            
        if b in get_bugs_from_warnings(sb_succ2):
            entry += "& F "
        elif b in get_bugs_from_warnings(sb_part2):
            entry += "& P "
        elif b in get_bugs_from_warnings(sb_fail2):
            entry += "& M "
        else:
            entry += "& - "
        
        #####################################
        if b in get_bugs_from_warnings(ep_succ1) or b in get_bugs_from_warnings(ep_succ2):
            entry += "& F "
        elif b in get_bugs_from_warnings(ep_part1) or b in get_bugs_from_warnings(ep_part2):
            entry += "& P "
        elif b in get_bugs_from_warnings(ep_fail1) or b in get_bugs_from_warnings(ep_fail2):
            entry += "& M "
        else:
            entry += "& - "
        
        if b in get_bugs_from_warnings(inf_succ1) or b in get_bugs_from_warnings(inf_succ2):
            entry += "& F "
        elif b in get_bugs_from_warnings(inf_part1) or b in get_bugs_from_warnings(inf_part2):
            entry += "& P "
        elif b in get_bugs_from_warnings(inf_fail1) or b in get_bugs_from_warnings(inf_fail2):
            entry += "& M "
        else:
            entry += "& - "
            
        if b in get_bugs_from_warnings(sb_succ1) or b in get_bugs_from_warnings(sb_succ2):
            entry += "& F "
        elif b in get_bugs_from_warnings(sb_part1) or b in get_bugs_from_warnings(sb_part2):
            entry += "& P "
        elif b in get_bugs_from_warnings(sb_fail1) or b in get_bugs_from_warnings(sb_fail2):
            entry += "& M "
        else:
            entry += "& - "
            
        entry += "\\\\"  
            
        print(entry)
        
    print()


def get_true_detected_bugs_by_each_tool():
    rel_path = './diffs_warnings/'
    ep_res1 = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ1 = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part1 = load_parsed_ep(rel_path + "ep_part.json")
     
    inf_res1 = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ1 = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part1 = load_parsed_inf(rel_path + "inf_part.json")
     
    sb_res1 = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ1 = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part1 = load_parsed_sb(rel_path + "sb_part.json")
    
    rel_path = './removed_warnings/'
    ep_res2 = load_parsed_ep(rel_path + "ep_warnings.json")
    ep_succ2 = load_parsed_ep(rel_path + "ep_succ.json")
    ep_part2 = load_parsed_ep(rel_path + "ep_part.json")
     
    inf_res2 = load_parsed_inf(rel_path + "inf_warnings.json")
    inf_succ2 = load_parsed_inf(rel_path + "inf_succ.json")
    inf_part2 = load_parsed_inf(rel_path + "inf_part.json")
     
    sb_res2 = load_parsed_sb(rel_path + "sb_warnings.json")
    sb_succ2 = load_parsed_sb(rel_path + "sb_succ.json")
    sb_part2 = load_parsed_sb(rel_path + "sb_part.json")
    
    print("\nTrue bugs found by each tool\n")
    ep_succ = get_bugs_from_warnings(ep_succ1) | get_bugs_from_warnings(ep_succ2) | get_bugs_from_warnings(ep_part1) | get_bugs_from_warnings(ep_part2)
    print("Ep:", len(ep_succ))
    with open(os.path.join(os.getcwd(), "ep_detected"), 'w') as f:
        f.write("\n".join(i for i in ep_succ))
     
    inf_succ = get_bugs_from_warnings(inf_succ1) | get_bugs_from_warnings(inf_succ2) | get_bugs_from_warnings(inf_part1) | get_bugs_from_warnings(inf_part2)
    print("Inf:", len(inf_succ))
    with open(os.path.join(os.getcwd(), "inf_detected"), 'w') as f:
        f.write("\n".join(i for i in inf_succ))
     
    sb_succ = get_bugs_from_warnings(sb_succ1) | get_bugs_from_warnings(sb_succ2) | get_bugs_from_warnings(sb_part1) | get_bugs_from_warnings(sb_part2)
    print("Sb:", len(sb_succ))
    with open(os.path.join(os.getcwd(), "sb_detected"), 'w') as f:
        f.write("\n".join(i for i in sb_succ))
    
    print()

     

''' this script has to be run from the results/ directory '''

    
if __name__ == '__main__':
    
    # display_min_max_avg_warnings_per_bug_total()
    
    # get_warnings_bugs_from_each_approach()
     
    # get_manually_inspected_warnings_bugs()

    # get_cand_detected_bugs_tools_sets()
      
    # get_cand_detected_bugs_tools_table()

    get_true_detected_bugs_by_each_tool()
