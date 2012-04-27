'''
Created on 11 Apr 2012

@author: thtar
'''

from atomia_entities import  AtomiaService
from pysimplesoap_atomia.client import SoapFault

class NotAllowedError(RuntimeError):
    def __init__(self):
        pass

class AtomiaOperations(object):
    '''
    This class provides a higher level view to the operations on automation server
    '''

    def __init__(self, manager, account, username, password):
        self.manager = manager
        self.account = account
        self.username = username
        self.password = password
        
    def list_root_services(self):
        return self.list_child_services(None)
    
    def list_child_services(self, parent, all_children = False):
        get_logical_children = "false" if all_children else "true"
        if parent is None:
            child_services_result = self.manager.list_existing_service(None, self.account, get_logical_children = get_logical_children, username = self.username, password = self.password)
        else:
            child_services_result = self.manager.list_existing_service([parent.to_xml_friendly_object()], self.account, get_logical_children = get_logical_children, username = self.username, password = self.password)
        list_result_list = []
        if child_services_result.has_key("ListExistingServicesResult") and child_services_result["ListExistingServicesResult"].children() is not None and len(child_services_result["ListExistingServicesResult"].children()) > 0:
            for j in child_services_result["ListExistingServicesResult"].children():
                child_service = AtomiaService(show_simple_props = True)
                child_service.from_simplexml(j)
                list_result_list.append(child_service)
        return list_result_list
    
    def modify_service(self, service):
        try:
            result = self.manager.modify_service([service.to_xml_friendly_object()], self.account, username = self.username, password = self.password)
            newsvc = AtomiaService(show_simple_props = True)
            newsvc.from_simplexml(result["ModifyServiceResult"])
            return newsvc
        except SoapFault, error:
            if "ID000030" in error.faultstring:
                raise NotAllowedError()
    
    def add_service(self, service, parent):
        if parent is None:
            result = self.manager.add_service([service.to_xml_friendly_object()], None, self.account, username = self.username, password = self.password)
        else:
            result = self.manager.add_service([service.to_xml_friendly_object()], [parent.to_xml_friendly_object()], self.account, username = self.username, password = self.password)
        newsvc = AtomiaService(show_simple_props = True)
        newsvc.from_simplexml(result["AddServiceResult"])
        return newsvc
    
    def delete_service(self, service):
        self.manager.delete_service([service.to_xml_friendly_object()], self.account, username = self.username, password = self.password)
        
    def find_services_by_path_with_paging(self, search_criteria_list, search_properties = None, sort_by_prop_name = '', sort_asc = 'true',):
        xml_search_criteria_list = []
        for criteria in search_criteria_list:
            xml_search_criteria_list.append(criteria.to_xml_friendly_object('atom:ServiceSearchCriteria', 'ServiceSearchCriteria'))
        xml_search_criteria_property_list = []
        for property1 in search_properties:
            xml_search_criteria_property_list.append(property1.to_xml_friendly_object('arr:KeyValueOfstringstring', 'KeyValueOfstringstring'))
        child_services_result = self.manager.find_services_by_path_with_paging(xml_search_criteria_list, self.account, xml_search_criteria_property_list, sort_by_prop_name, sort_asc, username = self.username, password = self.password)
        list_result_list = []
        if child_services_result.has_key("FindServicesByPathWithPagingResult") and child_services_result["FindServicesByPathWithPagingResult"].children() is not None and len(child_services_result["FindServicesByPathWithPagingResult"].children()) > 0:
            for j in child_services_result["FindServicesByPathWithPagingResult"].children():
                child_service = AtomiaService(show_simple_props = True)
                child_service.from_simplexml(j)
                list_result_list.append(child_service)
        return list_result_list
            