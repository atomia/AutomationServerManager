'''
Created on Nov 7, 2011

@author: Dusan
'''
from pysimplesoap_atomia.client import SoapClient
import ConfigParser, os

class AtomiaActions(object):
    
    def __init__(self, username = None, password = None, api_url = None, accountapi_url = None, bootstrap = False, soap_header = None, body_xmlns = None, account_body_xmlns = None):
       
        self.username = username
        self.password = password
        self.api_url = api_url
        self.accountapi_url = accountapi_url
        self.bootstrap = bootstrap
        
        if soap_header is None:
            
            if self.bootstrap:
                self.header = """<soap:Header xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                            xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
            </soap:Header>"""
            
            else:

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
            
            self.header = self.header
        else:
            self.header = soap_header
            
        if body_xmlns is None:
            self.body_xmlns = 'xmlns:prov="http://atomia.com/atomia/provisioning/" xmlns:atom="http://schemas.datacontract.org/2004/07/Atomia.Provisioning.Base" xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays"'
        else:
            self.body_xmlns = body_xmlns
            
        if account_body_xmlns is None:
            self.account_body_xmlns = 'xmlns:acc="http://atomia.com/atomia/accountapi/" xmlns:account="http://schemas.datacontract.org/2004/07/Atomia.Account.Lib.BusinessObjects" xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays"'
        else:
            self.account_body_xmlns = account_body_xmlns
            
        self.client = SoapClient(wsdl=self.api_url, header=self.header, body_xmlns= self.body_xmlns, namespace="http://atomia.com/atomia/provisioning/", trace=False)
        if accountapi_url is None:
            self.account_client = None
        else:
            self.account_client = SoapClient(wsdl=self.accountapi_url, header=self.header, body_xmlns= self.account_body_xmlns, namespace="http://atomia.com/atomia/accountapi/", trace=False)
        
    def get_account_for_user(self, user, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.account_client.GetAccountForUser( username, password, username = user )
    
    def get_accountid_for_user(self, user, username = None, password = None):
        
        account = self.get_account_for_user( user = user, username = username, password = password )
        x = account["GetAccountForUserResult"]
        for b in x.children():
            local_name = b.get_local_name()
            if local_name == 'Name':
                account_id = str(b)
        return account_id
    
    def list_accounts(self, page_number = "0", page_size = "100", username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.ListAccountsWithPagination(username, password, pageNumber = page_number, pageSize = page_size, sortAsc = "true")
    
    def get_account(self, account_number, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password        
        return self.client.GetAccount( username, password, accountId = account_number, username = None, password = None ) 
    
    def add_account(self, account, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password       
        return self.client.AddAccount(username, password, account = account, username = None, password = None)
    
    def delete_account(self, account_number, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password        
        return self.client.DeleteAccount( username, password, accountId = account_number )
        
    def list_packages(self, account_number, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password        
        return self.client.ListPackagesForAccount( username, password, accountName = account_number )
    
    def add_package(self, account_number, package, arguments = None, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password        
        return self.client.AddPackageForAccount( username, password, accountName = account_number, package = package, arguments = arguments )
    
    def delete_package(self, account_number, package, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password       
        return self.client.DeletePackageForAccount( username, password, accountName = account_number, package = package )
    
    def create_service(self, service_name, parent_service, account_number, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.CreateService(username, password, 
                                    serviceName = service_name,
                                    parentService = parent_service,
                                    accountName = account_number)
        
    def add_service(self, service, parent_service, account_number, resource_request_descriptions = None, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.AddService(username, password, 
                                    service = service,
                                    parentService = parent_service,
                                    accountName = account_number,
                                    resourceRequestDescriptions = resource_request_descriptions)
        
    def delete_service(self, service, account_number, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.DeleteService(username, password, 
                                    service = service,
                                    accountName = account_number)
        
        
    def modify_service (self, service, account_number, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.ModifyService(username, password, 
                                    service = service,
                                    accountName = account_number)

        
    def find_services_by_path_with_paging(self, search_criteria_list, account_number, search_properties = None,  sort_by_prop_name = '', sort_asc = 'true', page_number ='0', page_size = '100', username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.FindServicesByPathWithPaging(username, password, searchCriteriaList = search_criteria_list,
                                                 properties = search_properties,
                                                 account = account_number,
                                                 sortByPropName = sort_by_prop_name,
                                                 sortAsc = sort_asc,
                                                 pageNumber = page_number,
                                                 pageSize = page_size)
        
    def get_service_by_id(self, account_number, service_id, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.GetServiceById(username, password, accountId = account_number,
                                          serviceID = service_id)
        
    def list_existing_service(self, parent_service, account_number, get_logical_children = 'true', sort_asc = 'true', page_number ='0', page_size = '100', username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.ListExistingServices(username, password, parentService = parent_service,
                                                getLogicalChildren = get_logical_children,
                                                accountId = account_number,
                                                sortAsc = sort_asc,
                                                pageNumber = page_number,
                                                pageSize = page_size)