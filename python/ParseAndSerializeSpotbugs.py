'''

Created on Nov. 23, 2017

@author Andrew Habib

'''

'''
Currently, the spotbugs output files may contain 
analysis results of more than one .java file.
This happens in cases where analyzed bug involves 
more than one .java file.
'''

import json
import os
import sys

from xml.etree import cElementTree as ET

from Util import XmlReader, SpotbugsMsg, CustomEncoder, NO_WARNING


def parse_spotbugs_xml_output(proj, tree):
    reports = []
    has_bugs = False
    
    # Case where report file is NOT empty 
    try:
        for _, elem in tree:
            if elem.tag == "BugInstance":
                '''
                Tags gauaranteed to exist
                '''
                has_bugs = True
                cls = elem.find('Class').get("classname", "")
                cat = elem.attrib['category']
                abbrev = elem.attrib['abbrev']
                typ = elem.attrib['type']
                prio = elem.attrib['priority']
                rank = elem.attrib['rank']
                msg = elem.find('LongMessage').text
                '''
                Optional Tags (may not always exist)
                '''
                elem_mth = elem.find('Method')
                if elem_mth:
                    mth = elem_mth.get('name', '')
                else: mth = ''
            
                elem_field = elem.find('Field')
                if elem_field:
                    field = elem_field.get('name', '')
                else: field = ''
                
                lines = []
                elem_src_lines = elem.findall('SourceLine')
                if elem_src_lines:
                    for src_line in elem_src_lines:
                        if (src_line.tag == 'SourceLine' and
                            all (attr in src_line.attrib for attr in ['start', 'end']) and
                            src_line.get('classname') == cls):
                                lines.append((src_line.get('start'), src_line.get('end'), src_line.get('role')))                                
                
                parsed_msg = SpotbugsMsg(proj, cls, cat, abbrev, typ, prio, rank, msg, mth, field, lines)
                reports.append(parsed_msg)

    except ET.ParseError as err:
#         print(proj + " failed to parse.")
#         print(err)
        pass
    
    # Case where report file is empty 
    if not has_bugs:
        reports.append(SpotbugsMsg(proj, "", "", "", NO_WARNING, "", "", "", "", "", ""))
    
    return reports


'''
Takes only one argument: path to spotbugs raw data
'''

if __name__ == '__main__':
    
    location_to_data = os.path.join(os.getcwd(), sys.argv[1])
    list_of_data = sorted(os.listdir(location_to_data))
    
    data_paths = list(map(lambda f: os.path.join(location_to_data, f), list_of_data))

    parsed_reports_per_project = []

    for proj, tree in XmlReader(data_paths):
        parsed_reports_per_project.extend(parse_spotbugs_xml_output(proj, tree))
        
#     time_stamp = time.strftime("%Y%m%d-%H%M%S")
    time_stamp = ''
    parsed_output_file_name = "sb_parsed" + time_stamp + ".json"
    with open(parsed_output_file_name, "w") as file:
        json.dump(parsed_reports_per_project, file, cls=CustomEncoder, indent=4)
