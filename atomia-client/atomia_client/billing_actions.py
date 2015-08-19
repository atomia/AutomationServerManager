from pysimplesoap_atomia.client import SoapClient
import ConfigParser, os

class BillingActions(object):

    def __init__(self, username = None, password = None, api_url = None, accountapi_url = None, bootstrap = False, soap_header = None, body_xmlns = None, debug = False):

        self.username = username
        self.password = password
        self.api_url = api_url
        self.accountapi_url = accountapi_url
        self.bootstrap = bootstrap
        self.debug = debug

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
            self.body_xmlns = 'xmlns:bil="http://atomia.com/billing/"'
        else:
            self.body_xmlns = body_xmlns


        self.client = SoapClient(wsdl=self.api_url, header=self.header, body_xmlns= self.body_xmlns, namespace="http://atomia.com/billing/", trace=self.debug)

    def get_account(self, account_number, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.GetAccountByName( username, password, accountName = account_number )

    def send_email(self, account_number, template, properties, username = None, password = None):
        username = self.username if username == None else username
        password = self.password if password == None else password
        return self.client.SendMailToAccountOwner( username, password, accountName = account_number, templateName = template, templateProperties = properties)
