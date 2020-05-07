import requests
import json
# import lidaSheets


##You can choose how to declare you token and your fanpageId. You can use it as environment variable, external file or just hard code it.

class Main:
    def __init__(self):
        accessData = json.loads(open('accessData.json', 'r').read())
        self.token = accessData['token']
        self.fanpageId = accessData['fanpageId']
        self.coreUrl = 'https://graph.facebook.com/v6.0/'
        self.queryListForms = '/leadgen_forms?limit=100'
        self.queryDataForm = 'fields=created_time,id,campaign_name,form_id,field_data'
        self.urlRequestListForms = self.coreUrl + self.fanpageId + self.queryListForms+'&access_token=' + self.token

    def getFormIds(self):
        r = requests.get(self.urlRequestListForms)
        r = r.content.decode('utf-8')
        rJson = json.loads(r)
        for rowFormId in rJson['data']:
            self.formId = rowFormId['id']
            self.getFormData()
    
    def getFormData(self):
        urlRequestDataForm = self.coreUrl + self.formId + '/leads?' + self.queryDataForm + '&access_token=' + self.token
        r = requests.get(urlRequestDataForm)
        r = r.content.decode('utf-8')
        rJson = json.loads(r)
        for row in rJson['data']:
            created_time = row['created_time']
            idLead = row['id']
            campaign_name = row['campaign_name']
            field_data = row['field_data']
            listaSaida = []
            for i in field_data:
                if i['name'] == 'full_name':
                    name = i['values'][0]
                    listaSaida.append(name)
                elif i['name'] == 'email':
                    email = i['values'][0]
                    listaSaida.append(email)
                elif i['name'] == 'phone_number':
                    phone = i['values'][0]
                    listaSaida.append(phone)
                elif i['name'] == 'city':
                    city = i['values'][0]
                    listaSaida.append(city)
            print(name, email, phone, city, self.formId, campaign_name, created_time)

Main().getFormIds()