
from django.shortcuts import redirect, render
import requests
from django.contrib import messages

from .config import domain_name

def hospital(request):
    data = requests.get(f'{domain_name.url}GetHospitalList').json()
    # print(data)
    return data

def add_hospital_form(request):
    url = f'{domain_name.url}CreateHospitalProfile'
    if request.method == 'POST':
        hospitalname = request.POST.get('hospitalname')
        name = request.POST.get('username')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        tier = request.POST.get('tier')
        tier= int(tier)
        if password == confirmpassword:
            data = {"inputdata": {"hospitalname" : hospitalname,"mobile" : mobile,"email" : email,"username" : name,"psw" : password,"tier":tier}}
            a = requests.post(url, json = data).json()
            print(a)
            messages.success(request, 'Hospital added successfully..')

            result_data = a['ResultData']
            print(result_data,'id')
            return redirect('hospital_profile_edit', result_data)
        else:
            messages.warning(request, "Password did not match")
            return redirect('add_hospital')

def delete_hospital(request, id):
    data = {"ResultData": {"hospitalid":id}}
    url = f'{domain_name.url}deleteHospitalOtEquipments'
    requests.post(url, json=data)
    messages.info(request, 'Hospital deleted successfully...!')
    return data

def hospital_edit_profile(request,id):
    print('edit start', id)
    result = None
    Api = f'{domain_name.url}getHospitalProfile?hosid={id}'
    ApiData = requests.get(Api).json()

    imgapi = f'{domain_name.url}GetHospitalimgByid?hosid={id}'
    imgData = requests.get(imgapi).json()
    if ApiData['Status'] == False:
        pass
    else:
        result = ApiData['ResultData']
        result['hosid'] = id
        result['img'] = imgData['ResultData']
        if request.method == 'POST' :
            # hid = request.POST.get('hid')
            hname = request.POST.get('txtHospitalName')
            uname = request.POST.get('txtUsername')
            mobile = request.POST.get('txtMobile')
            email = request.POST.get('txtEmail')
            # image = request.FILES['file']
            
            api = f'{domain_name.url}updateHospitalProfile'
            out = {"inputdata": {"hosid":id,"email":email,"hospitalname":hname,"mobile":mobile,"username":uname}}
            a = requests.post(api, json = out)
            messages.success(request, 'Updated successfully...!')

            Api = f'{domain_name.url}getHospitalProfile?hosid={id}'
            ApiData = requests.get(Api).json()
            imgapi = f'{domain_name.url}GetHospitalimgByid?hosid={id}'
            imgData = requests.get(imgapi).json()
            result = ApiData['ResultData']
            result['hosid'] = id
            result['img'] = imgData['ResultData']
            return result
    return result

def hospital_edit_details(request, id):
    print('edit start', id)
    result = None
    Api = f'{domain_name.url}GetHospitalsDetails?hosid={id}'
    ApiData = requests.get(Api).json()
    if ApiData['Status'] == False:
        a = 'not data'
    else:
        result = ApiData['ResultData']
        result['hosid'] = id
        if request.method == 'POST':
            txtRegNumber = request.POST.get('txtRegNumber')
            txtESTDYear = request.POST.get('txtESTDYear')
            txtContactNumber = request.POST.get('txtContactNumber')
            txtContactPerson = request.POST.get('txtContactPerson')
            txtQualityaccreditations = request.POST.get('txtQualityaccreditations')
            txtNameofdirector = request.POST.get('txtNameofdirector')
            Specialities = request.POST.get('Specialities')
            txtOTCount = request.POST.get('txtOTCount')

            print(Specialities)
            api1 = f'{domain_name.url}updateHospitalDetails'
            out1 = {"inputdata":{"hospitalid": id, "hosid": id, "certificatefilename": None, "contactno": txtContactNumber, "contactperson": txtContactPerson, "estdyear": txtESTDYear, "hosnumber": None, "hospitalimage": None, "hospitallogo": None, "nameofdirector": txtNameofdirector, "otcount": txtOTCount, "proprietor": None, "qualityaccreditations": txtQualityaccreditations, "regnum": txtRegNumber, "specialityids": None, "specialityid": None, "specialities": Specialities,"specialityfield":Specialities}}
            a=requests.post(api1, json = out1)
            print(a.json())
            messages.success(request, 'updated successfully...!')
            Api = f'{domain_name.url}GetHospitalsDetails?hosid={id}'
            ApiData = requests.get(Api).json()
            result = ApiData['ResultData']
            result['hosid'] = id
            print(result)
            return result
            
    return result

