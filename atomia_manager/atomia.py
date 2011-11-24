'''
Created on Nov 7, 2011

@author: Dusan

'''
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
    else:
        if args.service_id is not None or args.path is not None:
            raise Exception("Could not find the parent service.")
        else:
            child_services_result = manager.list_existing_service(None, args.account)
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
    
def service_find(args, manager):
    
    if args.query is not None:
        find_options = json.loads(args.query)
        if isinstance(find_options, dict):
            if find_options.has_key('name'):
                service_name = find_options['name']
            else:
                raise InputError("find_options argument must contain key name")
            
            relative_path = find_options['path'] if find_options.has_key('path') else ''
            result_page = find_options['page'] if find_options.has_key('page') else '0'
            result_count = find_options['count'] if find_options.has_key('count') else '100'
            
            if find_options.has_key('properties'):
                if isinstance(find_options['properties'], dict):
                    service_properties = find_options['properties']
                else:
                    raise InputError("Invalid format of the properties key")
            else:
                service_properties = None
        else:
            raise InputError("Invalid format of query argument.")
    else:
        raise InputError("query is required argument for this action.")
    
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
        return find_result_list
    else:
        raise Exception("Could not find service: " + service_name)

def service_add(args, manager):
    
    if args.servicedata is not None:
        service_description = json.loads(args.servicedata)
        if isinstance(service_description, dict):
            if service_description.has_key('name'):
                service_name = service_description['name']
            else:
                raise InputError("service argument must contain key name")
            
            if service_description.has_key('properties'):
                if isinstance(service_description['properties'], dict):
                    service_properties = service_description['properties']
                else:
                    service_properties = None
            else:
                service_properties = None
        else:
            raise InputError("Invalid format of find_options argument.")
    else:
        raise InputError("service is required argument for this action.")
    
    parent_service = find_service_by_arguments(args, manager)
    
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

            
            if parent_service is not None:
                add_service_result = manager.add_service([created_service.to_xml_friendly_object()], [parent_service.to_xml_friendly_object()], args.account)
            else:
                add_service_result = manager.add_service([created_service.to_xml_friendly_object()], None, args.account)
            
            if add_service_result.has_key("AddServiceResult") and len(add_service_result["AddServiceResult"]) == 1:
                for k in add_service_result["AddServiceResult"]:
                    added_service = AtomiaService()
                    added_service.from_simplexml(k)
                    added_service.print_me(False, True)
                    return added_service
            else:
                raise Exception("Could not add service: " + created_service.name)
            
    else:
        raise Exception("Could not create service: " + service_name)

def service_delete(args, manager):
    service_to_delete = find_service_by_arguments(args, manager)
    if service_to_delete is not None:
        manager.delete_service([service_to_delete.to_xml_friendly_object()], args.account)
        print "Deleted service " + service_to_delete.logical_id + " successfully."
        return True
    else:
        raise Exception("No service found!")
    
    
def service_modify(args, manager):
    
    if args.servicedata is not None:
        service_description = json.loads(args.servicedata)
        if isinstance(service_description, dict):
            if service_description.has_key('properties'):
                if isinstance(service_description['properties'], dict):
                    service_properties = service_description['properties']
                else:
                    raise InputError("Invalid format of properties argument.")
            else:
                raise InputError("properties is required argument for this action")
        else:
            raise InputError("Invalid format of service argument.")
    else:
        raise InputError("service is required argument for this action.")
    
    current_service = find_service_by_arguments(args, manager)
    if current_service is None:
        raise Exception("Could not find service to be modified.")
    
    
    
    if current_service.properties is not None and len(current_service.properties) > 0:
        non_existing_props_list = list(set(service_properties.keys())-set(map(lambda x: x.name, current_service.properties)))
        if len(non_existing_props_list) > 0:
            raise Exception("Non-existing property: " + non_existing_props_list[0])
        else:
            for list_count in current_service.properties:
                if (service_properties.has_key(list_count.name)):
                    list_count.prop_string_value = service_properties[list_count.name]
                
        modify_service_result = manager.modify_service([current_service.to_xml_friendly_object()], args.account)
        
        if modify_service_result.has_key("ModifyServiceResult") and len(modify_service_result["ModifyServiceResult"]) == 1:
            for k in modify_service_result["ModifyServiceResult"]:
                modified_service = AtomiaService()
                modified_service.from_simplexml(k)
                modified_service.print_me(False, True)
                return modified_service
        else:
            raise Exception("Could not modify service: " + current_service.name)
                    
def find_service_by_arguments(args, manager):
    
    if args.service_id is not None:
        show_service_instance = manager.get_service_by_id(args.account, args.service_id)
        if show_service_instance.has_key("GetServiceByIdResult") and len(show_service_instance["GetServiceByIdResult"]) == 1:
            for k in show_service_instance["GetServiceByIdResult"]:
                service_to_return = AtomiaService()
                service_to_return.from_simplexml(k)
                return service_to_return if service_to_return.logical_id is not None else None
        
    elif args.path is not None:
        show_service_locator = json.loads(args.path)
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

