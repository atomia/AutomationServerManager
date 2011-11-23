import time
from atomia_entities import AtomiaAccount, AtomiaService, AtomiaServiceSearchCriteria, AtomiaServiceSearchCriteriaProperty
from atomia_actions import AtomiaActions
import atomia
import pytest
import urllib2

class ArgumentsMock(object):
    def __init__(self, username = None, password = None, api_url = None, entity = None, action = None, account_number = None, service_id = None, path = None, service = None, find_options = None):

        self.username = username
        
        self.password = password
        
        self.api_url = api_url
        
        self.entity = entity
        
        self.action = action
        
        self.account_number = account_number
        
        self.service_id = service_id
        
        self.path = path
        
        self.service = service
        
        self.find_options = find_options


# show service

def test_show_no_service():
    mock = ArgumentsMock(entity="service", action = "show")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_non_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "show", service_id="00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "show", service_id="4fe9b823-0020-4e33-abd9-a2de6a1480af", account_number="101321")
    assert isinstance(atomia.main(mock), AtomiaService)
    
def test_show_non_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"CsBase\" : {\"foo\" : \"bar\"}} ]", account_number="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_non_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : { \"foo\" : \"bar\" } } ]", account_number="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
    
def test_show_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"DomainRegContact\" : {\"Id\" : \"138\"}} ]", account_number="101321")
    assert isinstance(atomia.main(mock), AtomiaService)
    
def test_show_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : \"584e20b8-756f-49e4-b426-a58b835a873e\"} ]", account_number="101321")
    assert isinstance(atomia.main(mock), AtomiaService)

# list service
    
def test_list_no_service():
    mock = ArgumentsMock(entity="service", action = "list", account_number="101321")
    assert isinstance(atomia.main(mock), list)
    
def test_list_non_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "list", service_id="00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_list_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "list", service_id="d83805a8-c4a3-4e17-96af-4c9f0c1679d2", account_number="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0 
    
def test_list_non_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : {\"foo\" : \"bar\"}} ]", account_number="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_list_non_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : { \"foo\" : \"bar\" } } ]", account_number="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
    
def test_list_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsWindowsWebsite\" : {\"Hostname\":\"python43.org\"} } ]", account_number="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_list_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : \"584e20b8-756f-49e4-b426-a58b835a873e\"} ]", account_number="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
# find service 

def test_find_no_service():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321")
    with pytest.raises(atomia.InputError):
        atomia.main(mock)
    
def test_find_non_existing_parent_service_id():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", service_id="00000000-0000-0000-0000-000000000000", find_options = "{ \"service_name\" : \"CsLinuxWebsite\" }" )
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_find_existing_parent_service_id():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", service_id="d83805a8-c4a3-4e17-96af-4c9f0c1679d2", find_options = "{ \"service_name\" : \"CsLinuxWebsite\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_existing_parent_service_id_with_relative_path():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", service_id="d83805a8-c4a3-4e17-96af-4c9f0c1679d2", find_options = "{ \"service_name\" : \"ApacheWebSite\", \"relative_path\" : \"CsLinuxWebsite\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_existing_parent_service_id_with_invalid_relative_path():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", service_id="d83805a8-c4a3-4e17-96af-4c9f0c1679d2", find_options = "{ \"service_name\" : \"ApacheWebSite\", \"relative_path\" : \"foo\" }" )
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_find_existing_parent_service_id_with_relative_path():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", service_id="d83805a8-c4a3-4e17-96af-4c9f0c1679d2", find_options = "{ \"service_name\" : \"ApacheWebSite\", \"relative_path\" : \"CsLinuxWebsite\", \"service_properties\" : { \"PhpVersion\" : \"5.2\"} }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_existing_parent_service_locator_with_multiple_parents():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\"}, {\"CsWindowsWebsite\" : { \"InitEmail\" : \"true\"}}]", find_options = "{ \"service_name\" : \"DnsZoneRecord\", \"relative_path\" : \"DnsZone\" }" )
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_find_existing_parent_service_locator():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\"}, {\"CsWindowsWebsite\" : { \"Hostname\" : \"python44.org\"}}]", find_options = "{ \"service_name\" : \"DnsZoneRecord\", \"relative_path\" : \"DnsZone\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_no_parent():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", find_options = "{ \"service_name\" : \"DnsZoneRecord\", \"relative_path\" : \"CsBase/CsWindowsWebsite/DnsZone\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_no_parent_root_service():
    mock = ArgumentsMock(entity="service", action = "find", account_number="101321", find_options = "{ \"service_name\" : \"CsBase\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0  
 
# add service

def test_add_no_service():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321")
    with pytest.raises(atomia.InputError):
        atomia.main(mock)

def test_add_missing_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
    with pytest.raises(urllib2.HTTPError):
        atomia.main(mock)

def test_add_no_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result = atomia.main(mock)
    assert isinstance(result, AtomiaService)
    mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result.logical_id)
    atomia.main(mock)
    
def test_add_with_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        result = atomia.main(mock)
        assert isinstance(result, AtomiaService)
        mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False    
        
def test_add_with_parent_service_and_invalid_name():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase \", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        with pytest.raises(urllib2.HTTPError):
            atomia.main(mock)
        mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False
        
def test_add_with_parent_service_and_invalid_property():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseMame\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        with pytest.raises(urllib2.HTTPError):
            atomia.main(mock)
        mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False
    

def test_add_with_parent_service_and_missing_properties():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase\" }")
        with pytest.raises(urllib2.HTTPError):
            atomia.main(mock)
        mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False

