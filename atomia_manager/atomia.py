'''
Created on Nov 7, 2011

@author: Dusan

'''
from atomia_client.atomia_entities import AtomiaAccount, AtomiaService, AtomiaServiceSearchCriteria, AtomiaServiceSearchCriteriaProperty, AtomiaPackage, AtomiaAccountProperty
from atomia_client.atomia_actions import AtomiaActions
from xml.dom import minidom
import sys
import json
import urllib2
from atomia_client.pysimplesoap_atomia.client import SoapFault
import ConfigParser
import os
import inspect

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
    service_to_print = find_service_by_arguments(manager, args.account, args.service, args.path, args.simpleProps)
    if service_to_print is not None:
        service_to_print.print_me(args.filter, args.first, True, False,)
        return service_to_print
    else:
        raise Exception("No service found!")

def service_list(args, manager):
    current_service = find_service_by_arguments(manager, args.account, args.parent, args.path, args.simpleProps)
    if current_service is not None:
        child_services_result = manager.list_existing_service([current_service.to_xml_friendly_object()], args.account)
    else:
        if args.service is not None or args.path is not None:
            raise Exception("Could not find the parent service.")
        else:
            child_services_result = manager.list_existing_service(None, args.account)
            
    list_result_list = []
    if child_services_result.has_key("ListExistingServicesResult") and child_services_result["ListExistingServicesResult"].children() is not None and len(child_services_result["ListExistingServicesResult"].children()) > 0:
        for j in child_services_result["ListExistingServicesResult"].children():
            child_service = AtomiaService(show_simple_props = args.simpleProps)
            child_service.from_simplexml(j)
            list_result_list.append(child_service.to_print_friendly(False))
        
        result = json_repr(list_result_list)
        
        ''' filter results '''
        if args.filter is not None:
            import jsonpath
            result = jsonpath.jsonpath(json.loads(result), args.filter)
            
            if args.first is True:
                if result:
                    result = result[0]
                    print json_repr(result).strip('"')
                else:
                    print ""
            else: 
                print json_repr(result)
        else:
            print result
    ''' else:
         raise Exception("No child services found for the service with logical id: " + current_service.logical_id) '''
    return list_result_list
    
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
    
    parent_service = find_service_by_arguments(manager, args.account, args.parent, args.path, args.simpleProps)
    
    service_search_criteria_list = []
    search_properties = []
    if parent_service is not None:
        tmp_ssc = AtomiaServiceSearchCriteria(service_name, relative_path, parent_service)
    else:
        tmp_ssc = AtomiaServiceSearchCriteria(service_name, relative_path)
    
    service_search_criteria_list.append(tmp_ssc.to_xml_friendly_object('atom:ServiceSearchCriteria', 'ServiceSearchCriteria'))
    
    if service_properties is not None:
        for propk in service_properties:
            tmp_property = AtomiaServiceSearchCriteriaProperty(str(propk), str(service_properties[propk]))
            search_properties.append(tmp_property.to_xml_friendly_object('arr:KeyValueOfstringstring', 'KeyValueOfstringstring'))
    
    find_action_res = manager.find_services_by_path_with_paging(service_search_criteria_list, args.account, search_properties=search_properties, page_number=result_page, page_size = result_count)
    
    find_result_list = []
    if find_action_res.itervalues().next() is not None and find_action_res.itervalues().next().children() is not None:
        
        for k in find_action_res.itervalues().next().children():
            find_action_result = AtomiaService(show_simple_props = args.simpleProps)
            find_action_result.from_simplexml(k)
            find_result_list.append(find_action_result.to_print_friendly(False, True))
        
        result = json_repr(find_result_list)
        
        ''' filter results '''
        if args.filter is not None:
            import jsonpath
            result = jsonpath.jsonpath(json.loads(result), args.filter)
            
            if args.first is True:
                if result:
                    result = result[0]
                    print json_repr(result).strip('"')
                else:
                    print ""
            else: 
                print json_repr(result)
        else:
            print result
    ''' else:
        raise Exception("Could not find service: " + service_name) '''
    return find_result_list

