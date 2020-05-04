import requests
import json
# import lidaSheets


token = 'TOKEN'
idFanpage = 'FANPAGE'
coreUrl = 'https://graph.facebook.com/v6.0/'
queryListForms = '/leadgen_forms?limit=100'
queryDataForm = 'fields=created_time,id,campaign_name,form_id,field_data'
urlRequestListForms = coreUrl+idFanpage+queryListForms+'&access_token='+token


listIdsForms = []
r = requests.get(urlRequestListForms)
r = r.content.decode('utf-8')
rJson = json.loads(r)
for formId in rJson['data']:
    urlRequestDataForm = coreUrl+formId+'/leads?'+queryDataForm+'&access_token='+token
    r = requests.get(urlRequestDataForm)
    r = r.content.decode('utf-8')
    rJson = json.loads(r)
    for linha in rJson['data']:
        created_time = linha['created_time']
        idLead = linha['id']
        campaign_name = linha['campaign_name']
        field_data = linha['field_data']
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
        print(name, email, phone, city, formId, campaign_name, created_time)