# delete service

def test_delete_no_service():
    mock = ArgumentsMock(entity="service", action = "delete", account_number="101321")
    with pytest.raises(Exception):
        atomia.main(mock)

def test_delete_invalid_service_id():
    mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = "00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)

def test_delete_non_existing_service_locator_path():
    mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\"}, {\"CsMySqlDatabase\" : { \"DatabaseName\" : \"python44.org\"}}]")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_delete_service_id():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    add_result = atomia.main(mock)
    mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = add_result.logical_id)
    assert atomia.main(mock)
    
def test_delete_service_locator():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    add_result_parent = atomia.main(mock)
    if (isinstance(add_result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = add_result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if (isinstance(add_result, AtomiaService)):
            delete_mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", path="[{\"CsDatabase\" : \"" + add_result_parent.logical_id + "\"}, { \"CsMySqlDatabase\" : { \"DatabaseName\" : \"testpy45\"} } ]")
            assert atomia.main(delete_mock)

            mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = add_result_parent.logical_id)
            atomia.main(mock)
        else:
            assert False
    else:
        assert False

# modify service

def test_modify_no_service():
    mock = ArgumentsMock(entity="service", action = "modify", account_number="101321")
    with pytest.raises(atomia.InputError):
        atomia.main(mock)

def test_modify_missing_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"Collation\" : \"utf8_unicode_ci\"}}")
    with pytest.raises(urllib2.HTTPError):
        atomia.main(mock)

def test_modify_with_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if isinstance(add_result, AtomiaService):
            modify_result = ArgumentsMock(entity="service", action = "modify", account_number="101321", service_id = add_result.logical_id, service = "{ \"properties\" : { \"Collation\" : \"utf8_unicode_ci\"}}")
            assert isinstance(atomia.main(modify_result), AtomiaService)
            mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
            atomia.main(mock)
        else:
            assert False
    else:
        assert False    
        
def test_modify_with_parent_service_and_invalid_property():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if isinstance(add_result, AtomiaService):
            modify_result = ArgumentsMock(entity="service", action = "modify", account_number="101321", service_id = add_result.logical_id, service = "{ \"properties\" : { \"Colation\" : \"utf8_unicode_ci\"}}")
            with pytest.raises(Exception):
                atomia.main(modify_result)
            mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
            atomia.main(mock)
        else:
            assert False
            mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
            atomia.main(mock)
    else:
        assert False    

def test_modify_with_parent_service_and_missing_properties():
    mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account_number="101321", service_id = result_parent.logical_id, service = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if isinstance(add_result, AtomiaService):
            modify_result = ArgumentsMock(entity="service", action = "modify", account_number="101321", service_id = add_result.logical_id)
            with pytest.raises(Exception):
                atomia.main(modify_result)
            mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
            atomia.main(mock)
        else:
            assert False
            mock = ArgumentsMock(entity="service", action = "delete", account_number="101321", service_id = result_parent.logical_id)
            atomia.main(mock)
    else:
        assert False      