def account_list(args, manager):
    
    result_page = '0'
    result_count = '100'
    
    if args.query is not None:
        find_options = json.loads(args.query)
        if isinstance(find_options, dict):
            if find_options.has_key('page'):
                result_page = find_options['page']
            if find_options.has_key('count'):
                result_count = find_options['count'] 
        else:
            raise InputError("Invalid format of query argument.")
    
    accounts_result = manager.list_accounts(page_number = result_page, page_size = result_count)
    
    if accounts_result.has_key("ListAccountsWithPaginationResult") and len(accounts_result["ListAccountsWithPaginationResult"].children()) > 0:
        list_result_list = []
        for j in accounts_result["ListAccountsWithPaginationResult"].children():
            child_service = AtomiaAccount()
            child_service.from_simplexml(j)
            list_result_list.append(child_service)
        print json_repr(list_result_list) 
        return list_result_list
    else:
        raise Exception("Could not find any account.")
    
def account_show(args, manager):
    
    accounts_result = manager.get_account(args.account)
    
    if accounts_result.has_key("GetAccountResult") and len(accounts_result["GetAccountResult"].children()) > 0:
        account_result = AtomiaAccount()
        account_result.from_simplexml(accounts_result["GetAccountResult"])
        account_result.print_me()
        return account_result
    else:
        raise Exception("Could not find any account with number " + args.account)    


def account_add(args, manager):
    
    if args.accountdata is not None:
        account_data = json.loads(args.accountdata)
        if isinstance(account_data, dict):
            if account_data.has_key('account_id'):
                account_id = account_data['account_id']
            else:
                raise InputError("account argument must contain key account_id")
            
            if account_data.has_key('account_description'):
                account_description = account_data['account_description']
            else:
                account_description = None
                
            if account_data.has_key('provisioning_description'):
                provisioning_description = account_data['provisioning_description']
            else:
                provisioning_description = None
            
            if account_data.has_key('account_properties'):
                if isinstance(account_data['account_properties'], dict):
                    account_properties = account_data['account_properties']
                else:
                    account_properties = None
            else:
                account_properties = None
        else:
            raise InputError("Invalid format of account argument.")
    else:
        raise InputError("Account is required argument for this action.")
    
    account_to_create = AtomiaAccount(account_id = account_id, account_description = account_description, account_properties = account_properties, provisioning_description = provisioning_description)
    
    manager.add_account([account_to_create.to_xml_friendly_object()])
    
    accounts_result = manager.get_account(account_id)
    
    if accounts_result.has_key("GetAccountResult") and len(accounts_result["GetAccountResult"].children()) > 0:
        account_result = AtomiaAccount()
        account_result.from_simplexml(accounts_result["GetAccountResult"])
        account_result.print_me()
        return account_result
    else:
        raise Exception("Could not find any account with number " + account_id)
    
def account_delete(args, manager):

    manager.delete_account(args.account)
    print "Deleted account " + args.account + " successfully."
    return True

def main(args):
    manager = AtomiaActions(username = args.username, password = args.password, api_url = args.url)
    if args.entity == 'service':
        if args.account is None:
            raise InputError("Account number is required argument for this action.")
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
    elif args.entity == 'account':
        if args.action == 'list':
            return account_list(args, manager)
        elif args.action == 'show':
            if args.account is None:
                raise InputError("Account number is required argument for this action.")
            else:
                return account_show(args, manager)
        elif args.action == 'add':
            return account_add(args, manager)
        elif args.action == 'delete':
            if args.account is None:
                raise InputError("Account number is required argument for this action.")
            else: 
                return account_delete(args, manager)
        else:
            raise InputError("Unknown action: " + args.action + " for the entity: " + args.entity)
    
def entry():
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Atomia Automation Server Manager', prog='atomia')
    parser.add_argument('--username', help="The API user's username")
    parser.add_argument('--password', help="The API user's password")
    parser.add_argument('--url',  metavar='API_URL', help="The URL of the Automation Server API's wsdl")
    parser.add_argument('entity', help='account|package|service')
    parser.add_argument('action', help='show|list|find|add|delete|modify')
    parser.add_argument('--account', help='The account in Automation Server. Required for service *, package *, account show|delete.')
    parser.add_argument('--service_id', help='The string with logical id of the parent service (add|find service actions) or the given service (show|list|modify|delete service actions)')
    parser.add_argument('--path', help='Can replace --service or --parent. The JSON representation of the path to the parent service (add|find service actions) or the given service (show|list|modify|delete service actions)')
    parser.add_argument('--servicedata', metavar='SERVICE_DATA', help='Required argument when using add/modify service; Json representation of the service to be added/modified with possible keys: name(required when adding) and properties(required when adding or modifying')
    parser.add_argument('--query', help='Required argument when using find service, optional when using list accounts; Json object with possible keys: name, path, properties, page, count')
    parser.add_argument('--accountdata', metavar='ACCOUNT_DATA',help='Required argument when adding account; Json object with possible keys: account_id, account_description, account_properties, provisioning_description')
    
    args = parser.parse_args()
    
    try:
        main(args)
    except InputError, (instance):
        print instance.parameter
        sys.exit()     
    except urllib2.HTTPError, error:
        dom = minidom.parseString(error.read())
        print "Api returned an error: \n", dom.toprettyxml()
        sys.exit()

if __name__=="__main__":
    entry()   