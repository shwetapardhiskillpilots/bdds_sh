from django.contrib import admin
from django.urls import path,include
from bdds_dashboard import views
from bdds_dashboard.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import ObtainAuthToken



urlpatterns = [

    path('api-token-auth/', ObtainAuthToken.as_view()),
    path("",views.logine_page,name="login page"),
    path("logine_auth",views.index_page2,name="logine_authuntication"),
    path("index",views.index_page,name="index page"),
    path("logout",views.logout_page,name=" logout user"),
    path("error",views.error_page,name="error page"),
    #-----------user------------
    path("clogin",views.logine_creation,name="logine creation"),
    path("spauthority",views.sp_authority,name="sp authority"),
    path("users",views.all_user,name="all_users_data"),
    path('dltuser',views.dlt_user,name='delete user'),
    path('profile',views.user_profile,name='user_profile'),
    path('activate',views.user_activate,name='user activate deactivate'),
    path('chngepwd',views.forget_passwd,name='forgete'),
    #-------------request_edit/delete data--------
    path("editrequest",views.edit_request,name='edit_request'),
    path('dltrequest',views.dlt_request,name='delete requeste'),

    #--------------location---------------------
    path("tlocation",views.t_location,name="tlocation"),
    path("dlocation",views.dlt_location,name="dlocation"),
    path("updlocation",views.upd_location,name="update location"),
    path("apilocation",views.location_api,name='location api'),
    #----------------end location-------------------------
    #---------------start jurisdiction----------------
    path("jrusdiction",views.jurisdiction,name="jurisdiction"),
    path("dltjurisdiction",views.dlt_jurisdiction,name="delate jurisdiction"),
    path("updjuridiction",views.upd_juridiction,name="update juridiction"),
    path("apijuridiction",views.juridiction_api,name='api_juridiction'),

    #----------------end jurisdiction-----------------------
    #-----------------start incident------------------
    path("incident",views.t_incident,name="type of incident"),
    path("dltincident",views.dlt_incident,name="delate incident"),
    path("updincident",views.upd_incident,name="update incident"),
    path('apiincident',views.incident_api,name="update incident"),
    #--------------end incident-----------------------
    #------------start weight------------------
    path("weight",views.weight,name="type of weight"),
    path("dltweight",views.dlt_weight,name="delete weight"),
    path("updweight",views.upd_weight,name="update weight"),
    path("apiweight",views.weight_api,name="api weight"),
    #-------------------end weight---------------------
    #---------------start explosive-------------------
    path("explosive",views.t_explosive,name="type of explosive"),
    path("dltexplosive",views.dlt_explosive,name="delet explosive"),
    path("updexplosive",views.upd_explosive,name="update explosive"),
    path("master/apiexplosive",views.explosive_api,name="explosive api"),
    #-----------end explosive-----------------------
    path("a_status",views.a_current_status,name="assured current status"),
    path("dltstatus",views.dlt_c_status,name="delete status"),
    path('updstatus',views.upd_status,name="delate status"),
    path("master/assusedapi",views.assused_api,name="assused api"),
    #---------------end-----------
    #-------------start post---------
    path("post",views.post,name="post"),
    path("dltpost",views.dlt_post,name="delete post"),
    path("updpost",views.upd_post,name="update post"),
    path("master/postapi",views.post_api,name="post api"),
    #----------end post----------------
    #-----------start designation---------------
    path("designation",views.designation,name="designation"),
    path("dltdesignation",views.dlt_designation,name="delete designation"),
    path("upddesignation",views.upd_designation,name="update designation"),
    path("master/serdesignation",views.designation_api,name="serilize_designation"),
    #----------end designation---------------------
    #---------start detection---------------
    path("detection",views.n_detection,name="name of detection"),
    path("dltdetection",views.dlt_detection,name="delete detection"),
    path("upddetection",views.upd_detection,name="update detection"),
    path("master/ditectionapi",views.ditection_api,name="api detection"),
    #--------------------end detectipn--------------------
    #--------------start dispose-----------------
    path("dispose",views.h_dispose,name="how dispose"),
    path("dltdispose",views.dlt_dispose,name="delete dispose"),
    path('upddispose',views.upd_disposes,name="update dispose"),
    path('master/despose',views.despose_api,name="despose api"),
    #---------------start dispose----------------------
    path("dalam",views.dalam,name="master dalam"),
    path("dltdalam",views.dlt_dalam,name="delete dalam"),
    path("upddalam",views.upd_dalam,name="update dalam"),
    path("master/dalam",views.dalam_api,name="dalam api"),
    #---------------centalise_database_form--------------
    path("cdatabase",views.centralise_database,name="centralise_database form"),
    #================views_submit_data===================
    path("fdata",views.view_submitdata,name="views submit data"),
    path("dltfdata",views.dlt_subdata,name="delete submiit data"),
    path("viewdetails/<int:id>",views.view_details_data,name="viewdetails"),
    path("formapi",views.form_api,name="form submission api"),
    path("updfdata/<int:id>",views.update_form,name='update form'),
    path('updfdata/updatefirst/<int:id>', views.update_form_first,name='update first portion of form'),
    path('formviewapi',views.list_view,name='form_view_api'),
    path('listonly',views.list_only,name='list display only'),
# ---------------deleted_images------------------------
   path('dltimg',views.dlt_img,name="deleted images"),
   path('addimg',views.add_img,name='adding_images'),
   path('dltreport',views.dlt_special_report,name='delete special reports'),
   path('addreports',views.add_special_reports,name="add special reports"),
   path('dltsketch',views.dlt_sketch_scence,name='delete sketch scence'),
   path('addsketch',views.add_sketch,name='add sketch'),

#-----------update___dath---------------
   path('upddeath',views.upd_death_person,name='update death'),
   path('updinjured',views.upd_injured_persone,name='update injured'),
   path('dltdeath',views.dlt_death_persone,name='death_persone'),
   path('dltinjured',views.dlt_injured_persone,name='injured persone'),
   path('updexploded',views.upd_exploded,name="exploded name"),
   path('dltexploded',views.dlt_exploded,name='delete exploded'),
   path('updeatedispose',views.update_disposes,name='despose_update'),
    #_______________________mage_api_url_____________
   path('imageapi',views.images_api,name='image and video api'),
#--------------logine_with_api------------------
    path('logine/', CustomAuthToken.as_view()),
    path("logoutapi",views.logout_api,name="logout in api"),
#--------------testing_video---------------------------
  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