def service_add(args, manager, managernative):
    if args.accountdata is not None:
        account_data = json.loads(args.accountdata)
    else:
        account_data = None

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
    
    parent_service = find_service_by_arguments(manager, args.account, args.parent, args.path)
    
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
                        if (service_properties[list_count.name] == 'null' or service_properties[list_count.name] == 'NULL'):
                            list_count.prop_string_value = None
                        else:
                            list_count.prop_string_value = service_properties[list_count.name] 

            if args.noresource:
                if args.packagedata is not None:
                    package_data = json.loads(args.packagedata)
                    if isinstance(package_data, dict) and package_data.has_key('package_id') and package_data.has_key('package_name'):
                            package_arg = [ AtomiaPackage(package_id=package_data['package_id'], package_name=package_data['package_name']).to_xml_friendly_object() ]
                    else:
                        raise InputError("packagedata argument must contain key package_id and package_name")
                else:
                    package_arg = None

                if args.resourcename is None:
                    raise Exception("When specifying --noresource you have to specify --resourcename as well")
                elif parent_service is not None:
                    add_service_result = managernative.add_service_native([created_service.to_xml_friendly_object()], [parent_service.to_xml_friendly_object()], args.resourcename, None, args.account, package_arg, False)
                else:
                    add_service_result = managernative.add_service_native([created_service.to_xml_friendly_object()], None, args.resourcename, None, args.account, package_arg, False)
            else:
                if parent_service is not None:
                    add_service_result = manager.add_service([created_service.to_xml_friendly_object()], [parent_service.to_xml_friendly_object()], args.account)
                else:
                    add_service_result = manager.add_service([created_service.to_xml_friendly_object()], None, args.account)
            
            if add_service_result.has_key("AddServiceResult") and len(add_service_result["AddServiceResult"]) == 1:
                for k in add_service_result["AddServiceResult"]:
                    added_service = AtomiaService()
                    added_service.from_simplexml(k)
                    added_service.print_me(args.filter, args.first, False, True)
                    return added_service
            else:
                raise Exception("Could not add service: " + created_service.name)
            
    else:
        raise Exception("Could not create service: " + service_name)

def service_delete(args, manager, managernative):
    service_to_delete = find_service_by_arguments(manager, args.account, args.service, args.path)
    if service_to_delete is not None:
        if args.noresource:
            managernative.delete_service_native([service_to_delete.to_xml_friendly_object()], False)
        else:
            manager.delete_service([service_to_delete.to_xml_friendly_object()], args.account)
        print "Deleted service " + service_to_delete.logical_id + " successfully."
        return True
    else:
        raise Exception("No service found!")
    
    
def service_modify(args, manager, managernative):
    
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
    
    current_service = find_service_by_arguments(manager, args.account, args.service, args.path)
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

        if args.noresource:
            modify_service_result = managernative.modify_service_native([current_service.to_xml_friendly_object()], False)
        else:
            modify_service_result = manager.modify_service([current_service.to_xml_friendly_object()], args.account)
        
        if modify_service_result.has_key("ModifyServiceResult") and len(modify_service_result["ModifyServiceResult"]) == 1:
            for k in modify_service_result["ModifyServiceResult"]:
                modified_service = AtomiaService()
                modified_service.from_simplexml(k)
                modified_service.print_me(False, True)
                return modified_service
        else:
            raise Exception("Could not modify service: " + current_service.name)
                    
def service_operation(args, manager, managernative):
    service_to_call = find_service_by_arguments(manager, args.account, args.service, args.path)
    if service_to_call is not None:
        if args.operation is not None:
            operation_result = manager.call_operation_on_service([service_to_call.to_xml_friendly_object()], args.account, args.operation, args.arg)
            if operation_result.has_key("CallOperationResult"):
                print operation_result['CallOperationResult'].strip('"')
            else:
                raise Exception("Operation failed")
        else:
            raise InputError("operation is a required argument for this action.")
    else:
        raise Exception("Could not find service to perform operation on")

