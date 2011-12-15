class AtomiaAccount(object):
    def __init__(self, account_id = None, account_description = None, current_request_id = None, account_properties = None, 
                 is_active = None, provisioning_description = None):
         
            self.account_id = account_id
            self.account_description = account_description
            self.current_request_id = current_request_id
            self.account_properties = account_properties
            self.is_active = is_active
            self.provisioning_description = provisioning_description
            
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
    
    def from_simplexml(self, simple_xml_element):
        if simple_xml_element is None:
            return
        if (simple_xml_element.get_local_name() == 'ProvisioningAccount'):
            self.initialize_properties(simple_xml_element)
        else:
            found = False
            if simple_xml_element.children() is not None and len(simple_xml_element.children()) > 0:
                for k in simple_xml_element.children():
                    if (k.get_local_name() == 'AccountId'):
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
            if local_name == 'AccountId':
                self.account_id = str(b)
            elif local_name == 'AccountDescription':
                self.account_description = str(b)
            elif local_name == 'CurrentRequestId':
                self.current_request_id = str(b)
            elif local_name == 'IsActive':
                self.is_active = str(b)
            elif local_name == 'ProvisioningDescription':
                self.provisioning_description = str(b)
            elif local_name == 'AccountProperties':
                self.account_properties = []
                if b.children() is not None and len(b.children()) > 0:
                    for j in b.children():
                        tmp_property = AtomiaAccountProperty()
                        tmp_property.from_simplexml(j)
                        self.account_properties.append(tmp_property)
                        
                        
    def to_xml_friendly_object(self, xml_tag_with_namespace = None, xml_tag = None):
        
        xml_friendly = {}
        
        if xml_tag_with_namespace is not None:
            xml_friendly['xml_tag_with_namespace'] = xml_tag_with_namespace
        
        if xml_tag is not None:
            xml_friendly['xml_tag'] = xml_tag
        
        if self.account_description is not None:
            xml_friendly['account_description'] = { 'xml_tag_with_namespace' : 'atom:AccountDescription', 
                                        'xml_tag' : 'AccountDescription',
                                        'value' : self.account_description,
                                        'order' : 1
                                    }
         
        if self.account_id is not None:
            xml_friendly['account_id'] = { 'xml_tag_with_namespace' : 'atom:AccountId', 
                                        'xml_tag' : 'AccountId',
                                        'value' : self.account_id,
                                        'order' : 2
                                    }   
            
        if self.current_request_id is not None:
            xml_friendly['current_request_id'] = { 'xml_tag_with_namespace' : 'atom:CurrentRequestId', 
                                        'xml_tag' : 'CurrentRequestId',
                                        'value' : self.current_request_id,
                                        'order' : 4
                                    }
            
        if self.is_active is not None:
            xml_friendly['is_active'] = { 'xml_tag_with_namespace' : 'atom:IsActive', 
                                        'xml_tag' : 'IsActive',
                                        'value' : self.is_active,
                                        'order' : 5
                                    }
            
        if self.provisioning_description is not None:
            xml_friendly['provisioning_description'] = { 'xml_tag_with_namespace' : 'atom:ProvisioningDescription', 
                                        'xml_tag' : 'ProvisioningDescription',
                                        'value' : self.provisioning_description,
                                        'order' : 6
                                    }
            
        if self.account_properties is not None and len(self.account_properties) > 0:
            
            properties_list = []
            for proper in self.account_properties:
                properties_list.append(AtomiaAccountProperty(key = proper, value = self.account_properties[proper]).to_xml_friendly_object("arr:KeyValueOfstringstring", "KeyValueOfstringstring"))
            
            xml_friendly['account_properties'] = { 'xml_tag_with_namespace' : 'atom:AccountProperties', 
                                        'xml_tag' : 'AccountProperties',
                                        'value' : properties_list,
                                        'order' : 3
                                    }
        
        else: 
            xml_friendly['account_properties'] = { 'xml_tag_with_namespace' : 'atom:AccountProperties', 
                                        'xml_tag' : 'AccountProperties',
                                        'value' : '',
                                        'order' : 3
                                    }

        return xml_friendly

