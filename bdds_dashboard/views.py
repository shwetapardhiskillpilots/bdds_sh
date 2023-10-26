from django.shortcuts import render ,get_object_or_404
from .models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import datetime
from datetime import datetime
from bdds_dashboard.image_store import *
import os
import time
import re
from django.db import connection
from bdds_dashboard.serilizers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth.models import User
import base64
from .models import *
import json
#from .serilizers import FileSerializer
from .serilizers import images_serilizer
from rest_framework.parsers import MultiPartParser, FormParser
import logging
# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s %(funcName)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def logine_page(request):
       return render(request,"login.html")

def index_page(request):
    if request.method=="POST":
        user_name=request.POST["u_name"]
        user_pwd=request.POST["u_pwd"]
        user=authenticate(request,username=user_name,password=user_pwd)
        if user is not None:
            login(request, user)
            return HttpResponse("success")
        else:
            return HttpResponse("error")
@login_required(login_url='/error')
def index_page2(request):
    print(request.user.id)
    try:
            if request.user.is_superuser:
               Total_Case=Form_data.objects.count()
               Total_Dalam=N_dalam.objects.count()
               Total_Exposed=Form_data.objects.filter(radio_data='Exploded').count()
               Total_Detected=Form_data.objects.filter(radio_data='Detected').count()
               Total_Death=death_person.objects.count()
               Total_Injured=injured_person.objects.count()
               Total_Incident= N_incident.objects.count()
               Total_Location=N_location.objects.count()
            else:

                Total_Case=Form_data.objects.filter(user_id=request.user.id).count()
                Total_Dalam=N_dalam.objects.count()
                Total_Exposed=Form_data.objects.filter(user_id=request.user.id).filter(radio_data='Exploded').count()
                #Total_Detected=Form_data.objects.filter(usr_id=request.user.id).filter(radio_data='Detected').count()
                Total_Detected=Form_data.objects.filter(user_id=request.user.id).filter(radio_data='Detected').count()
                #Total_Death=death_person.objects.count()
                #Total_Injured=injured_person.objects.count()
                Total_Incident= N_incident.objects.count()
                Total_Location=N_location.objects.count()
                form_id=Form_data.objects.filter(user_id=request.user.id).values('id')
                death = [(death_person.objects.filter(form_id=i["id"]).count()) for i in form_id]
                Total_Death=sum(death)
                injured = [(injured_person.objects.filter(form_id=i["id"]).count()) for i in form_id]
                Total_Injured=sum(injured)



    except Exception as e:
          pass


    finally:
           context={'total_case':Total_Case,'total_dalam':Total_Dalam,
              'total_exposed':Total_Exposed,'total_detected':Total_Detected,
              'total_death':Total_Death,'total_injured':Total_Injured,'total_incident':Total_Incident,
              'total_location':Total_Location}
           return render(request,"index.html", context)

def logout_page(request):
    logout(request)
    return render(request,"login.html")

def error_page(request):
    return render(request,"error/page_404.html")

@login_required(login_url='/error')
def logine_creation(request):
    user_name=request.POST.get("lname")
    user_number=request.POST.get("lnumber")
    user_email=request.POST.get('lemail')
    user_password=request.POST.get("lpassword")
    user_designation=request.POST.get("ldesignation")
    user_edit_permission=request.POST.get('permission1')
    user_dlt_permission=request.POST.get("permission2")
    station_id=request.POST.get('post_value')
    try:
        if request.method=='POST' :

            my_user=User.objects.create_user(password=user_password,username=user_number,email=user_email,
                                             first_name=user_name,last_name=user_designation)
            my_user.save()
            user_data=Nlogines_creations(user=my_user,l_numbers=user_number,join_designation_id=user_designation,permission_edit=user_edit_permission,
                                         permission_delete=user_dlt_permission,post_id=station_id)
            user_data.save()
            messages.success(request, 'User created Successfully')

    except Exception as e:
        messages.info(request, 'Mobile Number Already Present ')

    finally:
        t_designation=N_degignation.objects.all()
        t_post=N_post.objects.all()
        context={"data":t_designation,"data1":t_post}
        return render(request,"logine_creation.html",context)

@login_required(login_url='/error')
def sp_authority(request):


        sname_value=request.POST.get("sname_value")

        snumber_value=request.POST.get("snumber_value")

        sdesignation_value=request.POST.get("sdesignation_value")
        semail_value=request.POST.get("semail_value")
        spassword_value=request.POST.get("spassword_value")
        spassword2_value=request.POST.get("spassword2_value")
        try:
             if request.method=="POST":
                my_user=User.objects.create_user(password=spassword_value,username=snumber_value,email=semail_value,is_superuser=1,
                                first_name=sname_value,last_name=sdesignation_value)
                my_user.save()
                user_data=Nlogines_creations(user=my_user,l_numbers=snumber_value,join_designation_id=sdesignation_value,permission_edit=1,permission_delete=1)
                user_data.save()
                messages.success(request,'Super User Created Succesfully')

        except Exception as e:
            messages.info(request, 'Mobile Number Already Present ')
        finally:
            t_designation=N_degignation.objects.all()
            t_spauthurity=Nsp_authourity.objects.all()
            return render(request,"spauthority.html",{"data":t_designation})

#---------all user data_----------
@login_required(login_url='/error')
def all_user(request):
    #user_join()
    user_data = Nlogines_creations.objects.all().select_related('user').select_related('join_designation').select_related('post')
    x,y= permission(request)
    t_designation=N_degignation.objects.all()
    context={"x":x,"y":y,"data":user_data}
    return render(request,"user/all_user.html",context)
@login_required(login_url='/error')
def dlt_user(request):
    try:
         user_id=request.POST['user_id']

         #Nlogines_creations.objects.get(user=user_id).delete()
         User.objects.get(id=user_id).delete()
         messages.success(request,'successfully user deleted')
         return HttpResponse("success")
     #authtoken_token.objects.get(user_id=user_id).delete()
    except Exception as e:
        messages.error(request,e)
        return HttpResponse("success")


     # user_data = Nlogines_creations.objects.all().select_related('user')
     # return render(request,"user/all_user.html",{"data":user_data})
@login_required(login_url='/error')
def user_profile(request):

    if request.method=='GET':
        user_data = Nlogines_creations.objects.filter(user_id=request.user.id).select_related('user').select_related('join_designation').select_related('post')
        user_post=N_post.objects.all()
        user_designation= N_degignation.objects.all()
        context={'user_data':user_data,
                 'user_post':user_post,
                 'user_designation':user_designation
                 }
        return render(request,'user/profile.html',context)
    if request.method=="POST":
        try:
            user_name=request.POST.get('user_name')
            user_number=request.POST.get('user_number')
            user_email=request.POST.get('user_mail')
            user_post=request.POST.get('user_post')
            user_designation=request.POST.get('user_designation')
            User.objects.filter(id=request.user.id).update(username=user_number,first_name=user_name,email=user_email)
            Nlogines_creations.objects.filter(user_id=request.user.id).update(post=user_post)
            messages.success(request,'Profile update successfully')


        except Exception as e:
            messages.error(request,'Something Wrong Please Try Again')
        finally:
               user_post=N_post.objects.all()
               user_designation= N_degignation.objects.all()
               user_data = Nlogines_creations.objects.filter(user_id=request.user.id).select_related('user').select_related('join_designation').select_related('post')
               context={'user_data':user_data,
                        'user_post':user_post,
                        'user_designation':user_designation
                        }
               return render(request,'user/profile.html',context)
