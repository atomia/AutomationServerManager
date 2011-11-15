'''
Created on Nov 7, 2011

@author: Dusan
'''
import time
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from datetime import datetime
import atomia_entities

class AtomiaActions(object):
    
    def __init__(self, username, password, api_url = None, token_created = None, token_expires = None, soap_header = None):

        if token_created is None:
            self.created = datetime.fromtimestamp(time.mktime(time.gmtime())).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            self.created = token_created
        
        if token_expires is None:
            self.expires = datetime.fromtimestamp(time.mktime(time.gmtime()) + 300).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            sefl.expires = token_expires 
        
        self.username = username
        self.password = password
        self.api_url = api_url
        
        if soap_header is None:

            self.header = """<soap:Header xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                            xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <wsse:Security soap:mustUnderstand="1">
                    <wsu:Timestamp wsu:Id="_0">
                        <wsu:Created>%(Created)s</wsu:Created>
                        <wsu:Expires>%(Expires)s</wsu:Expires>
                    </wsu:Timestamp>
                    <wsse:UsernameToken wsu:Id="uuid-8a45f51b-fe46-4715-bdae-e596c36ad6be-1">
                      <wsse:Username>%(Username)s</wsse:Username>
                      <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">
                         %(Password)s
                      </wsse:Password>
                   </wsse:UsernameToken>
                </wsse:Security>
            </soap:Header>"""
            
            self.header = self.header % dict(Created=self.created, Expires=self.expires, Username = self.username, Password = self.password)
        else:
            self.header = soap_header
            
        self.client = SoapClient(wsdl=self.api_url if self.api_url is not None else "https://provisioning.testgui.atomiademo.com/CoreAPIBasicAuth.svc?wsdl", header=self.header, namespace="http://atomia.com/atomia/provisioning/", trace=False)
    def add_account(self, account):
        
        client = SoapClient(wsdl=self.api_url if self.api_url is not None else "https://provisioning.testgui.atomiademo.com/CoreAPIBasicAuth.svc?wsdl", header=self.header, namespace="http://atomia.com/atomia/provisioning/", trace=False)
        return client.AddAccount(account = account)
        
    def create_service(self, service_name, parent_service, account_number):
        client = SoapClient(wsdl=self.api_url if self.api_url is not None else "https://provisioning.testgui.atomiademo.com/CoreAPIBasicAuth.svc?wsdl", header=self.header, namespace="http://atomia.com/atomia/provisioning/", trace=False)
        return client.CreateService(
                                    serviceName = service_name,
                                    parentService = parent_service,
                                    accountName = account_number)
        
    def find_services_by_path_with_paging(self, search_criteria_list, account_number, search_properties = None,  sort_by_prop_name = '', sort_asc = 'true', page_number ='0', page_size = '100'):

        return self.client.FindServicesByPathWithPaging(searchCriteriaList = search_criteria_list,
                                                 account = account_number,
                                                 sortByPropName = sort_by_prop_name,
                                                 sortAsc = sort_asc,
                                                 pageNumber = page_number,
                                                 pageSize = page_size)
        
#    def get_action_result_as_simple_xml(self, action_result):
#        for k in action_result:
#            return k
        
        