class AtomiaAccountProperty(object):
    def __init__(self, key = None, value = None):
        
        self.key = key
        self.value = value
        return
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
            
    def from_simplexml(self, simple_xml_element):
        if (simple_xml_element.get_local_name() == 'KeyValueOfstringstring' or simple_xml_element.get_local_name() == 'KeyValueOfstringint'):
            self.initialize_properties(simple_xml_element)
        else:
            found = False
            if len(simple_xml_element.children()) > 0:
                for k in simple_xml_element.children():
                    if (k.get_local_name() == 'Key'):
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
            if local_name == 'Key':
                self.key = str(b)
            elif local_name == 'Value':
                self.value = str(b)
            
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

class AtomiaPackage(object):
    def __init__(self, package_id = None, package_name = None, current_request_id = None, disable_script_name = None, package_extensions = None):
         
            self.package_id = package_id
            self.package_name = package_name
            self.current_request_id = current_request_id
            self.disable_script_name = disable_script_name
            self.package_extensions = package_extensions
            
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
    
    def from_simplexml(self, simple_xml_element):
        if simple_xml_element is None:
            return
        if (simple_xml_element.get_local_name() == 'ProvisioningPackage'):
            self.initialize_properties(simple_xml_element)
        else:
            found = False
            if simple_xml_element.children() is not None and len(simple_xml_element.children()) > 0:
                for k in simple_xml_element.children():
                    if (k.get_local_name() == 'ID'):
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
                self.package_id = str(b)
            elif local_name == 'Name':
                self.package_name = str(b)
            elif local_name == 'CurrentRequestId':
                self.current_request_id = str(b)
            elif local_name == 'DisableScriptName':
                self.disable_script_name = str(b)
            elif local_name == 'PackageExtensions':
                self.package_extensions = []
                if b.children() is not None and len(b.children()) > 0:
                    for j in b.children():
                        tmp_property = AtomiaPackageExtension()
                        tmp_property.from_simplexml(j)
                        self.package_extensions.append(tmp_property)
                        
                        
    def to_xml_friendly_object(self, xml_tag_with_namespace = None, xml_tag = None):
        
        xml_friendly = {}
        
        if xml_tag_with_namespace is not None:
            xml_friendly['xml_tag_with_namespace'] = xml_tag_with_namespace
        
        if xml_tag is not None:
            xml_friendly['xml_tag'] = xml_tag
        
        if self.current_request_id is not None:
            xml_friendly['current_request_id'] = { 'xml_tag_with_namespace' : 'atom:CurrentRequestId', 
                                        'xml_tag' : 'CurrentRequestId',
                                        'value' : self.current_request_id,
                                        'order' : 1
                                    }
         
        if self.disable_script_name is not None:
            xml_friendly['disable_script_name'] = { 'xml_tag_with_namespace' : 'atom:DisableScriptName', 
                                        'xml_tag' : 'DisableScriptName',
                                        'value' : self.disable_script_name,
                                        'order' : 2
                                    }   
            
        if self.package_id is not None:
            xml_friendly['package_id'] = { 'xml_tag_with_namespace' : 'atom:ID', 
                                        'xml_tag' : 'ID',
                                        'value' : self.package_id,
                                        'order' : 3
                                    }
            
        if self.package_name is not None:
            xml_friendly['package_name'] = { 'xml_tag_with_namespace' : 'atom:Name', 
                                        'xml_tag' : 'Name',
                                        'value' : self.package_name,
                                        'order' : 4
                                    }
            
        xml_friendly['package_extensions'] = { 'xml_tag_with_namespace' : 'atom:PackageExtensions', 
                                        'xml_tag' : 'PackageExtensions',
                                        'value' : '',
                                        'order' : 5
                                    }

        return xml_friendly

class AtomiaPackageExtension(object):
    def __init__(self, id = None, name = None):
        
        self.id = id
        self.name = name
        self.limitiation_overrides = []
        return
    
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]
            
    def from_simplexml(self, simple_xml_element):
        if len(simple_xml_element.children()) > 0:
            for k in simple_xml_element.children():
                local_name = k.get_local_name()
                if local_name == 'ID':
                    self.id = str(k)
                elif local_name == 'Name':
                    self.name = str(k)
                elif local_name == "LimitationsOverrides":
                    tmp_override = AtomiaAccountProperty()
                    tmp_override.from_simplexml(k.children())
                    self.limitiation_overrides.append(tmp_override)
    
    def print_me(self):
        import json
        print json.dumps(self, default=encode_me, indent=4)
    