def forget_passwd(request):



     if request.method=='POST':
        try:
                if request.POST.get("user_password1")==request.POST.get('user_password2'):
                        user_number=request.POST.get('user_number')
                        user_email=request.POST.get('user_email')
                        user=User.objects.filter(username=user_number,email=user_email).exists()
                        if User.objects.filter(username=user_number,email=user_email).exists():
                            u = User.objects.get(username=request.POST.get("user_number"))
                            u.set_password(request.POST.get('user_password1'))
                            u.save()
                            messages.success(request,'Password Update successfully')

                        else:
                            messages.error(request,'Please Insert Correct Mobile Number and Email Id')
                else:
                   messages.error(request,"Passwords do NOT match")
        except Exception as e:
            messages.error(request,'Something  Wrong Please Try Again')
        finally:
                 return render(request,'pwd_update.html')
     return render(request,'pwd_update.html')

@login_required(login_url='/error')
def user_activate(request):
    user_id=request.POST['id']
    try:
            user_value=User.objects.filter(id=user_id).values('is_active')[0]
            user_value=(user_value['is_active'])

            if user_value == True:
                User.objects.filter(id=user_id).update(is_active=0)
                messages.success(request,'User Deactivate Successfully')
            else:
                User.objects.filter(id=user_id).update(is_active=1)
                messages.success(request,'User Activate Successfully')
    except Exception as e:
           messages.info(request,'User Not Present')
    finally:
            return HttpResponse('success')
    #return render(request,"user/all_user.html")
#-----------start location--------------------
@login_required(login_url='/error')
@csrf_exempt
def t_location(request):
    try:
        locations = request.POST.get('locations_value')
        x,y= permission(request)
        if locations is None:
            ty_location= N_location.objects.all()
            context={"x":x,"y":y,"data":ty_location}
            return render(request,"location/tlocation.html",context)

        else:
            p_location=request.POST["locations_value"]
            m_location=N_location(l_location=p_location)
            m_location.save()
            messages.success(request,"successfully location created")
            ty_location= N_location.objects.all()
            context={"x":x,"y":y,"data":ty_location}
            return render(request,"location/tlocation.html",context)
    except Exception as e:
         messages.error(request,e)
         ty_location= N_location.objects.all()
         context={"x":x,"y":y,"data":ty_location}
         return render(request,"location/tlocation.html",context)


@login_required(login_url='/error')
@csrf_exempt
def dlt_location(request):
    try:
      l=request.POST.get('l_cation')
      N_location.objects.get(id=l).delete()
      messages.success(request,"successfully location deleted ")
      return HttpResponse("Success!")
    except Exception as e:
      messages.success(request,e)
      return HttpResponse("Success!")

@login_required(login_url='/error')
def upd_location(request):
    try:
        upd_value=request.POST.get("locations_value")
        location_id=request.POST.get("location_id")
        x,y= permission(request)

        if upd_value is None:
           ty_location= N_location.objects.all()
           context={"x":x,"y":y,"data":ty_location}
           return render(request,"location/tlocation.html",context)
        else:
            N_location.objects.filter(id=location_id).update(l_location=upd_value)
            messages.success(request,'successfully location updated')
            ty_location= N_location.objects.all()
            context={"x":x,"y":y,"data":ty_location}
            return render(request,"location/tlocation.html",context)
    except Exception as e:
        messages.error(request,e)
        ty_location= N_location.objects.all()
        context={"x":x,"y":y,"data":ty_location}
        return render(request,"location/tlocation.html",context)



#---------------end location-----------------------------------
#-------------------start jurisdiction--------------
@login_required(login_url='/error')
def jurisdiction(request):
   try:
        jurisdiction=request.POST.get("jurisdiction_value")
        x,y= permission(request)
        if jurisdiction is None:
            t_jurisdiction=N_juridiction.objects.all()
            context={"x":x,"y":y,"data":t_jurisdiction}
            return render(request,"jurisdiction/jurisdiction.html",context)

        else:
            p_jurisdiction=request.POST["jurisdiction_value"]
            m_jurisdiction=N_juridiction(l_juridiction=p_jurisdiction)
            m_jurisdiction.save()
            t_jurisdiction=N_juridiction.objects.all()
            messages.success(request,'successfully juridiction created')
            context={"x":x,"y":y,"data":t_jurisdiction}
            return render(request,"jurisdiction/jurisdiction.html",context)
   except Exception as e:
       messages.error(request,e)
       context={"x":x,"y":y,"data":t_jurisdiction}
       return render(request,"jurisdiction/jurisdiction.html",context)

@login_required(login_url='/error')
@csrf_exempt
def dlt_jurisdiction(request):
    try:
        j=request.POST["j_id"];
        N_juridiction.objects.get(id=j).delete()
        messages.success(request,'successfully juridiction deleted')
        return HttpResponse("success")
    except Exception as e:
        messages.error(request,e)
        return HttpResponse("success")
def upd_juridiction(request):
    try:

        juridiction_value=request.POST.get("jurisdiction_value")
        juridiction_id=request.POST.get("juridiction_id")
        x,y= permission(request)
        if juridiction_value is None:
            t_jurisdiction=N_juridiction.objects.all()
            context={"x":x,"y":y,"data":t_jurisdiction}
            return render(request,"jurisdiction/jurisdiction.html",context)

        else:
            N_juridiction.objects.filter(id=juridiction_id).update(l_juridiction=juridiction_value)
            messages.success(request,'successfully juridiction updated')
            t_jurisdiction=N_juridiction.objects.all()
            context={"x":x,"y":y,"data":t_jurisdiction}
            return render(request,"jurisdiction/jurisdiction.html",context)
    except Exception as e:
        messages.error(request,e)
        t_jurisdiction=N_juridiction.objects.all()
        context={"x":x,"y":y,"data":t_jurisdiction}
        return render(request,"jurisdiction/jurisdiction.html",context)





#----------end jurisdiction--------------------------
#---------------start type of incident---------------
@login_required(login_url='/error')
def t_incident(request):
    try:
        incident=request.POST.get("incident_value")
        x,y= permission(request)
        if incident is None:
            t_incident=N_incident.objects.all()
            context={"x":x,"y":y,"data":t_incident}
            return render(request,"incident/incident.html",context)

        else:
            p_incident=request.POST["incident_value"]
            m_incident=N_incident(i_incident=p_incident)
            m_incident.save()
            messages.success(request,'successfully type of incident created')
            t_incident=N_incident.objects.all()
            context={"x":x,"y":y,"data":t_incident}
            return render(request,"incident/incident.html",context)
    except Exception as e:
        messages.error(request,e)
        t_incident=N_incident.objects.all()
        context={"x":x,"y":y,"data":t_incident}
        return render(request,"incident/incident.html",context)

@login_required(login_url='/error')
@csrf_exempt
def dlt_incident(request):
    try:
         i_id=request.POST["i_id"]
         N_incident.objects.get(id=i_id).delete()
         messages.success(request,'successfully type of incident deleted')
         return HttpResponse("success")
    except Exception as e:
        messages.error(request,e)
        return HttpResponse("success")

