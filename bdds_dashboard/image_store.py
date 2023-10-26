# -*- coding: utf-8 -*-
#from django.db import cursor
from .models import *
from django.db import connection
from bdds_dashboard.models import *
import time
import os
import re
from datetime import datetime
from django.contrib.auth.models import *
from django.conf import settings
from django.contrib.auth.models import User
import matplotlib.pyplot as plt
import matplotlib
from django.db import connection
matplotlib.use('SVG')
import io
import urllib,base64
import numpy as np
from io import BytesIO
def path_x():
    path1='C:/Cluematrix/bdds/static/images/image1_folder/'
    path2='C:/Cluematrix/bdds/static/images/image2_folder/'
    path3='C:/Cluematrix/bdds/static/images/image3_folder/'
    return (path1,path2,path3)


def save_image_to_folder(value,img_path):
    # Create the file path to save the image in the Django static/img folder
    #img_path=imgk_path
    img=img_path
    image_name = value
    image_path = f'E:/Gadcchiroli_BDDS/images/{img}/{image_name}'
    print("image_Path===",image_path)
    # Open the image file and save it to the folder
    with open(image_path, 'wb+') as destination:
        if type(value) == str:
            destination.write(value.encode())
        else:
             for chunk in value.chunks():
                destination.write(chunk)

    # Return the image path
    return image_path
def join_location(request):
    user_id=request.user.id
    print(user_id)
    if request.user.is_superuser:
        query=Form_data.objects.raw('''
                SELECT USER.*, loc.l_location FROM `bdds_dashboard_form_data`
                AS USER LEFT JOIN `bdds_dashboard_n_location`
                AS loc ON USER.flocation_type = loc.id
                ORDER BY USER.id''')
        return(query)
    else:

       query=Form_data.objects.raw('''
            SELECT USER.*, loc.l_location FROM `bdds_dashboard_form_data`
            AS USER LEFT JOIN `bdds_dashboard_n_location`
            AS loc ON USER.flocation_type = loc.id
           WHERE user_id='%s' ORDER BY USER.id''',[user_id])
       return(query)


def join_all_data(id):
    user_id=id
    cursor = connection.cursor()
    #print("id=id===",id)
    #query=('SELECT USER.*, location.l_location FROM `bdds_dashboard_form_data` AS USER LEFT JOIN `bdds_dashboard_n_location` AS location ON location.id = USER.flocation_type WHERE USER.id = 211 ORDER BY USER.id;')
    #query=('SELECT USER.*, location.l_location, jdction.l_juridiction, ident.i_incident, wght.w_weight, texplosive.e_explosive, asmdetails.a_assused, dlm.d_dalam, ds.d_dispose FROM `bdds_dashboard_form_data` AS USER LEFT JOIN `bdds_dashboard_n_location` AS location ON location.id = USER.flocation_type LEFT JOIN `bdds_dashboard_n_juridiction` AS jdction ON jdction.id = USER.fjuridiction LEFT JOIN `bdds_dashboard_n_incident` AS ident ON ident.id = USER.fjuridiction LEFT JOIN `bdds_dashboard_n_weight` AS wght ON wght.id = USER.fweight_data LEFT JOIN `bdds_dashboard_n_explosive` AS texplosive ON texplosive.id = USER.fexplosive LEFT JOIN `bdds_dashboard_n_assused` AS asmdetails ON asmdetails.id = USER.fassume_status_new LEFT JOIN `bdds_dashboard_n_dalam` AS dlm ON dlm.id = USER.fdalam LEFT JOIN `bdds_dashboard_n_dispose` AS ds ON ds.id=USER.detected_dispose WHERE user.id='+"'"+str(user_id)+"'"'ORDER BY user.id')
    querys=Form_data.objects.raw('''
           SELECT USER.*, location.l_location, jdction.l_juridiction, ident.i_incident,
           wght.w_weight, texplosive.e_explosive, asmdetails.a_assused, dlm.d_dalam,
           ds.d_dispose, ditection.d_ditection FROM `bdds_dashboard_form_data` AS USER LEFT JOIN `bdds_dashboard_n_location`
           AS location ON location.id = USER.flocation_type LEFT JOIN `bdds_dashboard_n_juridiction`
           AS jdction ON jdction.id = USER.fjuridiction LEFT JOIN `bdds_dashboard_n_incident`
           AS ident ON ident.id = USER.fjuridiction LEFT JOIN `bdds_dashboard_n_weight`
           AS wght ON wght.id = USER.fweight_data LEFT JOIN `bdds_dashboard_n_explosive`
           AS texplosive ON texplosive.id = USER.fexplosive LEFT JOIN `bdds_dashboard_n_assused`
           AS asmdetails ON asmdetails.id = USER.fassume_status_new LEFT JOIN `bdds_dashboard_n_dalam`
           AS dlm ON dlm.id = USER.fdalam LEFT JOIN `bdds_dashboard_n_dispose`
           AS ds ON ds.id=USER.detected_dispose
           LEFT JOIN `bdds_dashboard_n_ditection` as ditection ON ditection.id=USER.mode_of_detection
           WHERE USER.id= '%s' ORDER BY USER.id''',[user_id])

    print("print===>",querys)
    querys=Form_data.objects.raw(querys)
    return(querys)
    querys=Form_data.objects.raw(query)
    return(querys)

