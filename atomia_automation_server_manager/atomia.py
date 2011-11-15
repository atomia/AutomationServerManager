'''
Created on Nov 7, 2011

@author: Dusan
'''
import time
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from datetime import datetime
from atomia_entities import AtomiaAccount, AtomiaService, AtomiaServiceSearchCriteria
from atomia_actions import AtomiaActions

if __name__=="__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Atomia Automation Server Manager', prog='atomia')
    parser.add_argument('--username', help="The API user's username")
    parser.add_argument('--password', help="The API user's password")
    parser.add_argument('--api_url', help="The URL of the Automation Server API service")
    parser.add_argument('--entity', help='account|package|service')
    parser.add_argument('--action', help='list|find|add|delete|modify')
    parser.add_argument('--account', help='The account number in Automation Server')
    parser.add_argument('--service_locator', help='The JSON representation of the path to the given service')
    parser.add_argument('--service', help='The JSON representation of the given service')
    args = parser.parse_args()
    
    manager = AtomiaActions(args.username if args.username is not None else 'Administrator', args.password if args.password is not None else 'Administrator')

#    import pprint
#    created_service = manager.create_service('CsDatabase', None, '100002')
#    
#    test = AtomiaService()
#    test.from_simplexml(created_service.itervalues().next())

    service_search_criteria_list = []
    tmp_ssc = AtomiaServiceSearchCriteria('CsLinuxWebsite', 'CsBase')
    service_search_criteria_list.append(tmp_ssc.to_xml_friendly_object('atom:ServiceSearchCriteria', 'ServiceSearchCriteria'))
#    tmp_ssc = AtomiaServiceSearchCriteria('CsWindowsWebsite', 'CsBase')
#    service_search_criteria_list.append(tmp_ssc)
    test = manager.find_services_by_path_with_paging(service_search_criteria_list, '100002')

    for k in test.itervalues().next().children():
        test2 = AtomiaService()
        test2.from_simplexml(k)
        test2.print_me()
        
        service_search_criteria_list = []
        xml_fr = test2.to_xml_friendly_object('atom:ParentService', 'ParentService')
        tmp_ssc = AtomiaServiceSearchCriteria('MailAccount', 'CsMailSupport/MailDomain', xml_fr)
        service_search_criteria_list.append(tmp_ssc.to_xml_friendly_object('atom:ServiceSearchCriteria', 'ServiceSearchCriteria'))
        test3 = manager.find_services_by_path_with_paging(service_search_criteria_list, '100002')
        
        for j in test3.itervalues().next().children():
            test4 = AtomiaService()
            test4.from_simplexml(j)
            test4.print_me()
    
    
    
#    a = client.CreateService(
#                         serviceName = 'CsDatabase',
#                         parentService = None,
#                         accountName = '100002'
#                         )
#    
#    test = AtomiaService()
#    test.from_simplexml(a)
#    
#    for k in a:
#        for b in a[k].children():
#            if (b.get_local_name() == 'logicalId'):
#                client.AddService(service = a[k], 
#                                  parentService = None,
#                                  accountName = '100002',
#                                  resourceRequestDescriptions = None
#                                  ) 
#    import pprint
#a = client.ListAccounts()
#    pprint.pprint(a['ListAccountsResult'].children()[0].as_xml())
    
#    account = AtomiaAccount('dusantest55', is_active = 'true', provisioning_description = 'ProvisioningDescription', namespace = 'atom:').account
#    manager.add_account(account)
    
#    account = {
#               #'atom:AccountDescription' : None,
#               'atom:AccountId' : 'dusantest14',
#               #'atom:AccountProperties': None,
#               #'atom:CurrentRequestId' : None,
#               'atom:IsActive' : 'true',
#               'atom:ProvisioningDescription' : 'ProvisioningDescription'
#               }
    
#    params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
#<soap:Envelope 
#    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
#    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
#    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#    xmlns:prov="http://atomia.com/atomia/provisioning/" 
#    xmlns:atom="http://schemas.datacontract.org/2004/07/Atomia.Provisioning.Base" 
#    xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
#         <prov:account>
#            <atom:AccountDescription>desc</atom:AccountDescription>
#            <atom:AccountId>dusantest</atom:AccountId>
#            <atom:IsActive>true</atom:IsActive>
#            <atom:ProvisioningDescription>ProvisioningDescription</atom:ProvisioningDescription>
#         </prov:account>
#</soap:Envelope>""")
#    
#    client.call('AddAccount',params)

   
#client.call('ListAccounts')

    
# client.AddAccount(account = a)
#    for k in a:
#        pprint.pprint(len(a[k].children()))
#        for b in a[k].children():
#            for c in b.children():
#                pprint.pprint(c)
      
#    client.AddAccount(
#                        account = {
#                                   'AccountDescription' : None,
#                                   'AccountId' : 'dusantest',
#                                   'AccountProperties': None,
#                                   'CurrentRequestId' : None,
#                                   'IsActive' : 'true',
#                                   'ProvisioningDescription' : 'ProvisioningDescription'
#                                   
#                                   }
#                         ) 
        
        


'''for service in client.services.values():
    for port in service['ports'].values():
        print port['location']
        for op in port['operations'].values():
            print 'Name:', op['name']
            print 'Docs:', op['documentation'].strip()
            print 'SOAPAction:', op['action']
            print 'Input', op['input'] # args type declaration
            print 'Output', op['output'] # returns type declaration
            print'''