@login_required(login_url='/error')
def upd_incident(request):
    try:
         x,y= permission(request)
         incident_value=request.POST.get('incident_value')
         incident_id=request.POST.get("incident_id")

         if incident_value is None:
            t_incident=N_incident.objects.all()
            context={"x":x,"y":y,"data":t_incident}
            return render(request,"incident/incident.html",context)

         else:
             N_incident.objects.filter(id=incident_id).update(i_incident=incident_value)
             messages.success(request,'successfully type of incident updated')
             t_incident=N_incident.objects.all()
             context={"x":x,"y":y,"data":t_incident}
             return render(request,"incident/incident.html",context)
    except Exception as e:
         messages.error(request,'successfully type of incident updated')
         t_incident=N_incident.objects.all()
         context={"x":x,"y":y,"data":t_incident}
         return render(request,"incident/incident.html",context)


#---------------end incident-----------------
#-----------start weight--------------
@login_required(login_url='/error')
def weight(request):
    try:
        weight=request.POST.get("weight_value")
        x,y= permission(request)
        if weight is None:
            t_weight=N_weight.objects.all()
            context={"x":x,"y":y,"data":t_weight}
            return render(request,"weight/weight.html",context)
        else:
            p_weight=request.POST["weight_value"]
            m_weight=N_weight(w_weight=p_weight)
            m_weight.save()
            messages.success(request,"successfully explosive weight created")
            t_weight=N_weight.objects.all()
            context={"x":x,"y":y,"data":t_weight}
            return render(request,"weight/weight.html",context)
    except Exception as e:
        messages.error(request,e)
        t_weight=N_weight.objects.all()
        context={"x":x,"y":y,"data":t_weight}
        return render(request,"weight/weight.html",context)

@login_required(login_url='/error')
@csrf_exempt
def dlt_weight(request):
    try:
        w_id=request.POST["w_id"]

        N_weight.objects.get(id=w_id).delete()
        messages.success(request,'successfully explosive weight deleted')
        return HttpResponse("success")
    except Exception as e:
        messages.error(request,e)
        return HttpResponse("success")


@login_required(login_url='/error')
def upd_weight(request):
    x,y= permission(request)
    try:
        w_id=request.POST.get("weight_id")
        weight_value=request.POST.get("weight_value")
        if weight_value is None:
           t_weight=N_weight.objects.all()
           context={"x":x,"y":y,"data":t_weight}
           return render(request,"weight/weight.html",context)
        else:
            N_weight.objects.filter(id=w_id).update(w_weight=weight_value)
            messages.success(request,'successfully explosive weight updated')
            t_weight=N_weight.objects.all()
            context={"x":x,"y":y,"data":t_weight}
            return render(request,"weight/weight.html",context)
    except Exception as e:
        messages.error(request,e)
        t_weight=N_weight.objects.all()
        context={"x":x,"y":y,"data":t_weight}
        return render(request,"weight/weight.html",context)


#------------end weight------------------------
#---------------start explosive----------
@login_required(login_url='/error')
def t_explosive(request):
    try:
        explosive=request.POST.get("explosive_value")
        x,y= permission(request)
        if explosive is None:
            t_explosive=N_explosive.objects.all()
            context={"x":x,"y":y,"data":t_explosive}
            return render(request,"explosive/explosive.html",context)
        else:
            p_explosive=request.POST["explosive_value"]
            m_explosive=N_explosive(e_explosive=p_explosive)
            m_explosive.save()
            messages.success(request,"successfully explosive type created")
            t_explosive=N_explosive.objects.all()
            context={"x":x,"y":y,"data":t_explosive}
            return render(request,"explosive/explosive.html",context)
    except Exception as e:
        messages.error(request,e)
        t_explosive=N_explosive.objects.all()
        context={"x":x,"y":y,"data":t_explosive}
        return render(request,"explosive/explosive.html",context)


@login_required(login_url='/error')
@csrf_exempt
def dlt_explosive(request):
    try:
        e_id=request.POST["e_id"]
        N_explosive.objects.get(id=e_id).delete()
        messages.success(request,"successfully explosive type deleted")
        return HttpResponse("success")
    except Exception as e:
        messages.error(request,"successfully explosive type deleted")
        return HttpResponse("success")


@login_required(login_url='/error')
def upd_explosive(request):
    try:
        explosive_value=request.POST.get("explosive_value")
        explosive_id=request.POST.get("explosive_id")
        x,y= permission(request)
        if explosive_value is None:
            t_explosive=N_explosive.objects.all()
            context={"x":x,"y":y,"data":t_explosive}
            return render(request,"explosive/explosive.html",context)
        else:
            N_explosive.objects.filter(id=explosive_id).update(e_explosive=explosive_value)
            messages.success(request,"successfully explosive value updated")
            t_explosive=N_explosive.objects.all()
            context={"x":x,"y":y,"data":t_explosive}
            return render(request,"explosive/explosive.html",context)
    except Exception as e:
        messages.error(request,e)
        t_explosive=N_explosive.objects.all()
        context={"x":x,"y":y,"data":t_explosive}
        return render(request,"explosive/explosive.html",context)
#--------end explosive-------------------
#--------------start current status-----------
@login_required(login_url='/error')
def a_current_status(request):
    try:
        c_status=request.POST.get("c_status_value")
        x,y= permission(request)

        if c_status is None:
            t_c_status= N_assused.objects.all()
            context={"x":x,"y":y,"data":t_c_status}
            return render(request,"currentstatus/current_status.html",context)
        else:
            p_c_status=request.POST["c_status_value"]
            m_c_status= N_assused(a_assused=p_c_status)
            m_c_status.save()
            messages.success(request, "successfully assused status created")
            t_c_status= N_assused.objects.all()
            context={"x":x,"y":y,"data":t_c_status}
            return render(request,"currentstatus/current_status.html",context)
    except Exception as e:
        messages.error(request, e)
        t_c_status= N_assused.objects.all()
        context={"x":x,"y":y,"data":t_c_status}
        return render(request,"currentstatus/current_status.html",context)


@login_required(login_url='/error')
@csrf_exempt
def dlt_c_status(request):
    try:
        s_id=request.POST.get("s_id")
        N_assused.objects.get(id=s_id).delete()
        messages.success(request, "successfully assused status deleted")
        return HttpResponse("success")
    except Exception as e:
        messages.success(request, e)
        return HttpResponse("success")
def upd_status(request):
    status_id=request.POST.get("status_id")
    x,y= permission(request)
    status_value=request.POST.get("status_value")
    if status_value is None:
        t_c_status= N_assused.objects.all()
        context={"x":x,"y":y,"data":t_c_status}
        return render(request,"currentstatus/current_status.html",context)

    else:
        N_assused.objects.filter(id=status_id).update(a_assused=status_value)
        messages.success(request,'successfully assused status update')
        t_c_status= N_assused.objects.all()
        context={"x":x,"y":y,"data":t_c_status}
        return render(request,"currentstatus/current_status.html",context)