def find_service_by_arguments(manager, account, service_id, path, show_simple_props = False):
    
    if service_id is not None:
        show_service_instance = manager.get_service_by_id(account, service_id)
        if show_service_instance.has_key("GetServiceByIdResult") and len(show_service_instance["GetServiceByIdResult"]) == 1:
            for k in show_service_instance["GetServiceByIdResult"]:
                service_to_return = AtomiaService(show_simple_props = show_simple_props)
                service_to_return.from_simplexml(k)
                return service_to_return if service_to_return.logical_id is not None else None
        
    elif path is not None:
        show_service_locator = json.loads(path)
        if len(show_service_locator) > 0:
            parent_service_for_criteria = None
            for count in show_service_locator:
                if isinstance(count.values()[0], dict) or count.values()[0] == '':
                    service_search_criteria_list = []
                    search_properties = []
                    if parent_service_for_criteria is not None:
                        tmp_ssc = AtomiaServiceSearchCriteria(str(count.keys()[0]), '', parent_service_for_criteria)
                    else:
                        tmp_ssc = AtomiaServiceSearchCriteria(str(count.keys()[0]), '')
                        
                    service_search_criteria_list.append(tmp_ssc.to_xml_friendly_object('atom:ServiceSearchCriteria', 'ServiceSearchCriteria'))
                    if isinstance(count.values()[0], dict):
                        for propk in count.values()[0]:
                            tmp_property = AtomiaServiceSearchCriteriaProperty(str(propk), str(count.values()[0][propk]))
                            search_properties.append(tmp_property.to_xml_friendly_object('arr:KeyValueOfstringstring', 'KeyValueOfstringstring'))
                    test = manager.find_services_by_path_with_paging(service_search_criteria_list, account, search_properties=search_properties)
                    if test.itervalues().next() is not None and test.itervalues().next().children() is not None and len(test.itervalues().next().children()) > 0:
                        for k in test.itervalues().next().children():
                            parent_service_for_criteria = AtomiaService(show_simple_props = show_simple_props)
                            parent_service_for_criteria.from_simplexml(k)
                            break
                    else:
                        parent_service_for_criteria = None
                        break
        
                elif count.values()[0] is not None:
                    parent_service_for_criteria = manager.get_service_by_id(account, str(count.values()[0])) 
                    parent_service_for_criteria_pretty = AtomiaService(show_simple_props = show_simple_props)
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

    if accounts_result.has_key("GetAccountResult") and accounts_result["GetAccountResult"].children() is not None and len(accounts_result["GetAccountResult"].children()) > 0:
        account_result = AtomiaAccount()
        account_result.from_simplexml(accounts_result["GetAccountResult"])
        account_result.print_me()
        return account_result
    else:
        result = "{\n\t\"error\": \"don't exist\"\n}"
	print result
        return result


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

def package_list(args, manager):
    
    packages_result = manager.list_packages(args.account)
    
    list_result_list = []
    if packages_result.has_key("ListPackagesForAccountResult") and packages_result["ListPackagesForAccountResult"].children() is not None and len(packages_result["ListPackagesForAccountResult"].children()) > 0:
        for k in packages_result["ListPackagesForAccountResult"].children():
            pack_result = AtomiaPackage()
            pack_result.from_simplexml(k)
            list_result_list.append(pack_result)
    print json_repr(list_result_list)
    return list_result_list

