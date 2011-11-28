from atomia_entities import AtomiaService
import atomia
import pytest
import urllib2

class ArgumentsMock(object):
    def __init__(self, username = None, password = None, url = None, entity = None, action = None, account = None, service = None, parent = None, path = None, servicedata = None, query = None):

        self.username = username
        
        self.password = password
        
        self.url = url
        
        self.entity = entity
        
        self.action = action
        
        self.account = account
        
        self.service = service
        
        self.parent = parent
        
        self.path = path
        
        self.servicedata = servicedata
        
        self.query = query


# show service

def test_show_no_service():
    mock = ArgumentsMock(entity="service", action = "show")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_non_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "show", service = "00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "show", service = "4fe9b823-0020-4e33-abd9-a2de6a1480af", account="101321")
    assert isinstance(atomia.main(mock), AtomiaService)
    
def test_show_non_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"CsBase\" : {\"foo\" : \"bar\"}} ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_non_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : { \"foo\" : \"bar\" } } ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
    
def test_show_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"DomainRegContact\" : {\"Id\" : \"138\"}} ]", account="101321")
    assert isinstance(atomia.main(mock), AtomiaService)
    
def test_show_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "show", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : \"584e20b8-756f-49e4-b426-a58b835a873e\"} ]", account="101321")
    assert isinstance(atomia.main(mock), AtomiaService)

# list service
    
def test_list_no_service():
    mock = ArgumentsMock(entity="service", action = "list", account="101321")
    assert isinstance(atomia.main(mock), list)
    
def test_list_non_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "list", parent = "00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_list_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "list", parent = "d83805a8-c4a3-4e17-96af-4c9f0c1679d2", account="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0 
    
def test_list_non_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : {\"foo\" : \"bar\"}} ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_list_non_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : { \"foo\" : \"bar\" } } ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
    
def test_list_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsWindowsWebsite\" : {\"Hostname\":\"python43.org\"} } ]", account="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_list_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "list", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : \"584e20b8-756f-49e4-b426-a58b835a873e\"} ]", account="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
# find service 

def test_find_no_service():
    mock = ArgumentsMock(entity="service", action = "find", account="101321")
    with pytest.raises(atomia.InputError):
        atomia.main(mock)
    
def test_find_non_existing_parent_service_id():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", parent = "00000000-0000-0000-0000-000000000000", query = "{ \"name\" : \"CsLinuxWebsite\" }" )
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_find_existing_parent_service_id():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", parent = "d83805a8-c4a3-4e17-96af-4c9f0c1679d2", query = "{ \"name\" : \"CsLinuxWebsite\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_existing_parent_service_id_with_relative_path():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", parent = "d83805a8-c4a3-4e17-96af-4c9f0c1679d2", query = "{ \"name\" : \"ApacheWebSite\", \"path\" : \"CsLinuxWebsite\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_existing_parent_service_id_with_invalid_relative_path():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", parent = "d83805a8-c4a3-4e17-96af-4c9f0c1679d2", query = "{ \"name\" : \"ApacheWebSite\", \"path\" : \"foo\" }" )
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_find_existing_parent_service_id_with_relative_path_and_properties():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", parent = "d83805a8-c4a3-4e17-96af-4c9f0c1679d2", query = "{ \"name\" : \"ApacheWebSite\", \"path\" : \"CsLinuxWebsite\", \"properties\" : { \"PhpVersion\" : \"5.2\"} }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_existing_parent_service_locator_with_multiple_parents():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\"}, {\"CsWindowsWebsite\" : { \"InitEmail\" : \"true\"}}]", query = "{ \"name\" : \"DnsZoneRecord\", \"path\" : \"DnsZone\" }" )
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_find_existing_parent_service_locator():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\"}, {\"CsWindowsWebsite\" : { \"Hostname\" : \"python44.org\"}}]", query = "{ \"name\" : \"DnsZoneRecord\", \"path\" : \"DnsZone\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_no_parent():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", query = "{ \"name\" : \"DnsZoneRecord\", \"path\" : \"CsBase/CsWindowsWebsite/DnsZone\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_find_no_parent_root_service():
    mock = ArgumentsMock(entity="service", action = "find", account="101321", query = "{ \"name\" : \"CsBase\" }" )
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0  
 
# add service

def test_add_no_service():
    mock = ArgumentsMock(entity="service", action = "add", account="101321")
    with pytest.raises(atomia.InputError):
        atomia.main(mock)

def test_add_missing_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
    with pytest.raises(urllib2.HTTPError):
        atomia.main(mock)

def test_add_no_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result = atomia.main(mock)
    assert isinstance(result, AtomiaService)
    mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result.logical_id)
    atomia.main(mock)
    
