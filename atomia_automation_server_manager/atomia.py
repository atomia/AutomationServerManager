'''
Created on Nov 7, 2011

@author: Dusan
'''
import time
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from datetime import datetime
from atomia_entities import AtomiaAccount, AtomiaService
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

#   client = SoapClient(wsdl="file:///C:/Users/Dusan/PythonWorkspace/Test2/src/wsdl0.xml", header=header, namespace="http://atomia.com/atomia/provisioning/", trace=False)
    
#    client = SoapClient(wsdl=args.api_url if args.api_url is not None else "https://provisioning.testgui.atomiademo.com/CoreAPIBasicAuth.svc?wsdl", header=manager.header, namespace="http://atomia.com/atomia/provisioning/", trace=False)
    
    import pprint
    created_service = manager.create_service('CsDatabase', None, '100002')
    
    test = AtomiaService()
    test.from_simplexml(created_service)
    
#    a = client.CreateService(
#                         serviceName = 'CsDatabase',
#                         parentService = None,
#                         accountName = '100002'
#                         )
#    
#   
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