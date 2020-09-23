import requests
import json

##Works on 8.0 API version

##Use this tool to check if your token is properly setup https://developers.facebook.com/tools/explorer/

##I used an external json file to host my token and fanpage id, but you can different ways
##You can use it as environment variable, external file or just hard code it.

##Permissions needed from Facebook:
##pages_show_list, leads_retrieval, pages_read_engagement, pages_manage_ads

##Calls must be made using a Page Access Token

##The user must be an administrator, editor, or moderator of the page in order 
##to impersonate it. If the page business requires Two Factor Authentication, 
##the user also needs to enable Two Factor Authentication




class Main:
    def __init__(self):
        access_data = json.loads(open('access_data.json', 'r').read())
        self.token = access_data['token']
        self.fanpage_id = access_data['fanpage_id']
        self.core_url = 'https://graph.facebook.com/v8.0/'
        self.query_list_forms = '/leadgen_forms?limit=100'
        self.query_data_form = 'fields=created_time,id,campaign_name,form_id,field_data'
        self.url_request_list_forms = self.core_url + self.fanpage_id + self.query_list_forms+'&access_token=' + self.token
        print(self.url_request_list_forms)

    def get_data(self):
        r = requests.get(self.url_request_list_forms)
        r = r.content.decode('utf-8')
        r_json = json.loads(r)
        all_forms = []
        for row_form_id in r_json['data']:
            self.form_id = row_form_id['id']
            form_data = self.get_form_data()
            all_forms.append(form_data)
        return all_forms
        
    
    def get_form_data(self):
        url_request_data_form = self.core_url + self.form_id + '/leads?' + self.query_data_form + '&access_token=' + self.token
        r = requests.get(url_request_data_form)
        r = r.content.decode('utf-8')
        r_json = json.loads(r)
        data = []
        for row in r_json['data']:
            created_time = row['created_time']
            id_lead = row['id']
            campaign_name = row['campaign_name']
            field_data = row['field_data']
            for_list = []
            for i in field_data:
                if i['name'] == 'full_name':
                    name = i['values'][0]
                    for_list.append(name)
                elif i['name'] == 'email':
                    email = i['values'][0]
                    for_list.append(email)
                elif i['name'] == 'phone_number':
                    phone = i['values'][0]
                    for_list.append(phone)
                elif i['name'] == 'city':
                    city = i['values'][0]
                    for_list.append(city)
                for_list.append(self.form_id)
                for_list.append(campaign_name)
                for_list.append(created_time)
            data.append(for_list)
        return data

if __name__ == '__main__':
    form_data = Main()
    form_data = form_data.get_data()
    print(form_data)