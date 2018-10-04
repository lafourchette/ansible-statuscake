#!/usr/bin/python

from ansible.module_utils.basic import *
import requests

class StatusCake:

    def __init__(self, module, username, api_key, name, url, state, test_tags, check_rate, test_type, contact_group, port, user_agent, status_codes, node_locations, follow_redirect, trigger_rate, final_endpoint, find_string, paused, timeout, use_jar, website_host, post_body, post_raw, custom_header, site_ip, dns_ip, dns_server, basic_user, basic_pass, include_header, do_not_find, confirmation, enable_ssl_warning, full_test, custom_message, subject_line, sender_address):
        self.headers = {"Username": username, "API": api_key}
        self.module = module
        self.name = name
        self.url = url
        self.state = state
        self.test_tags = test_tags
        self.status_codes = status_codes
        self.node_locations = node_locations
        self.test_type = test_type
        self.contact_group = contact_group
        self.port = port
        self.user_agent = user_agent
        self.check_rate = check_rate
        self.follow_redirect = follow_redirect
        self.trigger_rate = trigger_rate
        self.final_endpoint = final_endpoint
        self.find_string = find_string
        self.paused = paused
        self.timeout = timeout
        self.use_jar = use_jar
        self.website_host = website_host
        self.post_body = post_body
        self.post_raw = post_raw
        self.custom_header = custom_header
        self.site_ip = site_ip
        self.dns_ip = dns_ip
        self.dns_server = dns_server
        self.basic_user = basic_user
        self.basic_pass = basic_pass
        self.include_header = include_header
        self.do_not_find = do_not_find
        self.confirmation = confirmation
        self.enable_ssl_warning = enable_ssl_warning
        self.full_test = full_test
        self.custom_message = custom_message
        self.subject_line = subject_line
        self.sender_address = sender_address

    def check_response(self,resp):
        if resp['Success'] == False:
            self.module.exit_json(changed=False, meta=resp['Message'])
        else:
            self.module.exit_json(changed=True, meta=resp['Message'])
            
    def check_test(self):
        API_URL = "https://app.statuscake.com/API/Tests"
        response = requests.put(API_URL, headers=self.headers)
        json_object = response.json()

        for item in json_object:
            if item['WebsiteName'] == self.name:
                return item['TestID']
                    
    def manage_test(self):
        data = {
                    "WebsiteName": self.name,
                    "WebsiteURL": self.url,
                    "CheckRate": self.check_rate,
                    "TestType": self.test_type,
                    "TestTags": self.test_tags,
                    "StatusCodes": self.status_codes,
                    "NodeLocations": self.node_locations,
                    "ContactGroup": self.contact_group,
                    "Port": self.port,
                    "UserAgent": self.user_agent,
                    "FollowRedirect": self.follow_redirect,
                    "TriggerRate": self.trigger_rate,
                    "FinalEndpoint": self.final_endpoint,
                    "FindString": self.find_string, 
                    "Paused": self.paused,
                    "Timeout": self.timeout,
                    "UseJar": self.use_jar,
                    "WebsiteHost": self.website_host,
                    # not yet on the api "PostBody": self.post_body, 
                    "PostRaw": self.post_raw,
                    "CustomHeader": self.custom_header,
                    # not yet on the api "SiteIP": self.site_ip,
                    # not yet on the api "DNSIP": self.dns_ip,
                    # not yet on the api "DNSServer": self.dns_server, 
                    "BasicUser": self.basic_user,
                    "BasicPass": self.basic_pass,
                    # not yet on the api "IncludeHeader": self.include_header, 
                    "DoNotFind": self.do_not_find,
                    "Confirmation": self.confirmation, 
                    "EnableSSLWarning": self.enable_ssl_warning, 
                    # not yet on the api "FullTest": self.full_test,
                    # not yet on the api "CustomMessage": self.custom_message,
                    # not yet on the api "SubjectLine": self.subject_line,
                    # not yet on the api "SenderAddress": self.sender_address 
                }

        test_id = self.check_test()

        if self.state == 'present':
            if test_id:
               data['TestID'] = test_id
            API_URL = "https://app.statuscake.com/API/Tests/Update"
            response = requests.put(API_URL, headers=self.headers, data=data)
        elif self.state == 'absent':
             if not test_id:
                 self.module.exit_json(changed=False, meta='No test to delete with the specified name')
             data['TestID'] = test_id
             API_URL = "https://app.statuscake.com/API/Tests/Details"
             response = requests.delete(API_URL, headers=self.headers, data=data)
        self.check_response(response.json())

