import time
from atomia_entities import AtomiaAccount, AtomiaService, AtomiaServiceSearchCriteria, AtomiaServiceSearchCriteriaProperty
from atomia_actions import AtomiaActions
import atomia
import pytest

class ArgumentsMock(object):
    def __init__(self, username = None, password = None, api_url = None, entity = None, action = None, account = None, service_id = None, service_locator = None, service = None, find_options = None):

        self.username = username
        
        self.password = password
        
        self.api_url = api_url
        
        self.entity = entity
        
        self.action = action
        
        self.account = account
        
        self.service_id = service_id
        
        self.service_locator = service_locator
        
        self.service = service
        
        self.find_options = find_options


def test_show_no_service():
    mock = ArgumentsMock(entity="service", action = "show")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_non_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "show", service_id="00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "show", service_id="4fe9b823-0020-4e33-abd9-a2de6a1480af", account="101321")
    assert isinstance(atomia.main(mock), AtomiaService)
    
def test_show_non_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "show", service_locator="[{\"CsBase\" : {\"foo\" : \"bar\"}} ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_show_non_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "show", service_locator="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : { \"foo\" : \"bar\" } } ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
    
def test_show_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "show", service_locator="[{\"DomainRegContact\" : {\"Id\" : \"138\"}} ]", account="101321")
    assert isinstance(atomia.main(mock), AtomiaService)
    
def test_show_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "show", service_locator="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : \"584e20b8-756f-49e4-b426-a58b835a873e\"} ]", account="101321")
    assert isinstance(atomia.main(mock), AtomiaService)
    

def test_list_no_service():
    mock = ArgumentsMock(entity="service", action = "list", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
    
def test_list_non_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "list", service_id="00000000-0000-0000-0000-000000000000")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_list_existing_service_id():
    mock = ArgumentsMock(entity="service", action = "list", service_id="d83805a8-c4a3-4e17-96af-4c9f0c1679d2", account="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0 
    
def test_list_non_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "list", service_locator="[{\"CsBase\" : {\"foo\" : \"bar\"}} ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
        
def test_list_non_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "list", service_locator="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : { \"foo\" : \"bar\" } } ]", account="101321")
    with pytest.raises(Exception):
        atomia.main(mock)
    
def test_list_existing_service_description():
    mock = ArgumentsMock(entity="service", action = "list", service_locator="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsWindowsWebsite\" : {\"Hostname\":\"python43.org\"} } ]", account="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    
def test_list_existing_service_description_2():
    mock = ArgumentsMock(entity="service", action = "list", service_locator="[{\"CsBase\" : \"d83805a8-c4a3-4e17-96af-4c9f0c1679d2\" }, {\"CsLinuxWebsite\" : \"584e20b8-756f-49e4-b426-a58b835a873e\"} ]", account="101321")
    assert isinstance(atomia.main(mock), list) and len(atomia.main(mock)) > 0
    

    