#----------end current status------------------
#------------start post---------------------
@login_required(login_url='/error')
def post(request):
    post=request.POST.get("post_value")
    try:
        if post is None:
            t_post=N_post.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_post}
            return render(request,"post/post.html",context)
        else:
            p_post=request.POST["post_value"]
            m_post=N_post(p_post=p_post)
            m_post.save()
            messages.success(request, 'successfully created post')

            t_post=N_post.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_post}
            return render(request,"post/post.html",context)
    except Exception as e:
            messages.error(request,e)

            t_post=N_post.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_post}
            return render(request,"post/post.html",context)

@login_required(login_url='/error')
@csrf_exempt
def dlt_post(request):
    try:
        p_id=request.POST["p_id"]
        N_post.objects.get(id=p_id).delete()
        messages.success(request, "successfully deleted post")
        return HttpResponse("success")
    except Exception as e:
        messages.error(request, e)
        return HttpResponse("success")
@login_required(login_url='/error')
def upd_post(request):
    try:
        p_id=request.POST.get("post_id")
        post_value=request.POST.get("post_value")
        if post_value is None:
            t_post=N_post.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_post}
            return render(request,"post/post.html",context)
        else:
            N_post.objects.filter(id=p_id).update(p_post=post_value)
            messages.success(request, "successfully post updated")
            t_post=N_post.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_post}
            return render(request,"post/post.html",context)
    except Exception as e:
        messages.error(request,e)
        t_post=N_post.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_post}
        return render(request,"post/post.html",context)



#-----------------end post-------------------
#----------start designation-------------------
@login_required(login_url='/error')
def designation(request):
    designation=request.POST.get("designation_value")

    if designation is None:
        t_designation=N_degignation.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_designation}
        return render(request,"designation/designation.html",context)
    else:
        p_designation=request.POST["designation_value"]
        m_designation=N_degignation(d_designation=p_designation)
        m_designation.save()
        messages.success(request, 'desigation create successfully')
        x,y= permission(request)
        t_designation=N_degignation.objects.all()
        context={"x":x,"y":y,"data":t_designation}
        return render(request,"designation/designation.html",context)

@login_required(login_url='/error')
@csrf_exempt
def dlt_designation(request):
    d_id=request.POST["d_id"]
    N_degignation.objects.get(id=d_id).delete()
    messages.success(request, 'designation delete successfully')
    return HttpResponse("success")

@login_required(login_url='/error')
def upd_designation(request):
    d_id=request.POST.get('designation_id')
    designation_value=request.POST.get("designation_value")

    if designation_value is None:

        t_designation=N_degignation.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_designation}
        return render(request,"designation/designation.html",context)
    else:
        N_degignation.objects.filter(id=d_id).update(d_designation=designation_value)
        messages.success(request, 'designation update successfully')

        t_designation=N_degignation.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_designation}
        return render(request,"designation/designation.html",context)

#--------end designation-----------------
#--------start detection------------
@login_required(login_url='/error')
def n_detection(request):
    try:
        detection=request.POST.get("detection_value")
        if detection is None:
            t_detection=N_ditection.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_detection}
            return render(request,"detection/detection.html",context)
        else:
            p_detection=request.POST["detection_value"]
            m_detection=N_ditection(d_ditection=p_detection)
            m_detection.save()
            messages.success(request,'succeessfully detection created')
            t_detection=N_ditection.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_detection}
            return render(request,"detection/detection.html",context)
    except Exception as e:
        messages.error(request,e)
        t_detection=N_ditection.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_detection}
        return render(request,"detection/detection.html",context)
@login_required(login_url='/error')
@csrf_exempt
def dlt_detection(request):
    try:
        d_id=request.POST["di_id"]
        N_ditection.objects.get(id=d_id).delete()
        messages.success(request,'successfully deleted')
        return HttpResponse("success")
    except Exception as e:
        messages.error(request,e)
        return HttpResponse("success")

def upd_detection(request):
    try:
        di_id=request.POST.get('detection_id')
        detection_value=request.POST.get('detection_value')
        if detection_value is None:
            t_detection=N_ditection.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_detection}
            return render(request,"detection/detection.html",context)
        else:
            N_ditection.objects.filter(id=di_id).update(d_ditection=detection_value)
            messages.success(request,'successfully update')
            t_detection=N_ditection.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_detection}
            return render(request,"detection/detection.html",context)
    except Exception as e:
        messages.error(request,e)
        t_detection=N_ditection.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_detection}
        return render(request,"detection/detection.html",context)


#---------end detection-----------------
#-----------start dispose---------------------
@login_required(login_url='/error')
def h_dispose(request):
    try:
        dispose=request.POST.get("dispose_value")

        if dispose is None:
            t_dispose=N_dispose.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_dispose}
            return render(request,"dispose/dispose.html",context)
        else:
            p_dispose=request.POST["dispose_value"]
            m_dispose=N_dispose(d_dispose=p_dispose)
            m_dispose.save()
            messages.success(request,"successfully created")
            t_dispose=N_dispose.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_dispose}
            return render(request,"dispose/dispose.html",context)
    except Exception as e:
           messages.error(request,e)
           t_dispose=N_dispose.objects.all()
           x,y= permission(request)
           context={"x":x,"y":y,"data":t_dispose}
           return render(request,"dispose/dispose.html",context)
@login_required(login_url='/error')
@csrf_exempt
def dlt_dispose(request):
    try:
        d_id=request.POST["ds_id"]
        N_dispose.objects.get(id=d_id).delete()
        messages.success(request,"successfully deleted")
        return HttpResponse("success")
    except Exception as e:
        messages.success(request,e)
        return HttpResponse("success")

@login_required(login_url='/error')
def upd_disposes(request):
    try:
        ds_id=request.POST.get("dispose_id")
        dispose_value=request.POST.get("dispose_value")
        if dispose_value is None:
            t_dispose=N_dispose.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_dispose}
            return render(request,"dispose/dispose.html",context)
        else:
            N_dispose.objects.filter(id=ds_id).update(d_dispose=dispose_value)
            messages.success(request,'successfully updated')
            t_dispose=N_dispose.objects.all()
            x,y= permission(request)
            context={"x":x,"y":y,"data":t_dispose}
            return render(request,"dispose/dispose.html",context)
    except Exception as e:
        messages.error(request,e)
        t_dispose=N_dispose.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_dispose}
        return render(request,"dispose/dispose.html",context)
#------------end dispose----------------
#------------start dalam--------------
@login_required(login_url='/error')
def dalam(request):
    dlm=request.POST.get("dalam_value")
    if dlm is None:
        t_dalam=N_dalam.objects.all()
        x,y= permission(request)

        context={
            "x":x,
            "y":y,
            "data":t_dalam
            }
        return render(request,"dalam/dalam.html",context)
    else:
        p_dalam=request.POST["dalam_value"]
        m_dalam= N_dalam(d_dalam=p_dalam)
        m_dalam.save()
        messages.success(request, 'dalam created successfully')
        t_dalam= N_dalam.objects.all()
        x,y= permission(request)
        context={"x":x,"y":y,"data":t_dalam}
        return render(request,"dalam/dalam.html",context)

@login_required(login_url='/error')
def dlt_dalam(request):
    try:
      dalam_id=request.POST["dalam_id"]
      N_dalam.objects.get(id=dalam_id).delete()
      messages.success(request,"successfully dalam  deleted")
      return HttpResponse("success")
    except Exception as e:
        messages.error(request,'e')
        return HttpResponse("success")