def test_add_with_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy46\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        result = atomia.main(mock)
        assert isinstance(result, AtomiaService)
        mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False    
        
def test_add_with_parent_service_and_invalid_name():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase \", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        with pytest.raises(urllib2.HTTPError):
            atomia.main(mock)
        mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False
        
def test_add_with_parent_service_and_invalid_property():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseMame\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        with pytest.raises(urllib2.HTTPError):
            atomia.main(mock)
        mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False
    

def test_add_with_parent_service_and_missing_properties():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase\" }")
        with pytest.raises(urllib2.HTTPError):
            atomia.main(mock)
        mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False

# delete service

def test_delete_no_service():
    mock = ArgumentsMock(entity="service", action = "delete", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)

def test_delete_invalid_service_id():
    mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = "00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)

def test_delete_non_existing_service_locator_path():
    mock = ArgumentsMock(entity="service", action = "delete", account="101321", path="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\"}, {\"CsMySqlDatabase\" : { \"DatabaseName\" : \"python44.org\"}}]")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_delete_service_id():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    add_result = atomia.main(mock)
    mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = add_result.logical_id)
    assert atomia.main(mock)
    
def test_delete_service_locator():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    add_result_parent = atomia.main(mock)
    if (isinstance(add_result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = add_result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if (isinstance(add_result, AtomiaService)):
            delete_mock = ArgumentsMock(entity="service", action = "delete", account="101321", path="[{\"CsDatabase\" : \"" + add_result_parent.logical_id + "\"}, { \"CsMySqlDatabase\" : { \"DatabaseName\" : \"testpy45\"} } ]")
            assert atomia.main(delete_mock)

            mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = add_result_parent.logical_id)
            atomia.main(mock)
        else:
            assert False
    else:
        assert False

# modify service

def test_modify_no_service():
    mock = ArgumentsMock(entity="service", action = "modify", account="101321")
    with pytest.raises(atomia.InputError):
        atomia.main(mock)

def test_modify_missing_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"Collation\" : \"utf8_unicode_ci\"}}")
    with pytest.raises(urllib2.HTTPError):
        atomia.main(mock)

def test_modify_with_parent_service():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if isinstance(add_result, AtomiaService):
            modify_result = ArgumentsMock(entity="service", action = "modify", account="101321", service = add_result.logical_id, servicedata = "{ \"properties\" : { \"Collation\" : \"utf8_unicode_ci\"}}")
            assert isinstance(atomia.main(modify_result), AtomiaService)
        else:
            assert False
        mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False    
        
def test_modify_with_parent_service_and_invalid_property():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if isinstance(add_result, AtomiaService):
            modify_result = ArgumentsMock(entity="service", action = "modify", account="101321", service = add_result.logical_id, servicedata = "{ \"properties\" : { \"Colation\" : \"utf8_unicode_ci\"}}")
            with pytest.raises(Exception):
                atomia.main(modify_result)
        else:
            assert False
        mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False    

def test_modify_with_parent_service_and_missing_properties():
    mock = ArgumentsMock(entity="service", action = "add", account="101321", servicedata = "{ \"name\" : \"CsDatabase\" }")
    result_parent = atomia.main(mock)
    if (isinstance(result_parent, AtomiaService)):
        mock = ArgumentsMock(entity="service", action = "add", account="101321", parent = result_parent.logical_id, servicedata = "{ \"name\" : \"CsMySqlDatabase\", \"properties\" : { \"DatabaseName\" : \"testpy45\", \"CharacterSet\" : \"utf8\", \"Collation\" : \"utf8_general_ci\"}}")
        add_result = atomia.main(mock)
        if isinstance(add_result, AtomiaService):
            modify_result = ArgumentsMock(entity="service", action = "modify", account="101321", service = add_result.logical_id)
            with pytest.raises(Exception):
                atomia.main(modify_result)
        else:
            assert False
        mock = ArgumentsMock(entity="service", action = "delete", account="101321", service = result_parent.logical_id)
        atomia.main(mock)
    else:
        assert False      
