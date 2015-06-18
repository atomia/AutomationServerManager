class BillingAccount(object):
    def __init__(self, account_id = None, account_description = None, current_request_id = None, account_properties = None,
                 is_active = None, provisioning_description = None):
            self.properties = {}

    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]

    def from_simplexml(self, simple_xml_element):
        if simple_xml_element is None:
            return
        self.parse_elements(simple_xml_element)

    def parse_elements(self, x):
        for p in x.children():
            self.properties[p.get_local_name()] = str(p)
            if p.children() is not None and len(p.children()) > 0:
                tmpChild = {}
                for c in p.children():
                    tmpChild[c.get_local_name()] = str(c)
                self.properties[p.get_local_name()] = tmpChild


    def print_me(self):
        import json
        print json.dumps(self.properties, default=encode_me, indent=4)


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

def encode_me(obj):
    return obj.__dict__