def package_add(args, manager):
    
    if args.packagedata is not None:
        package_data = json.loads(args.packagedata)
        if isinstance(package_data, dict):
            if package_data.has_key('package_name'):
                package_name = package_data['package_name']
            else:
                raise InputError("packagedata argument must contain key package_name")
            
            if package_data.has_key('package_arguments'):
                if isinstance(package_data['package_arguments'], dict):
                    package_arguments = package_data['package_arguments']
                else:
                    package_arguments = None
            else:
                package_arguments = None
        else:
            raise InputError("Invalid format of packagedata argument.")
    else:
        raise InputError("packagedata is required argument for this action.")
    
    package_to_add = AtomiaPackage(package_name=package_name)
    
    if package_arguments is not None:
        properties_list = []
        for proper in package_arguments:
            properties_list.append(AtomiaAccountProperty(key = proper, value = package_arguments[proper]).to_xml_friendly_object("arr:KeyValueOfstringstring", "KeyValueOfstringstring"))

        manager.add_package(args.account, [package_to_add.to_xml_friendly_object()], properties_list)
    else:
        manager.add_package(args.account, [package_to_add.to_xml_friendly_object()])
    return package_list(args, manager)

def package_delete(args, manager):
    
    if args.packagedata is not None:
        package_data = json.loads(args.packagedata)
        if isinstance(package_data, dict):
            if package_data.has_key('package_id'):
                package_id = package_data['package_id']
            else:
                raise InputError("packagedata argument must contain key package_id")
            if package_data.has_key('package_name'):
                package_name = package_data['package_name']
            else:
                raise InputError("packagedata argument must contain key package_name")
        else:
            raise InputError("Invalid format of packagedata argument.")
    else:
        raise InputError("packagedata is required argument for this action.")
    
    package_to_delete = AtomiaPackage(package_id = package_id, package_name=package_name)

    manager.delete_package(args.account, [package_to_delete.to_xml_friendly_object()])
    print "Deleted package " + package_name + " for account " + args.account + " successfully."
    return True

def package_change(args, manager):

    if args.packagedata is not None:
        package_data = json.loads(args.packagedata)
        if isinstance(package_data, dict):
            if package_data.has_key('package_id'):
                package_id = package_data['package_id']
            else:
                raise InputError("packagedata argument must contain key package_id")
            if package_data.has_key('package_name'):
                package_name = package_data['package_name']
            else:
                raise InputError("packagedata argument must contain key package_name")
            if package_data.has_key('new_package_name'):
               new_package_name = package_data['new_package_name']
            else:
                raise InputError("packagedata argument must contain key new_package_name")
        else:
            raise InputError("Invalid format of packagedata argument.")
    else:
        raise InputError("packagedata is required argument for this action.")

    current_package = AtomiaPackage(package_id=package_id, package_name=package_name)

    manager.change_package(account_number=args.account, package=[current_package.to_xml_friendly_object()], new_package_name=new_package_name)
    return True

def main(args):
    username = args.username
    password = args.password
    api_url = args.url
    nativeapi_url = args.nativeurl
    bootstrap = False
    if (username is None or password is None or api_url is None):
        config = ConfigParser.ConfigParser()
        conf_file = config.read(['atomia.conf', os.path.dirname(os.path.realpath(inspect.stack()[-1][1])) + '/atomia.conf', os.path.abspath('/etc/atomia.conf')])
        if conf_file is not None and len(conf_file) > 0:
            if username is None:
                username = config.get("Automation Server API", "username")
            if password is None:
                password = config.get("Automation Server API", "password")
            if api_url is None:
                api_url = config.get("Automation Server API", "url")
            if nativeapi_url is None:
                nativeapi_url = config.get("Automation Server API", "nativeurl")
            
            bootstrap = config.has_option("Automation Server API", "bootstrap") and config.getboolean("Automation Server API", "bootstrap")
        else:
            raise Exception("Could not find the config file!")

    manager = AtomiaActions(username = username, password = password, api_url = api_url, bootstrap = bootstrap, debug = args.debug)
    if args.noresource and args.entity == 'service':
        managernative = AtomiaActions(username = username, password = password, api_url = nativeapi_url, bootstrap = bootstrap, debug = args.debug)
    else:
        managernative = None

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
            return service_add(args, manager, managernative)
        elif args.action == "delete":
            return service_delete(args, manager, managernative)
        elif args.action == "modify":
            return service_modify(args, manager, managernative)
        elif args.action == "operation":
            return service_operation(args, manager, managernative)
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
    elif args.entity == 'package':
        if args.account is None:
            raise InputError("Account number is required argument for this action.")
        if args.action == 'list':
            return package_list(args, manager)
        elif args.action == 'add':
            return package_add(args, manager)
        elif args.action == 'delete':
            return package_delete(args, manager)
        elif args.action == 'change':
            return package_change(args, manager)
        else:
            raise InputError("Unknown action: " + args.action + " for the entity: " + args.entity)
        
        
