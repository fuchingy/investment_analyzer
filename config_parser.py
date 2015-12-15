#!/usr/bin/python
"""Module contains functions to parse ini file

This module have functions to extract information from a ini file. The fundation
is the python ConfigParser module.

Example:
    Call functions

"""
import logging
import ConfigParser

def get_all(ini_file, to_list=False):
    """Get all information from a ini file

    Every section in the ini file will be extracted and put into a dictionary

    Args:
        ini_file: the ini file path
        to_list : if convert the value into a list

    Returns:
        A dict contains all settings.

    """
    log = logging.getLogger(__name__)
    cfg_parser = ConfigParser.ConfigParser()
    cfg_parser.optionxform = str # Preserve uppercase if any
    try:
        cfg_parser.read(ini_file)
    except:
        log.warning("Fail to parse %s", ini_file)
        return {}

    cfg = {}
    for section in cfg_parser.sections():
        dict1 = {}
        options = cfg_parser.options(section)
        for option in options:
            try:
                if to_list:
                    dict1[option] = cfg_parser.get(section, option)
                    dict1[option] = [e.strip(' \'"') for e in dict1[option].split(',')]
                else:
                    dict1[option] = cfg_parser.get(section, option)
                log.debug(dict1[option])
                if dict1[option] == -1:
                    log.debug("skip: %s", option)
            except:
                log.error("exception on %s!", option)
                dict1[option] = None
        cfg[section] = dict1

    return cfg

def get_by_section(ini_file, section, to_list=False):
    """Get only the specific section information from a ini file

    Only the section specified will be extracted and put into a dictionary.
    If no such section exists, empty dict will be returned.

    Args:
        ini_file: the ini file path
        section : the name of the section to be extracted
        to_list : if convert the value into a list

    Returns:
        A dict contains all settings.

    """
    log = logging.getLogger(__name__)
    cfg = get_all(ini_file, to_list)
    if section in cfg:
        return cfg[section]
    else:
        log.warning("Cannot find section %s in ini file %s", section, ini_file)
        return {}