@login_required(login_url='/error')
def upd_dalam(request):
    dlm_id=request.POST.get('dalam_id')
    dalam_value=request.POST.get("dalam_value")
    if dalam_value is None:
        t_dalam= N_dalam.objects.all()
        x,y= permission(request)
        context={
            "x":x,
            "y":y,
            "data":t_dalam
            }
        return render(request,"dalam/dalam.html",context)
    else:
        N_dalam.objects.filter(id=dlm_id).update(d_dalam=dalam_value)
        messages.success(request, 'dalam update successfully !')
        t_dalam= N_dalam.objects.all()
        x,y= permission(request)
        context={
            "x":x,
            "y":y,
            "data":t_dalam
            }
        return render(request,"dalam/dalam.html",context)

#------------centralise database system---------------
@login_required(login_url='/error')
def centralise_database(request):

    if request.method=="POST":
            serial_data=request.POST.get("serial_value")
            bomb_value=request.POST.get("bomb_value")
            date_time=request.POST.get("date&time")
            location_data=request.POST.get("location_value")
            location_type=request.POST.get("location_data")
            location_description=request.POST.get("location_description")
            jurisdiction_data=request.POST.get("jurisdiction_data")
            incident_data=request.POST.get("incident_data")
            weight_data=request.POST.get("weight_data")
            explosive_data=request.POST.get("explosive_data")
            detonator_data=request.POST.get("detonator_data")
            switch_data=request.POST.get("switch_data")
            target_data=request.POST.get("target_data")
            death_data=request.POST.getlist("death_value")
            death_contact=request.POST.getlist('death_contact')
            injured_data=request.POST.getlist('injured_value')
            injured_contact=request.POST.getlist("injured_contact")
            distruction_data=request.POST.get("distruction_data")
            i_data=request.POST.get("i_data")
            explode_name=request.POST.getlist("explode_name")
            explode_contact=request.POST.getlist("explode_contact")

            mode_detection=request.POST.get("mode_detection")
            mode_description=request.POST.get("mode_description")
            detected_name=request.POST.get("detected_name")
            detected_contact=request.POST.get("detected_contact")
            detcted_despose=request.POST.get("detected_despose")
            despose_name=request.POST.get('despose_name')
            despose_contact=request.POST.get("despose_contact")
            assume_data=request.POST.get("assume_data")
            assume_status=request.POST.get("assume_status")
            dalam_data=request.POST.get("dalam_data")
            learning_data=request.POST.get("learning_data")
            image1=request.FILES.getlist("incident_image")
            image2=request.FILES.getlist("special_image")
            image3=request.FILES.getlist("sketch_image")

            duplicate=Form_data.objects.filter(fserial=serial_data).count()
            if duplicate >=1:
                messages.info(request, 'Already Incident Serial Year Present Please Enter Another Incident Serial year ')
            else:

               sub_data=Form_data(fserial=serial_data,d_bomb= bomb_value,fdate=date_time,
                               flocation=location_data, flocation_type=location_type,
                               flocation_description=location_description,fjuridiction=jurisdiction_data,
                               fincident=incident_data,fweight_data=weight_data,fexplosive=explosive_data,
                               fdetonator=detonator_data,fswitch=switch_data,ftarget=target_data,
                               fdistruction=distruction_data,fassume=assume_data,fassume_status_new=assume_status,
                               radio_data=i_data,fdalam=dalam_data,flearning=learning_data,
                               mode_of_detection=mode_detection,detected_description=mode_description,
                               detected_pname=detected_name,detcted_contact=detected_contact,
                               detected_dispose=detcted_despose,dispose_name=despose_name,dispose_contact=despose_contact,edit_request=0,delete_request=0,
                               user_id=request.user.id)
               sub_data.save()
               f_key=Form_data.objects.filter(fserial=serial_data).values("id")[0]
               f_key=f_key['id']
          #--------------death_data--------------------
               if death_data is not None:

                    for a ,b in enumerate(death_data):
                        new_death_contact=(death_contact[a])
                        new_death=(death_data[a])
                        death_person(form_id=f_key,death_name=new_death,death_contact=new_death_contact).save()
         #---------------injured_data----------------------
               if injured_data is not None:
                    for x,y in enumerate(injured_data):
                        new_injured_person=injured_data[x]
                        new_injured_contact=injured_contact[x]

                        injured_person(form_id=f_key,injured_name=new_injured_person, injured_contact=new_injured_contact).save()

               if i_data == 'Exploded':
                    for  c,d in enumerate(explode_name):
                        new_exploded_name=explode_name[c]
                        new_exploded_contact=explode_contact[c]
                        exploded(form_id=f_key, exploded_name=new_exploded_name,explode_contact=new_exploded_contact).save()
#--------------------------------image---------------------------------------------------------

                #-----------image1----------------
               if image1 is not None:
                    for img in image1:
                        str_img=str(img)

                    path1,path2,path3=path_x()

                    for x in request.FILES.getlist("incident_image"):
                        ts = my_timestamp()
                        tv=my_timestamp_video()
                        x_str=str(x)
                        split_img=x_str.split('.')

                        if split_img[1]=='mp4':
                            def process(f):
                                with open(path1 + tv, 'wb+') as destination:
                                    for chunk in f.chunks():
                                        destination.write(chunk)
                            process(x)
                            status=1
                            images(form_id=f_key,im_vi=tv,status=status).save()
                        else:

                            def process(f):
                                with open(path1 + ts, 'wb+') as destination:
                                    for chunk in f.chunks():
                                        destination.write(chunk)
                            process(x)
                            status=0
                            images(form_id=f_key,im_vi=ts,status=status).save()

#----------image2------------

               if image2 is not None:

                     for x in request.FILES.getlist("special_image"):
                         ts_p=my_timestamp_pdf()
                         def process(f):
                             with open(path2 + ts_p, 'wb+') as destination:
                                 for chunk in f.chunks():
                                     destination.write(chunk)
                         process(x)
                         s_report(form_id=f_key,special_report=ts_p).save()



            #--------------image3----------------
               if image3 is not None:

                    for x in request.FILES.getlist("sketch_image"):
                        ts = my_timestamp()
                        def process(f):
                            with open(path3 + ts, 'wb+') as destination:
                                for chunk in f.chunks():
                                    destination.write(chunk)
                        process(x)
                        sk_report(form_id=f_key,sketch_scence=ts).save()

                    messages.success(request,"form submited successfully")

    ty_location= N_location.objects.all()
    t_jurisdiction=N_juridiction.objects.all()
    t_incident=N_incident.objects.all()
    t_weight=N_weight.objects.all()
    t_explosive=N_explosive.objects.all()
    t_c_status=N_assused.objects.all()
    t_dalam=N_dalam.objects.all()
    t_dispose=N_dispose.objects.all()
    t_detection= N_ditection.objects.all()
    return render(request,"main_form/plain_page.html",{"data1":ty_location,"data2":t_jurisdiction,"data3":t_incident,"data4":t_weight,
    "data5": t_explosive,"data6":t_c_status,"data7":t_dalam,"data8":t_dispose,"data9":t_detection})
