'''
Created on Nov 7, 2011

@author: Dusan
'''
import time
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from datetime import datetime
from atomia_entities import AtomiaAccount, AtomiaService, AtomiaServiceSearchCriteria, AtomiaServiceSearchCriteriaProperty
from atomia_actions import AtomiaActions
import sys
import json


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
         self.parameter = msg
        
    def __str__(self):
       return repr(self.parameter)


def json_repr(obj):
  """Represent instance of a class as JSON.
  Arguments:
  obj -- any object
  Return:
  String that reprent JSON-encoded object.
  """
  def serialize(obj):
    """Recursively walk object's hierarchy."""
    if isinstance(obj, (bool, int, long, float, basestring)):
      return obj
    elif isinstance(obj, dict):
      obj = obj.copy()
      for key in obj:
        obj[key] = serialize(obj[key])
      return obj
    elif isinstance(obj, list):
      return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
      return tuple(serialize([item for item in obj]))
    elif hasattr(obj, '__dict__'):
      return serialize(obj.__dict__)
    else:
      return repr(obj) # Don't know how to handle, convert to string
  return json.dumps(serialize(obj), indent = 4)

def service_show(args):
    service_to_print = find_service_by_arguments(args)
    if service_to_print is not None:
        service_to_print.print_me()
    else:
        raise Exception("No service found!")

def service_list(args):
    current_service = find_service_by_arguments(args)
    if current_service is not None:
        child_services_result = manager.list_existing_service([current_service.to_xml_friendly_object()], args.account)
        if child_services_result.has_key("ListExistingServicesResult") and len(child_services_result["ListExistingServicesResult"].children()) > 0:
            list_result_list = []
            for j in child_services_result["ListExistingServicesResult"].children():
                child_service = AtomiaService()
                child_service.from_simplexml(j)
                list_result_list.append(child_service.to_print_friendly(False))
            print json_repr(list_result_list) 
        else:
            raise Exception("No child services found for the service with logical id: " + current_service.logical_id)
    else:
        raise Exception("No parent service found!")
    
def service_find(args):
    try:
        if args.find_options is not None:
            find_options = json.loads(args.find_options)
            if isinstance(find_options, dict):
                if find_options.has_key('service_name'):
                    service_name = find_options['service_name']
                else:
                    raise InputError("find_options argument must contain key service_name")
                
                relative_path = find_options['relative_path'] if find_options.has_key('relative_path') else ''
                result_page = find_options['result_page'] if find_options.has_key('result_page') else '0'
                result_count = find_options['result_count'] if find_options.has_key('result_count') else '100'
                
                if find_options.has_key('service_properties'):
                    if isinstance(find_options['service_properties'], dict):
                        service_properties = find_options['service_properties']
                    else:
                        raise InputError("Invalid format of the service_properties key")
                else:
                    service_properties = None
            else:
                raise InputError("Invalid format of find_options argument.")
        else:
            raise InputError("find_options is required argument for this action.")
    except InputError, (instance):
        print instance.parameter
        sys.exit()
    
    parent_service = find_service_by_arguments(args)
    
    service_search_criteria_list = []
    search_properties = []
    if parent_service is not None:
        tmp_ssc = AtomiaServiceSearchCriteria(service_name, relative_path, parent_service.to_xml_friendly_object('atom:ParentService', 'ParentService'))
    else:
        tmp_ssc = AtomiaServiceSearchCriteria(service_name, relative_path)
    
    service_search_criteria_list.append(tmp_ssc.to_xml_friendly_object('atom:ServiceSearchCriteria', 'ServiceSearchCriteria'))
    
    if service_properties is not None:
        for propk in service_properties:
            tmp_property = AtomiaServiceSearchCriteriaProperty(str(propk), str(service_properties[propk]))
            search_properties.append(tmp_property.to_xml_friendly_object('arr:KeyValueOfstringstring', 'KeyValueOfstringstring'))
    
    find_action_res = manager.find_services_by_path_with_paging(service_search_criteria_list, args.account, search_properties=search_properties, page_number=result_page, page_size = result_count)
    
    if find_action_res.itervalues().next() is not None and find_action_res.itervalues().next().children() is not None:
        find_result_list = []
        for k in find_action_res.itervalues().next().children():
            find_action_result = AtomiaService()
            find_action_result.from_simplexml(k)
            find_result_list.append(find_action_result.to_print_friendly(False, True))
        print json_repr(find_result_list)
    else:
        print "No service found."
        sys.exit()
        
   

