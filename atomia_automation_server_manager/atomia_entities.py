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
    
    def to_xml_friendly_object(self, xml_tag_with_namespace, xml_tag):
        
        xml_friendly = {}
        
        xml_friendly['xml_tag_with_namespace'] = xml_tag_with_namespace
        
        xml_friendly['xml_tag'] = xml_tag
        
        if self.logical_id is not None:
            xml_friendly['logical_id'] = { 'xml_tag_with_namespace' : 'atom:logicalId', 
                                        'xml_tag' : 'logicalId',
                                        'value' : self.logical_id,
                                        'order' : 6
                                    }
         
        if self.account_owner_id is not None:
            xml_friendly['account_owner_id'] = { 'xml_tag_with_namespace' : 'atom:AccountOwnerId', 
                                        'xml_tag' : 'AccountOwnerId',
                                        'value' : self.account_owner_id,
                                        'order' : 0
                                    }   
            
        if self.physical_id is not None:
            xml_friendly['physical_id'] = { 'xml_tag_with_namespace' : 'atom:physicalId', 
                                        'xml_tag' : 'physicalId',
                                        'value' : self.physical_id,
                                        'order' : 8
                                    }
            
        if self.current_request_id is not None:
            xml_friendly['current_request_id'] = { 'xml_tag_with_namespace' : 'atom:CurrentRequestId', 
                                        'xml_tag' : 'CurrentRequestId',
                                        'value' : self.current_request_id,
                                        'order' : 1
                                    }
            
        if self.status is not None:
            xml_friendly['status'] = { 'xml_tag_with_namespace' : 'atom:Status', 
                                        'xml_tag' : 'Status',
                                        'value' : self.status,
                                        'order' : 3
                                    }
            
        if self.disabled is not None:
            xml_friendly['disabled'] = { 'xml_tag_with_namespace' : 'atom:disabled', 
                                        'xml_tag' : 'disabled',
                                        'value' : self.disabled,
                                        'order' : 4
                                    }
            
        if self.friendly_name is not None:
            xml_friendly['friendly_name'] = { 'xml_tag_with_namespace' : 'atom:friendlyName', 
                                        'xml_tag' : 'friendlyName',
                                        'value' : self.friendly_name,
                                        'order' : 5
                                    }
            
        if self.name is not None:
            xml_friendly['name'] = { 'xml_tag_with_namespace' : 'atom:name', 
                                        'xml_tag' : 'name',
                                        'value' : self.name,
                                        'order' : 7
                                    }

        if self.provisioning_description is not None:
            xml_friendly['provisioning_description'] = { 'xml_tag_with_namespace' : 'atom:provisioningDescription', 
                                        'xml_tag' : 'provisioningDescription',
                                        'value' : self.provisioning_description,
                                        'order' : 10
                                    }
        return xml_friendly
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
    
    def from_simplexml(self, simple_xml_element):
        import pprint
        if (simple_xml_element.get_local_name() == 'ProvisioningService'):
            self.initialize_properties(simple_xml_element)
        else:
            found = False
            if len(simple_xml_element.children()) > 0:
                for k in simple_xml_element.children():
                    if (k.get_local_name() == 'logicalId'):
                        found = True
            
            if found:
                self.initialize_properties(simple_xml_element)
            else:  
                self.from_simplexml(simple_xml_element.children())
    
    def print_me(self):
        for k, v in self.__dict__.iteritems():
            print k, v
    
    def initialize_properties(self, k):
        for b in k.children():
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

class AtomiaServiceSearchCriteria(object):
    def __init__(self, service_name, service_path, parent_service = None):
        
        self.xml_tag_with_namespace = 'atom:ServiceSearchCriteria'
        
        self.xml_tag = 'ServiceSearchCriteria'
        
        self.service_name = { 'xml_tag_with_namespace' : 'atom:ServiceName', 
                              'xml_tag' : 'ServiceName',
                              'value' : service_name
                              }
        self.service_path = { 'xml_tag_with_namespace' : 'atom:ServicePath', 
                              'xml_tag' : 'ServicePath',
                              'value' : service_path
                            }
        
        if parent_service is not None:
         
            self.parent_service = { 'xml_tag_with_namespace' : 'atom:ParentService', 
                                  'xml_tag' : 'ParentService',
                                  'value' : parent_service
                                }
        return
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