def user_join():
    query='SELECT USER.*, USER.username, USER.password, USER.email, user_logine.l_designation, user_logine.l_numbers, designation.d_designation FROM `auth_user` AS USER LEFT JOIN `bdds_dashboard_nlogines_creations` AS user_logine ON user_logine.user_id = USER.id LEFT JOIN `bdds_dashboard_n_degignation` as designation ON user_logine.l_designation=designation.id;'
    p = User.objects.raw(query)
    #print(p)
    return(p)

    #return(query)
def permission(request):
    '''permission edit delate'''
    try:
        user = request.user
        id=user.id
        print(user.is_superuser)
        if user.is_superuser:
            x=1
            y=1
            return(x,y)
        else:
            x=(Nlogines_creations.objects.filter(user_id=id).values("permission_edit"))[0]
            y=(Nlogines_creations.objects.filter(user_id=id).values('permission_delete'))[0]
            y=(y['permission_delete'])
            x=(x['permission_edit'])
            return(x,y)
    except Exception as e:

        return(None,None)




    return(user)

def my_timestamp():
    d = str(datetime.now())
    d = d.replace('.', '_')
    d = re.sub(r"\s+", "", d.replace(':', '_'), flags=re.UNICODE)+".png"
    return d

def my_timestamp_video():
    d = str(datetime.now())
    d = d.replace('.', '_')
    d = re.sub(r"\s+", "", d.replace(':', '_'), flags=re.UNICODE)+".mp4"
    return d
def my_timestamp_pdf():
    d = str(datetime.now())
    d = d.replace('.', '_')
    d = re.sub(r"\s+", "", d.replace(':', '_'), flags=re.UNICODE)+".pdf"
    return d
# def exploded_despose(dx,ex):
#     label = ["Exploded", "Detected"]
#     val = [dx,ex]

#     # append data and assign color
#     label.append("")
#     val.append(sum(val))  # 50% blank
#     colors = ['red',  'green', ]
#     text_prop = {'family':'sans-serif', 'fontsize':'x-large',
#              'fontstyle':'italic', 'fontweight':'light'}

#     # plot
#     plt.figure(figsize=(8,6),dpi=100)

#     wedges, labels=plt.pie(val, wedgeprops=dict(width=0.6,edgecolor='w'),labels=label, colors=colors,textprops =text_prop)
#     # I tried this method
#     wedges[-1].set_visible(False)

#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     buffer.close()

#     graphic = base64.b64encode(image_png)
#     graphic_file = graphic.decode('utf-8')
#     return graphic_file


# def death_injured_graph(d,i):

#     y = np.array([d, i ])
#     mylabels = ["Death", "Injured"]
#     myexplode = [0.2, 0]
#     #textprops = {"fontsize":15}
#     text_prop = {'family':'sans-serif', 'fontsize':'x-large',
#              'fontstyle':'italic', 'fontweight':'light'}

#     plt.pie(y, labels = mylabels, explode = myexplode,textprops =text_prop,autopct='%.1f%%', shadow = True)


#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     buffer.close()

#     graphic = base64.b64encode(image_png)
#     graphic = graphic.decode('utf-8')
#     return graphic