def hospital_edit_address(request, id):
    print('edit start', id)
    result = None
    Api = f'{domain_name.url}GetHospitalsAddress?hosid={id}'
    ApiData = requests.get(Api).json()
    if ApiData['Status'] == False:
        a = 'not data'
    else:
        result = ApiData['ResultData']
        result['hosid'] = id
        print(result)
        if request.method == 'POST':
            txtAddress = request.POST.get('txtAddress')
            txtCity = request.POST.get('txtCity')
            txtLandmark = request.POST.get('txtLandmark')
            txtPincode = request.POST.get('txtPincode')
            txtLatitude = request.POST.get('txtLatitude')
            txtLongitude = request.POST.get('txtLongitude')
            
            api1 = f'{domain_name.url}updateHospitalsAddress'
            out1 = {"inputdata":{"address":txtAddress,"city":txtCity,"landmark":txtLandmark,"pincode":txtPincode ,"latitude":txtLatitude,"longitude":txtLongitude,"hosid":id}}
            requests.post(api1, json = out1)
            
            messages.success(request, 'updated successfully...!')
            Api = f'{domain_name.url}GetHospitalsAddress?hosid={id}'
            ApiData = requests.get(Api).json()
            result = ApiData['ResultData']
            result['hosid'] = id
            return result
    return result

def hospital_edit_status(request,id):
    result = None
    Api = f'{domain_name.url}GetHospitalsStatus?hosid={id}'
    ApiData = requests.get(Api).json()
    if ApiData['Status'] == False:
        a = 'not data'
    else:
        result = ApiData['ResultData']
        if request.method == 'POST':
            verifiedhospdetails = request.POST.get('verifiedhospdetails')
            verifiedhospaddress = request.POST.get('verifiedhospaddress')
            verifiedhospots = request.POST.get('verifiedhospots')
            comment = request.POST.get('comment')
            status = request.POST.get('status')
            print(status,comment,verifiedhospots,verifiedhospaddress,verifiedhospdetails)
            if verifiedhospdetails == 'on':
                verifiedhospdetails = 1
            else:
                verifiedhospdetails = 0

            if verifiedhospaddress == 'on':
                verifiedhospaddress = 1
            else:
                verifiedhospaddress = 0

            if verifiedhospots == 'on':
                verifiedhospots = 1
            else:
                verifiedhospots = 0
            url = f'{domain_name.url}updateHospitalsStatus'
            data = {"inputdata":{"verifiedhospdetails":verifiedhospdetails,"verifiedhospaddress":verifiedhospaddress,"verifiedhospots":verifiedhospots,"status":int(status),"comment":comment,"hosid":id}}
            a = requests.post(url, json = data)
            print('successsss', data, a.json())
            messages.success(request, 'Status edited successfully..')
            Api = f'{domain_name.url}GetHospitalsStatus?hosid={id}'
            ApiData = requests.get(Api).json()
            result = ApiData['ResultData']
            return result
    return result

def hospital_edit_surgeons(request,id):
    data = requests.get(f'{domain_name.url}getSurgonslist?hosid={id}').json()
    result = {'surgons':data['ResultData'],'hosid':id}
    return  result 

def hospital_add_surgeon(request,id):
    url = f'{domain_name.url}Createsurgen'
    print(id)
    if request.method == 'POST':
        name = request.POST.get('name')
        specialist = request.POST.get('specialist')
        year = request.POST.get('year')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        print(name,email,phone,year,specialist)
        data = {"inputdata":{"name":name,"specialist":specialist,"hosid":id,"year":year,"phone":phone,"email":email}}
        a = requests.post(url, json = data)
        print('successsss', data, a.json())
        messages.success(request, 'Surgeon added successfully..')
        return data

