from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.core import serializers 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import Error
from copy import deepcopy

from .models import Irecord, IrecordUnapproved, IrecordDel


def r_login(request):
    """ REST login api """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                data = {'success': True}
            else:
                data = {'success': False, 
                        'error': 'Wrong username and/or password'}
            return JsonResponse(data, safe=True)    
    return HttpResponseBadRequest()

def manager_grp_check(user):
    """ check whether user is in manager group """
    if user:
        return user.groups.filter(name='Store Manager').count()
    return False

@login_required
def r_enumerate(request): 
    """ Return a Json response with all record details """
    records = Irecord.objects.all() 
    unappr_records = IrecordUnapproved.objects.all()
    json_records = serializers.serialize('json', records)
    return JsonResponse(json_records, safe=False)

@login_required
def add_items(request):
    """ Add records view """
    in_data = request.body
    if manager_grp_check(user):
        new_record = Irecord( pname = in_data['pname'], 
                              vendor= in_data['vendor'], 
                              mrp= in_data['mrp'], 
                              batch_num = in_data['batch_num'], 
                              quantity = in_data['quantity'])  
    else:
        new_record = IrecordUnapproved( pname = in_data['pname'], 
                                        vendor= in_data['vendor'], 
                                        mrp= in_data['mrp'], 
                                        batch_num = in_data['batch_num'], 
                                        quantity = in_data['quantity'])  
    try:
        new_record.save()
        data = {'success': True}
    except Error:
        data = {'success': False, 'error': 'db save error'} 
    return JsonResponse(data, safe=True)    

@login_required
def modify_items(request):
    try:
        disp_record = Irecord.objects.get(pk=request.body['pid'])
        if manager_grp_check(user):
            record = disp_record 
        else: 
            record = IrecordUnapproved.objects.get_or_create(
                                            edit_of=disp_record)
    except DoesNotExist:
        data = {'success': False, 'error': 'product does not exist'}
        return JsonResponse(data, safe=True)
    for key, value in request.body.items():
        record.key = value
    record.save()
    data = {'success': True}
    return JsonResponse(data, safe=True)    
    
@login_required
def delete_items(request):
    try:
        tbdel = Irecord.objects.get(pid = in_data['id']) 
    except DoesNotExist:
        data = {'success': False, 'error': 'record does not exist'}
        return JsonResponse(data, safe=True)    
    except KeyError:
        data = {'success': False, 'error': 'malformed data'}
        return JsonResponse(data, safe=True)    

    if manager_grp_check(user):
        try:
            tbdel.delete()
            data = {'success': True}
        except Error:
            data = {'success': False, 'error': 'db delete error'}
    else:
        ## Create delete queue status obj when record deleted by non-manager
        del_appr = IrecordDel(del_status_of=tbdel)
        del_appr.save()
        data = {'success': True}
    return JsonResponse(data, safe=True)    
        
@login_required
@user_passes_test(manager_grp_check, login_url='/unauthorized/')
def approve_changes(request):
    """ Approval handler view for manager group user """
    action_model = request.body['model'] ## Assuming the first item in json is modelname
    if action_model is 'IrecordUnapproved':
        unappr_record = IrecordUnapproved.objects.get(pk=request.body['pk'])
        parent_record = unappr_record.edit_of
        parent_record = deepcopy(unappr_record) ## Placeholder operation  
        try:
            parent_record.save()
            data = {'success': True}
        except Error:
            data = {'success': False, 'error': 'db delete error'}

    elif action_model is 'IrecordDelete':
        try:
            del_inst = IrecordDelete.objects.get(pk=request.body['pk'])
            del_record = del_inst.del_status_of
            del_record.delete()
            data = {'success': True}
        except KeyError:
            data = {'success': False, 'error': 'malformed data'}
        except Error:
            data = {'success': False, 'error': 'db delete error'}
    return JsonResponse(data, safe=True)    

def r_unauthorized(request):
    data = {'success': False, 'error': 'unauthorized'}
    return JsonResponse(data, safe=True)    