#-------------------start view subdata------------------------
@login_required(login_url='/error')
def view_submitdata(request):
    user = request.user
    user_id = request.user.id
    super_user=user.is_superuser

    if super_user is False:
        serial_data=request.POST.get("serial_value")
        x,y= permission(request)
        t_form_module=join_location(request)
        context={"x":x,"y":y,"data":t_form_module}
        return render(request,"view_data/view_data.html",context)
    else:
        serial_data=request.POST.get("serial_value")
        x,y= permission(request)
        #t_form_module=join_location(request)
        t_form_module=Form_data.objects.all().select_related('user')


        context={"x":x,"y":y,"data":t_form_module}
        return render(request,"sp_logine/view_data.html",context)
@login_required(login_url='/error')
def edit_request(request):
    try:
       if request.method=="POST":
           id=request.POST['id']
           req=request.POST['req']
           Form_data.objects.filter(id=id).update(edit_request=req)
           messages.success(request,'edit request send succeessfully ......')
           return HttpResponse("success")
    except Exception as e:
        messages.error(request,e)
        return HttpResponse("success")
@login_required(login_url='/error')
def dlt_request(request):
    try:
        if request.method=="POST":
            id=request.POST['id']
            req=request.POST['req']
            Form_data.objects.filter(id=id).update(delete_request=req)
            messages.success(request,'delete request send successfuly.....')
            return HttpResponse('success')
    except Exception as e:
            messages.error(request,e)
            return HttpResponse('success')



@login_required(login_url='/error')
def dlt_subdata(request):
    f_id=request.POST["f_id"]
    path1,path2,path3=path_x()

    try:
            img=(images.objects.filter(form_id=f_id).values('im_vi'))
            x=[path1+x['im_vi']  for x in img]
            for y in x:
                if os.path.exists(y):
                    os.remove(y)
                else:
                  pass
            report=(s_report.objects.filter(form_id=f_id).values('special_report'))
            report=[path2+x['special_report']  for x in report]
            for z in report:
                if os.path.exists(z):
                   os.remove(z)
                else:
                    pass
            sketch=sk_report.objects.filter(form_id=f_id).values('sketch_scence')
            sketch=[path3+x['sketch_scence'] for x in sketch]
            for v in sketch:
                if os.path.exists(v):
                    os.remove(v)
                else:
                    pass
            Form_data.objects.get(id=f_id).delete()
            messages.success(request,'form successfully deleted')
    except Exception as e:
       messages.error(request,e)
    finally:
        return HttpResponse("success")
@login_required(login_url='/error')
def update_form(request,id):
    #id=request.POST.get('id')
    try:
        view_details= join_all_data(id)
        #content={"data1":view_details}
        #return render(request,'view_data/update_details.html',content)

    except Exception as e:
        messages.error(request,e)
    finally:
        #print("details_id=====",id)
        view_details= join_all_data(id)
        #print(view_details)
        death_persons=death_person.objects.filter(form_id=id)
        injured_persons=injured_person.objects.filter(form_id=id)
        exploded_data=exploded.objects.filter(form_id=id)
        image_video=images.objects.filter(form_id=id)
        special_report=s_report.objects.filter(form_id=id)
        sketch_image=sk_report.objects.filter(form_id=id)
        t_detection= N_ditection.objects.all()
        t_dispose=N_dispose.objects.all()

        return render(request,'view_data/update_details.html',{"data1":view_details,"data2":death_persons,"data3":injured_persons,
                                                             "data4":exploded_data,"data5":image_video,"data6":special_report,
                     "data7":sketch_image,'data8': t_detection,"data9": t_dispose})


@login_required(login_url='/error')
def update_form_first(request,id):
    "update first portion of details form"

    if request.method=="POST":
            seril_number=request.POST.get('serial_uvalue')
            bomb_uvalue=request.POST.get('bomb_uvalue')
            date_uvalue=request.POST.get('date_uvalue')
            location_uvalue=request.POST.get('loacation_uvalue')
            location_ty_uvalue=request.POST.get('location_ty_uvalue')
            location_dy_uvalue=request.POST.get('location_dy_uvalue')
            juridiction_uvalue=request.POST.get('juridiction_uvalue')
            incident_uvalue=request.POST.get('incident_uvalue')
            explosive_uvalue=request.POST.get('explosive_uvalue')
            weight_uvalue=request.POST.get('weight_uvalue')
            detonator_uvalue=request.POST.get('detonator_uvalue')
            switch_uvalue=request.POST.get('switch_uvalue')
            target_uvalue=request.POST.get('target_uvalue')
            distruction_uvalue=request.POST.get('distruction_uvalue')
            assused_uvalue=request.POST.get('assused_uvalue')
            assused_status_uvalue=request.POST.get('assused_status_uvalue')
            mistake_uvalue=request.POST.get('mistake_uvalue')
            dalam_uvalue=request.POST.get('dalam_uvalue')
            i_data=request.POST.get('i_data')
            #----------------mode_of_detection---------------
            mode_detection=request.POST.get('mode_detection')
            mode_description=request.POST.get('mode_description')
            detcted_name=request.POST.get('detected_name')
            detected_contact=request.POST.get('detected_contact')
            detcted_despose=request.POST.get('detected_despose')
            despose_name=request.POST.get('despose_name')
            despose_contact=request.POST.get('despose_contact')
            #-----------------explode_nmae/contacts-------------
            explode_name=request.POST.getlist('explode_name')
            explode_contact=request.POST.getlist('explode_contact')


            Form_data.objects.filter(id=id).update(fserial=seril_number,d_bomb=bomb_uvalue,
                fdate=date_uvalue,flocation=location_uvalue,flocation_type=location_ty_uvalue,
                flocation_description=location_dy_uvalue,fjuridiction=juridiction_uvalue,
                fincident=incident_uvalue,fweight_data=weight_uvalue,fexplosive= explosive_uvalue,
                fdetonator=detonator_uvalue,fswitch=switch_uvalue,ftarget=target_uvalue,
                fdistruction=distruction_uvalue,fassume=assused_uvalue,fdalam=dalam_uvalue,
                fassume_status_new=assused_status_uvalue,flearning=mistake_uvalue,radio_data=i_data,
              )
            messages.success(request,"form update successfully")
    view_details= join_all_data(id)
    ty_location= N_location.objects.all()
    t_jurisdiction=N_juridiction.objects.all()
    t_incident=N_incident.objects.all()
    t_explosive=N_explosive.objects.all()
    t_weight=N_weight.objects.all()
    t_c_status=N_assused.objects.all()
    t_dalam=N_dalam.objects.all()
    t_detection= N_ditection.objects.all()
    t_dispose=N_dispose.objects.all()
    explode_data=exploded.objects.filter(form_id=id)
    context={"data1":view_details,"data2":ty_location,
             "data3":t_jurisdiction,"data4":t_incident,
             'data5':t_explosive,'data6':t_weight,
             "data7":t_c_status,"data8":t_dalam,
             "data9":t_detection,"data10":t_dispose,
            }
    return render(request,"view_data/update_first.html",context)

@login_required(login_url='/error')
def view_details_data(request,id):
    #id=request.POST['id']
    #print("details_id=====",id)
    view_details= join_all_data(id)
    #print(view_details)
    death_persons=death_person.objects.filter(form_id=id)
    injured_persons=injured_person.objects.filter(form_id=id)
    exploded_data=exploded.objects.filter(form_id=id)
    image_video=images.objects.filter(form_id=id)
    special_report=s_report.objects.filter(form_id=id)
    sketch_image=sk_report.objects.filter(form_id=id)
    return render(request,"view_data/view_details.html",{"data1":view_details,"data2":death_persons,"data3":injured_persons,
                                                         "data4":exploded_data,"data5":image_video,"data6":special_report,
                                                         "data7":sketch_image})
