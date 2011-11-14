class AtomiaAccount(object):
     def __init__(self, account_id, account_description = None, current_request_id = None,
                 is_active = False, provisioning_description = None, namespace = ''):
         
            self.account = {
               '%sAccountId' % namespace : account_id,
            }
            
            if (account_description is not None):
                self.account['%sAccountDescription' % namespace] = account_description
                
            if (current_request_id is not None):
                self.account['%sCurrentRequestId' % namespace] = current_request_id
                
            if (is_active is not None):
                self.account['%sCurrentRequestId' % namespace] = is_active
                
            if (provisioning_description is not None):
                self.account['%sProvisioningDescription' % namespace] = provisioning_description
         

class AtomiaServiceProperty(object):
    def __init__(self, id = None, is_key = None, name = None, property_type = None, prop_string_value = None):
        return


class AtomiaService(object):
    def __init__(self, account_owner_id = None, current_request_id = None, status = None, disabled = None, 
              friendly_name = None, logical_id = None, name = None, physical_id = None, properties = None, provisioning_description = None):
        self.logical_id = logical_id
        self.account_owner_id = account_owner_id
        self.physical_id = physical_id
        self.current_request_id = current_request_id
        self.status = status
        self.disabled = disabled
        self.friendly_name = friendly_name
        self.name = name
        self.properties = properties
        self.provisioning_description = provisioning_description
        return
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
    
    def from_simplexml(self, simple_xml_element):
        import pprint
        for k in simple_xml_element:
#            pprint.pprint(simple_xml_element[k].children()['a:logicalId'])
            for b in simple_xml_element[k].children():
                local_name = b.get_local_name()
                if local_name == 'logicalId':
                    self.logical_id = str(b)
                elif local_name == 'AccountOwnerId':
                    self.account_owner_id = str(b)
                elif local_name == 'physicalId':
                    self.physical_id = str(b)
                elif local_name == 'CurrentRequestId':
                    self.current_request_id = str(b)
                elif local_name == 'Status':
                    self.status = str(b)
                elif local_name == 'disabled':
                    self.disabled = str(b)
                elif local_name == 'friendlyName':
                    self.friendly_name = str(b)
                elif local_name == 'name':
                    self.name = str(b)
                elif local_name == 'provisioningDescription':
                    self.provisioning_description = str(b)
#                for c in b.children():
#                    pprint.pprint(c)

        for k, v in self.__dict__.iteritems():
            print k, v
