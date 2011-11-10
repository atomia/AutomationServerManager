'''
Created on Nov 7, 2011

@author: Dusan
'''
import time
from pysimplesoap.client import SoapClient
from datetime import datetime

created     = datetime.fromtimestamp(time.mktime(time.gmtime()))
created     = created.strftime('%Y-%m-%dT%H:%M:%SZ')

expires     = datetime.fromtimestamp(time.mktime(time.gmtime()) + 300)
expires     = expires.strftime('%Y-%m-%dT%H:%M:%SZ')

username = 'Administrator'
password = 'Administrator'

header = """<soap:Header xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
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

header = header % dict(Created=created, Expires=expires, Username = username, Password = password)

'''client = SoapClient(wsdl="file:///C:/Users/Dusan/PythonWorkspace/Test2/src/wsdl0.xml", header=header, namespace="http://atomia.com/atomia/provisioning/", trace=False)'''

client = SoapClient(wsdl="https://provisioning.testgui.atomiademo.com/CoreAPIBasicAuth.svc?wsdl", header=header, namespace="http://atomia.com/atomia/provisioning/", trace=False)

for k in next(client.ListAccounts().itervalues())('a:AccountId'):
    print k

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