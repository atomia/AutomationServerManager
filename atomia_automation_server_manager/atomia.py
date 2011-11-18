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
from xml.dom import minidom
import sys
import json
import urllib2


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

def service_show(args, manager):
    service_to_print = find_service_by_arguments(args, manager)
    if service_to_print is not None:
        service_to_print.print_me()
        return service_to_print
    else:
        raise Exception("No service found!")

def service_list(args, manager):
    current_service = find_service_by_arguments(args, manager)
    if current_service is not None:
        child_services_result = manager.list_existing_service([current_service.to_xml_friendly_object()], args.account)
        if child_services_result.has_key("ListExistingServicesResult") and len(child_services_result["ListExistingServicesResult"].children()) > 0:
            list_result_list = []
            for j in child_services_result["ListExistingServicesResult"].children():
                child_service = AtomiaService()
                child_service.from_simplexml(j)
                list_result_list.append(child_service.to_print_friendly(False))
            print json_repr(list_result_list) 
            return list_result_list
        else:
            raise Exception("No child services found for the service with logical id: " + current_service.logical_id)
    else:
        raise Exception("No parent service found!")
    
def service_find(args, manager):
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
    
    try:
    
        parent_service = find_service_by_arguments(args, manager)
        
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
    
    except urllib2.HTTPError, error:
        dom = minidom.parseString(error.read())
        print "Api returned an error: \n", dom.toprettyxml()
        return

def service_add(args, manager):
    try:
        if args.service is not None:
            service_description = json.loads(args.service)
            if isinstance(service_description, dict):
                if service_description.has_key('service_name'):
                    service_name = service_description['service_name']
                else:
                    raise InputError("service argument must contain key service_name")
                
                if service_description.has_key('service_properties'):
                    if isinstance(service_description['service_properties'], dict):
                        service_properties = service_description['service_properties']
                    else:
                        service_properties = None
                else:
                    service_properties = None
            else:
                raise InputError("Invalid format of find_options argument.")
        else:
            raise InputError("service is required argument for this action.")
    except InputError, (instance):
        print instance.parameter
        sys.exit()
    
    parent_service = find_service_by_arguments(args, manager)
    
    try:
        if parent_service is not None:
            created_service_result = manager.create_service(service_name, [parent_service.to_xml_friendly_object()], args.account)
        else:
            created_service_result = manager.create_service(service_name, None, args.account)
        
        if created_service_result.has_key("CreateServiceResult") and len(created_service_result["CreateServiceResult"]) == 1:
            for j in created_service_result["CreateServiceResult"]:
                created_service = AtomiaService()
                created_service.from_simplexml(j)
                
                if service_properties is not None and created_service.properties is not None and len(created_service.properties) > 0:
                    for list_count in created_service.properties:
                        if (service_properties.has_key(list_count.name)):
                            list_count.prop_string_value = service_properties[list_count.name] 
    
                try :            
                    if parent_service is not None:
                        add_service_result = manager.add_service([created_service.to_xml_friendly_object()], [parent_service.to_xml_friendly_object()], args.account)
                    else:
                        add_service_result = manager.add_service([created_service.to_xml_friendly_object()], None, args.account)
                    
                    if add_service_result.has_key("AddServiceResult") and len(add_service_result["AddServiceResult"]) == 1:
                        for k in add_service_result["AddServiceResult"]:
                            added_service = AtomiaService()
                            added_service.from_simplexml(k)
                            added_service.print_me(False, True)
                    else:
                        raise Exception("Could not add service: " + created_service.name)
                            
                except urllib2.HTTPError, error:
                    dom = minidom.parseString(error.read())
                    print "Api returned an error: \n", dom.toprettyxml()
                    return
                
        else:
            raise Exception("Could not create service: " + service_name)
        
                 
    except urllib2.HTTPError, error:
        dom = minidom.parseString(error.read())
        print "Api returned an error: \n", dom.toprettyxml()
        return


def service_delete(args, manager):
    service_to_delete = find_service_by_arguments(args, manager)
    if service_to_delete is not None:
        try:
            manager.delete_service([service_to_delete.to_xml_friendly_object()], args.account)
            print "Deleted service " + service_to_delete.logical_id + " successfully."
        except urllib2.HTTPError, error:
            dom = minidom.parseString(error.read())
            print "Api returned an error: \n", dom.toprettyxml()
            return
    else:
        raise Exception("No service found!")
    
    
