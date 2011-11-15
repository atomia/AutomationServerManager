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
              friendly_name = None, logical_id = None, name = None, physical_id = None, properties = None, provisioning_description = None, parent = None):
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
        self.parent = parent
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
            
        xml_friendly['parent'] = { 'xml_tag_with_namespace' : 'atom:Parent', 
                                    'xml_tag' : 'Parent',
                                    'value' : '',
                                    'order' : 2
                                }
        return xml_friendly
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
    
    def from_simplexml(self, simple_xml_element):
        if simple_xml_element is None:
            return
        if (simple_xml_element.get_local_name() == 'ProvisioningService'):
            self.initialize_properties(simple_xml_element)
        else:
            found = False
            if simple_xml_element.children() is not None and len(simple_xml_element.children()) > 0:
                for k in simple_xml_element.children():
                    if (k.get_local_name() == 'logicalId'):
                        found = True
            
            if found:
                self.initialize_properties(simple_xml_element)
            else:  
                self.from_simplexml(simple_xml_element.children())
    
    def print_me(self):
        import json
        print json.dumps(self, default=encode_me, indent=4)
    
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
            elif local_name == 'properties':
                self.properties = []
                for j in b.children():
                    tmp_property = AtomiaServiceProperty()
                    tmp_property.from_simplexml(j)
                    self.properties.append(tmp_property)
            elif local_name == 'Parent':
                tmp_property = AtomiaService()
                tmp_property.from_simplexml(b)
                self.parent = tmp_property

class AtomiaServiceSearchCriteria(object):
    def __init__(self, service_name, service_path, parent_service = None):
        
        self.service_name = service_name
        self.service_path = service_path
        self.parent_service = parent_service
        return
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
            
    def to_xml_friendly_object(self, xml_tag_with_namespace, xml_tag):
        
        xml_friendly = {}
        
        xml_friendly['xml_tag_with_namespace'] = xml_tag_with_namespace
        
        xml_friendly['xml_tag'] = xml_tag
        
        if self.service_name is not None:
            xml_friendly['service_name'] = { 'xml_tag_with_namespace' : 'atom:ServiceName', 
                                              'xml_tag' : 'ServiceName',
                                              'value' : self.service_name,
                                              'order' : 1
                                              }
         
        if self.service_path is not None:
            xml_friendly['service_path'] = { 'xml_tag_with_namespace' : 'atom:ServicePath', 
                                              'xml_tag' : 'ServicePath',
                                              'value' : self.service_path,
                                              'order' : 2
                                            }
            
        if self.parent_service is not None:
            xml_friendly['parent_service'] = { 'xml_tag_with_namespace' : 'atom:ParentService', 
                                              'xml_tag' : 'ParentService',
                                              'value' : self.parent_service,
                                              'order' : 0
                                            }
        return xml_friendly


class AtomiaServiceSearchCriteriaProperty(object):
    def __init__(self, key, value):
        
        self.key = key
        self.value = value
        return
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
            
    def to_xml_friendly_object(self, xml_tag_with_namespace, xml_tag):
        
        xml_friendly = {}
        
        xml_friendly['xml_tag_with_namespace'] = xml_tag_with_namespace
        
        xml_friendly['xml_tag'] = xml_tag
        
        if self.key is not None:
            xml_friendly['key'] = { 'xml_tag_with_namespace' : 'arr:Key', 
                                              'xml_tag' : 'Key',
                                              'value' : self.key,
                                              'order' : 1
                                            }
        if self.value is not None:
            xml_friendly['value'] = { 'xml_tag_with_namespace' : 'arr:Value', 
                                              'xml_tag' : 'Value',
                                              'value' : self.value,
                                              'order' : 2
                                              }
         
        return xml_friendly

class AtomiaServiceProperty(object):
    def __init__(self, id = None, is_key = None, name = None, property_type = None, prop_string_value = None):
        
        self.id = id
        self.is_key = is_key
        self.name = name
        self.property_type = property_type
        self.prop_string_value = prop_string_value
        return
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
            
    def from_simplexml(self, simple_xml_element):
        if (simple_xml_element.get_local_name() == 'ProvisioningServiceProperty'):
            self.initialize_properties(simple_xml_element)
        else:
            found = False
            if len(simple_xml_element.children()) > 0:
                for k in simple_xml_element.children():
                    if (k.get_local_name() == 'PropertyType'):
                        found = True
            
            if found:
                self.initialize_properties(simple_xml_element)
            else:  
                self.from_simplexml(simple_xml_element.children())
    
    def print_me(self):
        import json
        print json.dumps(self, default=encode_me, indent=4)
    
    def initialize_properties(self, k):
        for b in k.children():
            local_name = b.get_local_name()
            if local_name == 'ID':
                self.id = str(b)
            elif local_name == 'IsKey':
                self.is_key = str(b)
            elif local_name == 'Name':
                self.name = str(b)
            elif local_name == 'PropertyType':
                self.property_type = str(b)
            elif local_name == 'propStringValue':
                self.prop_string_value = str(b)
            
    def to_xml_friendly_object(self, xml_tag_with_namespace, xml_tag):
        
        xml_friendly = {}
        
        xml_friendly['xml_tag_with_namespace'] = xml_tag_with_namespace
        
        xml_friendly['xml_tag'] = xml_tag
        
        if self.service_name is not None:
            xml_friendly['service_name'] = { 'xml_tag_with_namespace' : 'atom:ServiceName', 
                                              'xml_tag' : 'ServiceName',
                                              'value' : self.service_name,
                                              'order' : 1
                                              }
         
        if self.service_path is not None:
            xml_friendly['service_path'] = { 'xml_tag_with_namespace' : 'atom:ServicePath', 
                                              'xml_tag' : 'ServicePath',
                                              'value' : self.service_path,
                                              'order' : 2
                                            }
            
        if self.parent_service is not None:
            xml_friendly['parent_service'] = { 'xml_tag_with_namespace' : 'atom:ParentService', 
                                              'xml_tag' : 'ParentService',
                                              'value' : self.parent_service,
                                              'order' : 0
                                            }
        return xml_friendly

def encode_me(obj):
    return obj.__dict__