#---------------------update_date_persone------------
@login_required(login_url='/error')
def upd_death_person(request):

    id_form=request.POST.get('form_id')
    name=request.POST.getlist('death_name')
    contacts=request.POST.getlist('death_contacts')
    death_person.objects.filter(form_id=id_form).delete()
    try:
        for a ,b in enumerate(name):
            new_death_contact=(contacts[a])
            new_death=(name[a])
            death_person(form_id=id_form,death_name=new_death,death_contact=new_death_contact).save()
        messages.success(request, "person add successfully")
    except Exception as e:
        messages.error(request,'something wrong please try againe')
    return redirect('updfdata/'+str(id_form))
def dlt_death_persone(request):
    id =request.POST['id']
    try:
        death_person.objects.filter(id=id).delete()
        messages.success(request,"person delete successfully")
    except:
        messages.error(request,"something wrong please try againe")
    finally:
            return HttpResponse("success")
#------------------------update_injured_persone----------
@login_required(login_url='/error')
def upd_injured_persone(request):
    injured_name=request.POST.getlist('injured_name')
    injured_contacts=request.POST.getlist('injured_contacts')
    id=request.POST.get('form_id')
    injured_person.objects.filter(form_id=id).delete()

    try:
        for x,y in enumerate(injured_name):
            new_injured_person=injured_name[x]
            new_injured_contact=injured_contacts[x]
            injured_person(form_id=id,injured_name=new_injured_person, injured_contact=new_injured_contact).save()
        messages.success(request,'person add successfully')
    except:
        messages.error(request,'something wrong try againe')
    finally:
        return redirect('updfdata/'+str(id))
def dlt_injured_persone(request):
   id=request.POST['id']
   try:
       injured_person.objects.filter(id=id).delete()
       messages.success(request, "injured person deleted successfully")
   except Exception as e:
       messages.error(request,"something wrong please try againe")
   finally:
       return HttpResponse("success")
#-------------------exploded_update------------------
@login_required(login_url='/error')
def upd_exploded(request):
    id=request.POST.get("form_id")
    explode_name=request.POST.getlist('exploded_name')
    explode_contact=request.POST.getlist('exploded_contacts')
    exploded.objects.filter(form_id=id).delete()
    try:
        for  c,d in enumerate(explode_name):
            new_exploded_name=explode_name[c]
            new_exploded_contact=explode_contact[c]
            exploded(form_id=id, exploded_name=new_exploded_name,explode_contact=new_exploded_contact).save()
        messages.success(request,"injured persone successfully update")
    except:
        messages.error(request,'something wring please try againe')

    return redirect('updfdata/'+str(id))
@login_required(login_url='/error')
def dlt_exploded(request):
    id=request.POST['id']
    try:
        exploded.objects.filter(id=id).delete()
        messages.success(request,"exploded successfully deleted")
    except:
        messages.error(request,'something wrong please try againe')
    finally:
        return HttpResponse("success")
#---------------update__disposed-------------
@login_required(login_url='/error')
def update_disposes(request):
    mode_detection=request.POST.get('mode_detection')
    description=request.POST.get('detction_description')
    detected_name=request.POST.get('detected_name')
    detected_contacts=request.POST.get('detected_contacts')
    detected_despose=request.POST.get('detected_despose')
    despose_name=request.POST.get('dispose_name')
    despose_contacts=request.POST.get('despose_contacts')
    id_form=request.POST.get('form_id')
    try:
        Form_data.objects.filter(id=id_form).update(mode_of_detection=mode_detection, detected_description=description, detected_pname=detected_name, detcted_contact=detected_contacts, detected_dispose=detected_despose, dispose_name=despose_name, dispose_contact=despose_contacts)
        messages.success(request,'successfully save')
    except Exception as e:
        messages.error(request,e)
    finally:

         return redirect('updfdata/'+str(id_form))

#------------------delete_images----------------------
@login_required(login_url='/error')
def dlt_img(request):
    id=request.POST['id']
    img_path=request.POST['img_path']
    path1,path2,path3=path_x()
    full_path=path1+ img_path

    if request.method=='POST':
        try:
            images.objects.filter(id=id).delete()
            if os.path.isfile(full_path):
                os.remove(full_path)
            messages.success(request, "suceesfully image deleted")
        except Exception as e:
            messages.error(request,e)
        finally:
            return HttpResponse("success")
@login_required(login_url='/error')
def add_img(request):
  id=request.POST.get('form_id')
  file_image = request.FILES.getlist("image_name")
  path1,path2,path3=path_x()
  if request.method=="POST":
      try:

              for x in request.FILES.getlist("image_name"):
                  ts = my_timestamp()
                  tv=my_timestamp_video()
                  x_str=str(x)
                  split_img=x_str.split('.')
                  if split_img[1]=='mp4':
                      def process(f):
                          with open(path1 + tv, 'wb+') as destination:
                              for chunk in f.chunks():
                                  destination.write(chunk)
                      process(x)
                      status=1
                      images(form_id=id,im_vi=tv,status=status).save()
                  else:

                      def process(f):
                          with open(path1 + ts, 'wb+') as destination:
                              for chunk in f.chunks():
                                  destination.write(chunk)
                      process(x)
                      status=0
                      images(form_id=id,im_vi=ts,status=status).save()
              messages.success(request, "image upload successfully")
      except Exception as e:
             messages.error(request,"something wrong  try again")
      finally:

          return redirect('updfdata/'+id)
#-------------dlt_special_reports--------------
@login_required(login_url='/error')
def dlt_special_report(request):
   id=request.POST['id']
   report_path=request.POST['report_path']
   path1,path2,path3=path_x()
   full_path=path2+ report_path
   if request.method=="POST":
       try:
           s_report.objects.filter(id=id).delete()
           if os.path.isfile(full_path):
              os.remove(full_path)
           messages.success(request,'successfully report deleted')
       except Exception as e:
           messages.error(request,'something wrong please delete againe')
       finally:
           return HttpResponse("success")
@login_required(login_url='/error')
def add_special_reports(request):
  id=request.POST.get('id')
  path1,path2,path3=path_x()

  if request.method=='POST':
     try:

          for x in request.FILES.getlist("reports_name"):
              ts_p=my_timestamp_pdf()
              def process(f):
                  with open(path2 + ts_p, 'wb+') as destination:
                      for chunk in f.chunks():
                          destination.write(chunk)
              process(x)
              s_report(form_id=id,special_report=ts_p).save()
          messages.success(request,'reports upload successfully')
     except Exception as e:
          messages.error(request,'something wron please try againe')
     finally:
              return redirect('updfdata/'+id)
#----------------dlt_sketch_scence----------
@login_required(login_url='/error')
def dlt_sketch_scence(request):
    id=request.POST['id']
    sketch_path=request.POST['sketch_path']
    path1,path2,path3=path_x()
    full_path=path3+sketch_path
    if request.method=='POST':
        try:
            sk_report.objects.filter(id=id).delete()
            if os.path.isfile(full_path):
                os.remove(full_path)
            messages.success(request,'successfully deleted')
        except Exception as e:
            messages.error(request,e)
        finally:
           return  HttpResponse('success')