def main():
    
    fields = {
        "username": {"required": True, "type": "str"},
        "api_key": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "url": {"required": True, "type": "str"},
        "state": {"required": True, "choices": ['present', 'absent'], "type": "str"},
        "test_tags": {"required": False, "type": "str"},
        "status_codes": {"required": False, "type": "str"},
        "node_locations": {"required": False, "type": "str"},
        "follow_redirect": {"required": False, "type": "str"},
        "trigger_rate": {"required": False, "type": "str"},
        "check_rate": {"required": False, "default": 300, "type": "int"},
        "test_type": {"required": False, "choices": ['HTTP', 'HEAD', 'TCP', 'DNS', 'SMTP', 'SSH', 'PING', 'PUSH'],"type": "str"},
        "contact_group": {"required": False, "type": "str"},
        "port": {"required": False, "type": "int"},
        "user_agent": {"required": False, "default":"StatusCake Agent", "type": "str"},
        "final_endpoint": {"required": False, "type": "str"},
        "find_string": {"required": False, "type": "str"},
        "paused": {"required": False, "type": "int"},
        "timeout": {"required": False, "type": "int"},
        "use_jar": {"required": False, "type": "int"},
        "website_host": {"required": False, "type": "str"},
        "post_body": {"required": False, "type": "str"},
        "post_raw": {"required": False, "type": "str"},
        "custom_header": {"required": False, "type": "str"},
        "site_ip": {"required": False, "type": "str"},
        "dns_ip": {"required": False, "type": "str"},
        "dns_server": {"required": False, "type": "str"},
        "basic_user": {"required": False, "type": "str"},
        "basic_pass": {"required": False, "type": "str"},
        "include_header": {"required": False, "type": "int"},
        "do_not_find": {"required": False, "type": "int"},
        "confirmation": {"required": False, "type": "int"},
        "enable_ssl_warning": {"required": False, "type": "int"},
        "full_test": {"required": False, "type": "str"},
        "custom_message": {"required": False, "type": "str"},
        "subject_line": {"required": False, "type": "str"},
        "sender_address": {"required": False, "type": "str"}
    }   

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    
    username = module.params['username']
    api_key = module.params['api_key']
    name = module.params['name']
    url = module.params['url']
    state = module.params['state']
    test_tags = module.params['test_tags']
    status_codes = module.params['status_codes']
    node_locations = module.params['node_locations']
    check_rate = module.params['check_rate']
    test_type = module.params['test_type']
    contact_group = module.params['contact_group']
    port = module.params['port']
    user_agent = module.params['user_agent']
    follow_redirect = module.params['follow_redirect']
    trigger_rate = module.params['trigger_rate']
    final_endpoint = module.params['final_endpoint']
    find_string = module.params['find_string']
    paused = module.params['paused']
    timeout = module.params['timeout']
    use_jar = module.params['use_jar']
    website_host = module.params['website_host']
    post_body = module.params['post_body']
    post_raw = module.params['post_raw']
    custom_header = module.params['custom_header']
    site_ip = module.params['site_ip']
    dns_ip = module.params['dns_ip']
    dns_server = module.params['dns_server']
    basic_user = module.params['basic_user']
    basic_pass = module.params['basic_pass']
    include_header = module.params['include_header']
    do_not_find = module.params['do_not_find']
    confirmation = module.params['confirmation']
    enable_ssl_warning = module.params['enable_ssl_warning']
    full_test = module.params['full_test']
    custom_message = module.params['custom_message']
    subject_line = module.params['subject_line']
    sender_address = module.params['sender_address']

    test_object = StatusCake(module, username, api_key, name, url, state, test_tags, check_rate, test_type, contact_group, port, user_agent, status_codes, node_locations, follow_redirect, trigger_rate, final_endpoint, find_stringi, paused, timeout, use_jar, website_host, post_body, post_raw, custom_header, site_ip, dns_ip, dns_server, basic_user, basic_pass, include_header, do_not_find, confirmation, enable_ssl_warning, full_test, custom_message, subject_line, sender_address)
    test_object.manage_test()

if __name__ == '__main__':  
    main()