def find_service_by_arguments(args):
    
    if args.service_id is not None:
        show_service_instance = manager.get_service_by_id(args.account, args.service_id)
        service_to_return = AtomiaService()
        service_to_return.from_simplexml(show_service_instance.itervalues().next())
        return service_to_return
        
    elif args.service_locator is not None:
        show_service_locator = json.loads(args.service_locator)
        if len(show_service_locator) > 0:
            parent_service_for_criteria = None
            for count in show_service_locator:
                if isinstance(count.values()[0], dict):
                    service_search_criteria_list = []
                    search_properties = []
                    if parent_service_for_criteria is not None:
                        tmp_ssc = AtomiaServiceSearchCriteria(str(count.keys()[0]), '', parent_service_for_criteria.to_xml_friendly_object('atom:ParentService', 'ParentService'))
                    else:
                        tmp_ssc = AtomiaServiceSearchCriteria(str(count.keys()[0]), '')
                        
                    service_search_criteria_list.append(tmp_ssc.to_xml_friendly_object('atom:ServiceSearchCriteria', 'ServiceSearchCriteria'))
                    for propk in count.values()[0]:
                        tmp_property = AtomiaServiceSearchCriteriaProperty(str(propk), str(count.values()[0][propk]))
                        search_properties.append(tmp_property.to_xml_friendly_object('arr:KeyValueOfstringstring', 'KeyValueOfstringstring'))
                    test = manager.find_services_by_path_with_paging(service_search_criteria_list, args.account, search_properties=search_properties)
                    if test.itervalues().next() is not None and test.itervalues().next().children() is not None and len(test.itervalues().next().children()) == 1:
                        for k in test.itervalues().next().children():
                            parent_service_for_criteria = AtomiaService()
                            parent_service_for_criteria.from_simplexml(k)
                    else:
                        break
        
                elif count.values()[0] is not None and count.values()[0] != '':
                    parent_service_for_criteria = manager.get_service_by_id(args.account, str(count.values()[0])) 
                    parent_service_for_criteria_pretty = AtomiaService()
                    parent_service_for_criteria_pretty.from_simplexml(parent_service_for_criteria.itervalues().next())
                    
                    if parent_service_for_criteria_pretty.logical_id is None:
                        parent_service_for_criteria = None
                    else:
                        parent_service_for_criteria = parent_service_for_criteria_pretty
                else:
                    raise InputError("Wrong input format of service locator for: " + str(count.keys()[0]))
                
            return parent_service_for_criteria
    else:
        return None

if __name__=="__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Atomia Automation Server Manager', prog='atomia')
    parser.add_argument('--username', help="The API user's username")
    parser.add_argument('--password', help="The API user's password")
    parser.add_argument('--api_url', help="The URL of the Automation Server API service")
    parser.add_argument('entity', help='account|package|service')
    parser.add_argument('action', help='show|list|find|add|delete|modify')
    parser.add_argument('account', help='The account number in Automation Server')
    parser.add_argument('--service_id', help='The string with logical id of the service (used in list|show|find actions')
    parser.add_argument('--service_locator', help='The JSON representation of the path to the given service')
    parser.add_argument('--service', help='The JSON representation of the given service')
    parser.add_argument('--find_options', help='Required argument when using find services; Json object with possible keys: service_name, relative_path, service_properties, result_page, result_count')
    
    args = parser.parse_args()
    
    manager = AtomiaActions(args.username if args.username is not None else 'Admin', args.password if args.password is not None else 'Admin123')
    
    if args.entity == 'service':
        if args.action == 'show':
            service_show(args)
        elif args.action == 'list':
           service_list(args)
        elif args.action == 'find':
            service_find(args)      
        else:
            raise InputError("Unknown action: " + args.action +" for the entity: " + args.entity)     