def str2bool(str):
    return str.lower() in ("true", "1")


def entry():
    
    import argparse
    import textwrap
    
    epilog = textwrap.dedent('''
            Examples
            ---------------------------------------------------------------------
            atomia service show --account 101321 --service "4fe9b823-0020-4e33-abd9-a2de6a1480af"
            atomia service show --account 101321 --path '[{"CsBase" : "d83805a8-c4a3-4e17-96af-4c9f0c1679d2" }, {"CsLinuxWebsite" : "584e20b8-756f-49e4-b426-a58b835a873e"} ]'
            atomia service list --account 101321 --path '[{"CsBase" : "d83805a8-c4a3-4e17-96af-4c9f0c1679d2" }, {"CsWindowsWebsite" : {"Hostname":"python43.org"} } ]'
            atomia service find --account 101321 --parent "d83805a8-c4a3-4e17-96af-4c9f0c1679d2" --query '{ "name" : "ApacheWebSite", "path" : "CsLinuxWebsite", "properties" : { "PhpVersion" : "5.2"} }'
            atomia service find --account 101321 --path '[{"CsBase" : "d83805a8-c4a3-4e17-96af-4c9f0c1679d2"}, {"CsWindowsWebsite" : { "Hostname" : "python44.org"}}]' --query '{ "name" : "DnsZoneRecord", "path" : "DnsZone" }'
            atomia service add --account 101321 --parent "b287bc9f-c0ae-43c4-88b0-ccb2bea4a17d" --servicedata '{ "name" : "CsMySqlDatabase", "properties" : { "DatabaseName" : "testpy46", "CharacterSet" : "utf8", "Collation" : "utf8_general_ci"}}'
            atomia service add --noresource --resourcename "MySQLResource1" --account 101321 --packagedata '{ "package_id" : "fd90201c-51a3-4057-b954-ad4d067b9431", "package_name": "BasePackage" }' --parent "b287bc9f-c0ae-43c4-88b0-ccb2bea4a17d" --servicedata '{ "name" : "CsMySqlDatabase", "properties" : { "DatabaseName" : "testpy46", "CharacterSet" : "utf8", "Collation" : "utf8_general_ci"}}'
            atomia service modify --account 101321 --service "61575762-d85a-4c6f-b953-5a71a504106b" --servicedata '{ "properties" : { "Collation" : "utf8_unicode_ci"}}'
            atomia service delete --account 101321 --service "61575762-d85a-4c6f-b953-5a71a504106b"
            atomia service operation --account 101321 --service "61575762-d85a-4c6f-b953-5a71a504106b" --operation "OperationName" --arg "Arguments"
            atomia account add --accountdata '{ "account_id":"manageracc1", "account_description" : "My desc"}'
            atomia package list --account 101321
            atomia package delete --account 101321 --packagedata '{ "package_id" : "fd90201c-51a3-4057-b954-ad4d067b9431",  "package_name" : "DomainRegistrationContactPackage"}'
            atomia package add --account 101321 --packagedata '{ "package_name" : "BasePackage", "package_arguments" : { "test1": "value1", "test2": "value2" }}'
            atomia package change --account 101321 --packagedata '{ "package_id": "fd90201c-51a3-4057-b954-ad4d067b9431", "package_name": "BasePackage", "new_package_name": "DnsPackage" }'
            
            Note:
            In Windows cmd.exe escape the quotes in the following way:
            atomia service show --account 101321 --path "[{\\"CsBase\\" : \\"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\\" }, {\\"CsLinuxWebsite\\" : \\"584e20b8-756f-49e4-b426-a58b835a873e\\"} ]"
            ''')
    
    parser = argparse.ArgumentParser(description='Atomia Automation Server Manager', prog='atomia', epilog = epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--username', help="The API user's username")
    parser.add_argument('--password', help="The API user's password")
    parser.add_argument('--url',  metavar='API_URL', help="The URL of the Automation Server Core API's wsdl")
    parser.add_argument('--nativeurl',  metavar='NATIVEAPI_URL', help="The URL of the Automation Server Native API's wsdl")
    parser.add_argument('--noresource', action='store_true', help="If set for service actions, then they will be done through Native API not touching resource. When set you need to specify the resource name that the service will be imported as beeing on.")
    parser.add_argument('--resourcename', help="If --noresource is set, then this is used to specify the resource name")
    parser.add_argument('--debug', action='store_true', help="If set, then trace all SOAP calls giving lots of debugging info")
    parser.add_argument('entity', help='account|package|service')
    parser.add_argument('action', help='show|list|find|add|delete|modify')
    parser.add_argument('--account', help='The account in Automation Server. Required for service *, package *, account show|delete.')
    parser.add_argument('--service', metavar='SERVICE_ID', help='The logical id of the service. Required for service show|modify|delete.')
    parser.add_argument('--parent', metavar='SERVICE_ID', help='The logical id of the parent service. Required for service add. Optional for service list|find.')
    parser.add_argument('--path', help='Can replace --service or --parent. The JSON representation of the path to the parent service (add|find service actions) or the given service (show|list|modify|delete service actions)')
    parser.add_argument('--servicedata', metavar='SERVICE_DATA', help='Required argument for service add|modify. Json representation of the service to be added/modified with possible keys: name(required when adding) and properties (required when adding or modifying). For service add you need to fill all required properties (as returned by service template. For service modify, you need to supply only properties that need to be changed.')
    parser.add_argument('--query', help='Required argument when using find service, optional when using list accounts; Json object with possible keys: name, path, properties, page, count')
    parser.add_argument('--accountdata', metavar='ACCOUNT_DATA',help='Required argument when adding account; Json object with possible keys: account_id, account_description, account_properties, provisioning_description')
    parser.add_argument('--packagedata', metavar='PACKAGE_DATA',help='Required argument when adding/deleting package for account; Json object with possible keys: package_id, package_name, package_arguments')

    ''' changes by Vukasin '''
    parser.add_argument('--filter', help="Filter result by using JSON paths.")
    parser.add_argument('--first', help="Show only first filtered result.")
    parser.add_argument('--simpleProps', help="Fill simple property structure, used for JSON paths.")
    ''' changes by Vukasin '''
    
    parser.add_argument('--operation', help="The operation to perform on service")
    parser.add_argument('--arg', help="Operation arguments to pass")

    args = parser.parse_args()
    
    if args.first is not None:
        args.first = str2bool(args.first)
    else:
        args.first = False;
        
    if args.simpleProps is not None:
        args.simpleProps = str2bool(args.simpleProps)
    else:
        args.simpleProps = False;
        
    try:
        main(args)
    except InputError, (instance):
        print >> sys.stderr, instance.parameter
        sys.exit(1)     
    except urllib2.HTTPError, error:
        dom = minidom.parseString(error.read())
        print >> sys.stderr, "Api returned an error: \n", dom.toprettyxml()
        sys.exit(2)
    except SoapFault, error:
        print >> sys.stderr, "Api returned an error: \n", error.faultstring
        sys.exit(2)

if __name__=="__main__":
    entry()   