def surgeonedit(request, id):
    result = None
    Api = f'{domain_name.url}getSurgonsById?surgonid={id}'
    ApiData = requests.get(Api).json()
    if ApiData['Status'] == False:
        a = 'not data'
    else:
        result = ApiData['ResultData'][0]
        # result['surgonid'] = id
        if request.method == 'POST':
            surgonsname = request.POST.get('surgeonName')
            year = request.POST.get('surgeonYear')
            phone = request.POST.get('surgeonPhone')
            specialist = request.POST.get('surgeonSpecialist')
            emailid = request.POST.get('surgeonEmail')
            api1 = f'{domain_name.url}modifysurgen'
            out1 = {"inputdata":{"surgonid":id,"name":surgonsname,"specialist":specialist,"year":year,"phone":phone,"email":emailid}}
            a =requests.post(api1, json = out1)
            messages.success(request, 'updated successfully...!')
            Api = f'{domain_name.url}getSurgonsById?surgonid={id}'
            ApiData = requests.get(Api).json()
            result = ApiData['ResultData'][0]
            # result['hosid'] = id
            return result
    return result

def surgeon_delete(request, id):
    print(id, 'surgeon id')
    url = f'{domain_name.url}deletesurgen'
    data = {"ResultData": {"surgonid":id}}
    requests.post(url, json=data)
    messages.info(request, 'Surgeon deleted successfully...!')
    return ('hospital_surgeons_edit')

def hospital_edit_equipment(request,id):
    data = requests.get(f'{domain_name.url}GetHospitalOtEquipment?hosid={id}').json()
    names = f'{domain_name.url}GetOTEquipment'
    Dropdown_data = requests.get(names).json()
    # print(Dropdown_data)
    result = {'equipments':data['ResultData'],'hosid':id, 'dropdown_data':Dropdown_data['ResultData']}
    print(result)
    return  result 
 
def hospital_equipment_add(request,id):
    url = f'{domain_name.url}insertHospitalOtEquipments'
    print(id)

    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        print(name,desc)
        data = {"inputdata": {"hosid": id, "equid": name, "description": desc}}
        a = requests.post(url, json = data)
        print('successsss', data, a.json())
        messages.success(request, 'Equipment added successfully..')
        return data

def equipment_delete(request, id):
    data = {"ResultData": {"equid":id}}
    url = f'{domain_name.url}deleteHospitalOtEquipments'
    requests.post(url, json=data)
    messages.info(request, 'Equipment deleted successfully...!')
    return data



 # Hospital View

def hospital_profile_view_get(request, id):
    Api_Profile = requests.get(f'{domain_name.url}getHospitalProfile?hosid={id}').json()
    if Api_Profile['Status'] == False:
        a = 'no data'
    else:
        profile_result = Api_Profile['ResultData']
        return profile_result
    
def hospital_details_view_get(request, id):
    Api_Details = requests.get(f'{domain_name.url}GetHospitalsDetails?hosid={id}').json()
    if Api_Details['Status'] == False:
        a = 'no data'
    else:
        details_result = Api_Details['ResultData']
        return details_result
    
def hospital_address_view_get(request, id):
    Api_Address = requests.get(f'{domain_name.url}GetHospitalsAddress?hosid={id}').json()
    if Api_Address['Status'] == False:
        a = 'no data'
    else:
        address_result = Api_Address['ResultData']
        return address_result
    
def hospital_status_view_get(request, id):
    Api_Status = requests.get(f'{domain_name.url}GetHospitalsStatus?hosid={id}').json()
    if Api_Status['Status'] == False:
        a = 'no data'
    else:
        status_result = Api_Status['ResultData']
        return status_result
    
def hospital_surgeon_view_get(request, id):
    Api_Surgeon = requests.get(f'{domain_name.url}getSurgonslist?hosid={id}').json()
    if Api_Surgeon['Status'] == False:
        a = 'no data'
    else:
        surgeon_result = Api_Surgeon['ResultData']
        return surgeon_result
    
def hospital_equipment_view_get(request, id):
    Api_Equipment= requests.get(f'{domain_name.url}GetHospitalOtEquipment?hosid={id}').json()
    if Api_Equipment['Status'] == False:
        a = 'no data'
    else:
        equipment_result = Api_Equipment['ResultData']
        return equipment_result
    
def hospital_transaction_view_get(request, id):
    Trasanction_URL = requests.get(f'{domain_name.url}GetAllHospitalTransaction?hosid={id}&startdate=&enddate=').json()
    if Trasanction_URL['Status'] == False:
        messages.info(request, 'Something went wrong, try after sometime..!')
    else:
        transaction_result = Trasanction_URL['ResultData']
        print(transaction_result)
        return transaction_result