@login_required(login_url='/error')
def add_sketch(request):
    path1,path2,path3=path_x()
    id=request.POST.get('id')
    a=request.FILES.getlist("sketch_name")

    if request.method=='POST':
        try:

            for x in request.FILES.getlist("sketch_name"):
                ts = my_timestamp()
                def process(f):
                    with open(path3 + ts, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                process(x)
                sk_report(form_id=id,sketch_scence=ts).save()
            messages.success(request, "successfully add sketch")
        except Exception as e:
            messages.error(request,'something wrong please try againe')
        finally:
                return redirect('updfdata/'+id)




#-----------------------------api_start--------------------------------------------------------
#-------------designation_api---------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def designation_api(request):
    if (request.method=='GET'):
        designation_obj= N_degignation.objects.all()
        serilize_obj=designation_serilizer(designation_obj,many=True)
        return Response(serilize_obj.data)

#-----------location_api----------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def location_api(request):
    if(request.method=='GET'):
        location_obj=N_location.objects.all()
        serilize_obj=location_serilization(location_obj,many=True)
        return Response(serilize_obj.data)
#-----------juridiction_api--------------

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def juridiction_api(request):

     if(request.method=='GET'):
         juridiction_obj=N_juridiction.objects.all()
         serilizer_obj=juridiction_serilization(juridiction_obj,many=True)
         return Response(serilizer_obj.data)
#-------------incident_api-------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def incident_api(request):
    if(request.method=="GET"):
        incident_obj=N_incident.objects.all()
        serilizer_obj=incident_serilization(incident_obj,many=True)
        return Response(serilizer_obj.data)
#---------------------weight--------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def weight_api(request):
  if(request.method=="GET"):
      weight_obj=N_weight.objects.all()
      serilizer_obj=weight_serilization(weight_obj,many=True)
      return Response(serilizer_obj.data)
#--------------------explosive_api-------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def explosive_api(request):
    if(request.method=="GET"):
        explosive_obj=N_explosive.objects.all()
        serilizer_obj=explosive_serilization(explosive_obj,many=True)
        return Response(serilizer_obj.data)
#--------------assused-----------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def assused_api(request):
        if(request.method=="GET"):
            assused_obj=N_assused.objects.all()
            serilizer_obj=assused_serilization(assused_obj,many=True)
            return Response(serilizer_obj.data)
#------------------post_api--------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def post_api(request):
     if(request.method=="GET"):
         post_obj=N_post.objects.all()
         serilizer_obj=post_serilization(post_obj,many=True)
         return Response(serilizer_obj.data)
#----------------detection_api---------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def ditection_api(request):
      if(request.method=="GET"):
          ditection_obj=N_ditection.objects.all()
          serilization_obj=detection_serilization(ditection_obj,many=True)
          return Response(serilization_obj.data)
#------------------despose_api-------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def despose_api(request):
    if request.method=='GET':
        despose_obj=N_dispose.objects.all()
        serilization_obj=despose_serilization(despose_obj,many=True)
        return Response(serilization_obj.data)
#--------------------dalam------------------
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def dalam_api(request):
    if request.method=="GET":
        dalam_obj=N_dalam.objects.all()
        serilization_obj=dalam_serilization(dalam_obj,many=True)
        return Response(serilization_obj.data)

#--------------form_api-------------------
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def form_api(request):
    fserial_no = request.data.get('fserial')
    if Form_data.objects.filter(fserial=fserial_no).exists():
        return Response({"msg": "Serial number already exists"}, status=status.HTTP_400_BAD_REQUEST)
    serialize = form_serilization(data=request.data)
    if serialize.is_valid():
        obj_id = serialize.save()
    death_person = request.data.get('death',[])
    if death_person  and obj_id is not None:
        death_person = [{"form":obj_id.id,**item} for item in death_person]
        serialize_death = death_serilizer(data= death_person,many=True)
        if serialize_death.is_valid():
            serialize_death.save()
    injured_person_data = request.data.get('injured',[])
    if injured_person_data and obj_id is not None:
        injured_person_data = [{"form":obj_id.id,**item} for item in injured_person_data]
        serialize_injured = injured_serilizer(data=injured_person_data,many=True)
        if serialize_injured.is_valid():
            serialize_injured.save()
    exploded_data = request.data.get('explode') 
    if exploded_data and obj_id is not None:
        exploded_data = [{'form':obj_id.id,**item} for item in exploded_data]
        serialize_explode = exploded_serilizer(data=exploded_data,many=True)
        if serialize_explode.is_valid():
            serialize_explode.save()
            return Response({"msg":"form have been save successfully"},status=status.HTTP_200_OK)
      
   
  



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_view(request):
    id  = request.data.get('id')
    form_instance = get_object_or_404(Form_data, pk=id)
    serialize_form_data = form_serilization(form_instance).data
    data = {
        'form_data': serialize_form_data,   # Include Form_data fields
        'death_data': list(form_instance.death_person_set.values()),  # Related Death_person instances
        'injured_data': list(form_instance.injured_person_set.values()),  # Related Injured_person instances
        'explode_data': list(form_instance.exploded_set.values()),  # Related Exploded instances
        'image_data': list(form_instance.images_set.values()),  # Related Images instances
        'reports_data': list(form_instance.s_report_set.values()),  # Related S_report instances
        'sketch_data': list(form_instance.sk_report_set.values()),  # Related Sk_report instances
    }
    return Response(data)  
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_only(request):
    id=request.data.get('id')
    form_instance = get_object_or_404(Form_data,pk=id)
    serializers = form_serilization(form_instance).data
    return Response(serializers,status=status.HTTP_200_OK)
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def images_api(request):
    try:
        id=request.data.get('id')
        for vimg in request.FILES.getlist('im_vi'):
            data = {'form': id, 'im_vi': vimg}
            if vimg.name.endswith(('.mp4','avi', 'mov', 'mkv')):
                data['status'] = 1
            elif vimg.name.endswith(('.png', '.jpg')):
                data['status'] = 0
            else:
                continue  # Skip files with other extensions
            serializer = image_serilizer(data=data)
            if serializer.is_valid():
                serializer.save()
        for report in request.FILES.getlist('special_reports'):
            data_02 = {'form':id,'special_report':report}
            serializer_02 = reports_serilizer(data=data_02) 
            if serializer_02.is_valid():
                serializer_02.save()
        for sketch in request.FILES.getlist('sketch_scences'):
            data_03 = {'form':id,'sketch_scence':sketch}
            serializer_03 = sketch_serializer(data = data_03)
            if serializer_03.is_valid():
                serializer_03.save()
        return Response({'status':200,'msg':'all document upload successfully'})
    except Exception as e:
        return Response({'status': 500, 'msg': 'An error occurred while processing the request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

#----------------------logine_api----------------------------------------
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user.is_superuser:
            return Response({"msg":"invalied credential","status":400})
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'Mobile_No':user.username,
                'User_Name':user.first_name,
                'status':200,
              })


#-----------logout_api----------------------------------
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def logout_api(request):
    request.user.auth_token.delete()
    return Response({"status":200,"message":"successfully logout"})