#    def initialize_properties(self, k):
#        for b in k.children():
#            local_name = b.get_local_name()
#            if local_name == 'Key':
#                self.key = str(b)
#            elif local_name == 'Value':
#                self.value = str(b)
            
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
    
    def to_xml_friendly_object(self, xml_tag_with_namespace = None, xml_tag = None):
        
        xml_friendly = {}
        
        if xml_tag_with_namespace is not None:
            xml_friendly['xml_tag_with_namespace'] = xml_tag_with_namespace
        
        if xml_tag is not None:
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
        if self.properties is not None and len(self.properties) > 0:
            
            properties_list = []
            for proper in self.properties:
                properties_list.append(AtomiaServiceProperty(id = None, is_key = None, name = proper.name, property_type = None, prop_string_value = proper.prop_string_value).to_xml_friendly_object("atom:ProvisioningServiceProperty", "ProvisioningServiceProperty"))
            
            xml_friendly['properties'] = { 'xml_tag_with_namespace' : 'atom:properties', 
                                        'xml_tag' : 'properties',
                                        'value' : properties_list,
                                        'order' : 9
                                    }
        
        else: 
            xml_friendly['properties'] = { 'xml_tag_with_namespace' : 'atom:properties', 
                                        'xml_tag' : 'properties',
                                        'value' : '',
                                        'order' : 9
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
    
    def to_print_friendly(self, display_parent = True, display_parent_id = False):
        if display_parent:
            return self
        elif display_parent_id:
            from copy import deepcopy
            copied = deepcopy(self)
            tmp_dict = copied.__dict__
            if tmp_dict.has_key('parent'):
                tmp_dict['parent_id'] = tmp_dict['parent'].logical_id
                del tmp_dict['parent']
            return copied
        else:
            from copy import deepcopy
            copied = deepcopy(self)
            tmp_dict = copied.__dict__
            if tmp_dict.has_key('parent'):
                del tmp_dict['parent']
            return copied
            
    def print_me(self, display_parent = True, display_parent_id = False, filter = None):
        import json
        if display_parent:
            result = json.dumps(self, default=encode_me, indent=4)
        elif display_parent_id:
            result = json.dumps(self, default=encode_me_with_parent_id, indent=4)
        else:
            result = json.dumps(self, default=encode_me_without_parent, indent=4)

        if filter is not None:
            import jsonpath
            jsonpath.jsonpath(result, filter)

        print result
    
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
                if b.children() is not None and len(b.children()) > 0:
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
        
        if self.id is not None:
            xml_friendly['id'] = { 'xml_tag_with_namespace' : 'atom:ID', 
                                              'xml_tag' : 'ID',
                                              'value' : self.id,
                                              'order' : 1
                                              }
         
        if self.is_key is not None:
            xml_friendly['is_key'] = { 'xml_tag_with_namespace' : 'atom:IsKey', 
                                              'xml_tag' : 'IsKey',
                                              'value' : self.is_key,
                                              'order' : 2
                                            }
            
        if self.name is not None:
            xml_friendly['name'] = { 'xml_tag_with_namespace' : 'atom:Name', 
                                              'xml_tag' : 'Name',
                                              'value' : self.name,
                                              'order' : 3
                                            }
            
        if self.property_type is not None:
            xml_friendly['property_type'] = { 'xml_tag_with_namespace' : 'atom:PropertyType', 
                                              'xml_tag' : 'PropertyType',
                                              'value' : self.property_type,
                                              'order' : 4
                                            }
            
            
        if self.prop_string_value is not None:
            xml_friendly['prop_string_value'] = { 'xml_tag_with_namespace' : 'atom:propStringValue', 
                                              'xml_tag' : 'propStringValue',
                                              'value' : self.prop_string_value,
                                              'order' : 5
                                            }
        return xml_friendly

def encode_me(obj):
    return obj.__dict__
              
def encode_me_without_parent(obj):
    from copy import deepcopy
    tmp_dict = deepcopy(obj.__dict__)
    if tmp_dict.has_key('parent'):
        del tmp_dict['parent']
    return tmp_dict

def encode_me_with_parent_id(obj):
    from copy import deepcopy
    tmp_dict = deepcopy(obj.__dict__)
    if tmp_dict.has_key('parent'):
        tmp_dict['parent_id'] = tmp_dict['parent'].logical_id
        del tmp_dict['parent']
    return tmp_dict