def service_modify(args, manager):
    try:
        if args.service is not None:
            service_description = json.loads(args.service)
            if isinstance(service_description, dict):
                if service_description.has_key('service_properties'):
                    if isinstance(service_description['service_properties'], dict):
                        service_properties = service_description['service_properties']
                    else:
                        raise InputError("Invalid format of service_properties argument.")
                else:
                    raise InputError("service_properties is required argument for this action")
            else:
                raise InputError("Invalid format of service argument.")
        else:
            raise InputError("service is required argument for this action.")
    except InputError, (instance):
        print instance.parameter
        sys.exit()
    
    current_service = find_service_by_arguments(args, manager)
    if current_service is None:
        raise Exception("Could not find service to be modified.")
    
    if current_service.properties is not None and len(current_service.properties) > 0:
        for list_count in current_service.properties:
            if (service_properties.has_key(list_count.name)):
                list_count.prop_string_value = service_properties[list_count.name]
                
        try:            
            modify_service_result = manager.modify_service([current_service.to_xml_friendly_object()], args.account)
            
            if modify_service_result.has_key("ModifyServiceResult") and len(modify_service_result["ModifyServiceResult"]) == 1:
                for k in modify_service_result["ModifyServiceResult"]:
                    modified_service = AtomiaService()
                    modified_service.from_simplexml(k)
                    modified_service.print_me(False, True)
            else:
                raise Exception("Could not modify service: " + current_service.name)
                    
        except urllib2.HTTPError, error:
            dom = minidom.parseString(error.read())
            print "Api returned an error: \n", dom.toprettyxml()
            return
                
    
def find_service_by_arguments(args, manager):
    
    if args.service_id is not None:
        try:
            show_service_instance = manager.get_service_by_id(args.account, args.service_id)
            if show_service_instance.has_key("GetServiceByIdResult") and len(show_service_instance["GetServiceByIdResult"]) == 1:
                for k in show_service_instance["GetServiceByIdResult"]:
                    service_to_return = AtomiaService()
                    service_to_return.from_simplexml(k)
                    return service_to_return if service_to_return.logical_id is not None else None
        
        except urllib2.HTTPError, error:
            dom = minidom.parseString(error.read())
            print "Api returned an error: \n", dom.toprettyxml()
            sys.exit()
        
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
                        parent_service_for_criteria = None
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

def main(args):
    manager = AtomiaActions(args.username if args.username is not None else 'Admin', args.password if args.password is not None else 'Admin123')
    if args.entity == 'service':
        if args.action == 'show':
            return service_show(args, manager)
        elif args.action == 'list':
            return service_list(args, manager)
        elif args.action == 'find':
            return service_find(args, manager)
        elif args.action == "add":
            return service_add(args, manager)
        elif args.action == "delete":
            return service_delete(args, manager)
        elif args.action == "modify":
            return service_modify(args, manager)
        else:
            raise InputError("Unknown action: " + args.action + " for the entity: " + args.entity)

if __name__=="__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Atomia Automation Server Manager', prog='atomia')
    parser.add_argument('--username', help="The API user's username")
    parser.add_argument('--password', help="The API user's password")
    parser.add_argument('--api_url', help="The URL of the Automation Server API service")
    parser.add_argument('entity', help='account|package|service')
    parser.add_argument('action', help='show|list|find|add|delete|modify')
    parser.add_argument('account', help='The account number in Automation Server')
    parser.add_argument('--service_id', help='The string with logical id of the parent service (add|find service actions) or the given service (show|list|modify|delete service actions)')
    parser.add_argument('--service_locator', help='The JSON representation of the path to the parent service (add|find service actions) or the given service (show|list|modify|delete service actions)')
    parser.add_argument('--service', help='Required argument when using add/modify service; Json representation of the service to be added/modified with possible keys: service_name(required when adding) and service_properties(required when adding or modifying')
    parser.add_argument('--find_options', help='Required argument when using find service; Json object with possible keys: service_name, relative_path, service_properties, result_page, result_count')
    
    args = parser.parse_args()
    
    main(args)     


       