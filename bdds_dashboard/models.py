from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your models here.

#---------------------permission---------------------


#-------------sp_authurity---------------------------
class Nsp_authourity(models.Model):
    s_name=models.CharField(max_length=200,null=True,blank=True)
    s_numbers=models.CharField(max_length=200,null=True,blank=True)
    s_designation=models.CharField(max_length=200,null=True,blank=True)
    s_email=models.EmailField(max_length=256,null=True,blank=True)
    s_password=models.CharField(max_length=200,null=True,blank=True)
    s_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#----------designation------------------------------
class N_degignation(models.Model):
     d_designation=models.CharField(max_length=200,null=True,blank=True)
     d_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#----------------post---------------------
class N_post(models.Model):
    p_post=models.CharField(max_length=200,null=True,blank=True)
    p_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#=================================================
class Nlogines_creations(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      l_numbers=models.CharField(max_length=200,null=True,blank=True)
      l_designation=models.CharField(max_length=200,null=True,blank=True)
      permission_edit=models.IntegerField(null=True, default='0', blank=True)
      permission_delete=models.IntegerField(null=True, default='0', blank=True)
      l_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True),
      join_designation=models.ForeignKey(N_degignation, on_delete=models.SET_NULL, blank=True,null=True)
      post=models.ForeignKey(N_post,on_delete=models.SET_NULL,blank=True,null=True)
# -------------------location--------------
class N_location(models.Model):
    l_location=models.CharField(max_length=200,null=True,blank=True)
    l_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#---------------------juridiction---------------
class N_juridiction(models.Model):
    l_juridiction=models.CharField(max_length=200,null=True,blank=True)
    l_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#--------------incident----------------------------------
class N_incident(models.Model):
      i_incident=models.CharField(max_length=200,null=True,blank=True)
      i_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#--------------weight-----------------------------
class N_weight(models.Model):
      w_weight=models.CharField(max_length=200,null=True,blank=True)
      w_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#--------------explosive----------------------
class N_explosive(models.Model):
     e_explosive=models.CharField(max_length=200,null=True,blank=True)
     e_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#----------------assused----------------
class N_assused(models.Model):
    a_assused=models.CharField(max_length=200,null=True,blank=True)
    a_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)

#-----------ditection------------
class N_ditection(models.Model):
    d_ditection=models.CharField(max_length=200,null=True,blank=True)
    di_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#--------------dispose--------------------
class N_dispose(models.Model):
    d_dispose=models.CharField(max_length=200,null=True,blank=True)
    ds_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)
#---------------------dalam------------
class N_dalam(models.Model):
    d_dalam=models.CharField(max_length=200,null=True,blank=True)
    d_datetime=models.DateTimeField(auto_now_add=True, blank=True,null=True)

class Form_data(models.Model):
    fserial=models.CharField(max_length=200,null=True,blank=True)
    d_bomb=models.CharField(max_length=200,null=True,blank=True)
    fdate=models.DateTimeField(null=True,blank=True)
    flocation=models.CharField(max_length=200,null=True,blank=True)
    flocation_type=models.ForeignKey(N_location,on_delete=models.SET_NULL,blank=True,null=True)
    flocation_description=models.TextField(null=True,blank=True)
    fjuridiction=models.ForeignKey(N_juridiction,  on_delete=models.SET_NULL,blank=True,null=True)
    fincident=models.ForeignKey(N_incident,on_delete=models.SET_NULL,null=True,blank=True)
    fweight_data=models.ForeignKey(N_weight,on_delete=models.SET_NULL,null=True,blank=True)
    fexplosive=models.ForeignKey(N_explosive, on_delete=models.SET_NULL,blank=True,null=True)
    fdetonator=models.CharField(max_length=200,null=True,blank=True)
    fswitch=models.TextField(null=True,blank=True)
    ftarget=models.CharField(max_length=200,null=True,blank=True)
    fdistruction=models.TextField(null=True,blank=True)
    fassume=models.TextField(null=True,blank=True)
    radio_data=models.CharField(max_length=200,null=True,blank=True)
    fir=models.CharField(max_length=200,null=True,blank=True)
    latitude=models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    longitude=models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    fdalam=models.ManyToManyField(N_dalam, blank=True)
    flearning=models.TextField(null=True,blank=True)
    fassume_status_new=models.ForeignKey(N_assused, on_delete=models.SET_NULL,blank=True,null=True)
#-------------------------------if detected-----------------------------------------------------------
    mode_of_detection=models.ForeignKey(N_ditection,on_delete=models.SET_NULL,blank=True,null=True)
    detected_description=models.TextField(max_length=200,null=True,blank=True)
    detected_pname=models.CharField(max_length=200,null=True,blank=True)
    detcted_contact=models.CharField(max_length=200,null=True,blank=True)
    detected_dispose=models.ForeignKey(N_dispose, on_delete=models.SET_NULL,blank=True,null=True)
    dispose_name=models.CharField(max_length=200,blank=True,null=True)
    dispose_contact=models.CharField(max_length=200,blank=True,null=True)
    edit_request=models.IntegerField(null=True,blank=True)
    delete_request=models.IntegerField(null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)


#---------------image_table----------------------------------------------------
def image_upload_to(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base, extension = os.path.splitext(filename)
    unique_filename = f"{timestamp}{extension}"
    return f'file/image1/{unique_filename}'
class images(models.Model):
    form=models.ForeignKey(Form_data, on_delete=models.CASCADE)
    im_vi=models.FileField(upload_to=image_upload_to,null=True,blank=True)
    status=models.IntegerField(null=True,blank=True)
def pdf_upload_to(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base, extension = os.path.splitext(filename)
    unique_filename = f"{timestamp}_{base}{extension}"
    return f'file/image2/{unique_filename}'    
class s_report(models.Model):
    form=models.ForeignKey(Form_data, on_delete=models.CASCADE)
    special_report=models.FileField(upload_to=pdf_upload_to,null=True,blank=True)
def sketch_upload_to(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base, extension = os.path.splitext(filename)
    unique_filename = f"{timestamp}{extension}"
    return f'file/image3/{unique_filename}'    
class sk_report(models.Model):
    form=models.ForeignKey(Form_data, on_delete=models.CASCADE)
    sketch_scence=models.ImageField(upload_to=sketch_upload_to,null=True,blank=True)


#-----------------------death_table----------------------------------
class death_person(models.Model):
    form=models.ForeignKey(Form_data, on_delete=models.CASCADE)
    death_name=models.CharField(max_length=200,null=True,blank=True)
    death_contact=models.CharField(max_length=200,null=True,blank=True)
#-------------------------injured_table------------------------------
class injured_person(models.Model):
    form=models.ForeignKey(Form_data, on_delete=models.CASCADE)
    injured_name=models.CharField(max_length=200,null=True,blank=True)
    injured_contact=models.CharField(max_length=200,null=True,blank=True)
#------------------exploded-----------------
class exploded(models.Model):
      form=models.ForeignKey(Form_data, on_delete=models.CASCADE)
      exploded_name=models.CharField(max_length=200,null=True,blank=True)
      explode_contact=models.CharField(max_length=200,null=True,blank=True)

from datetime import datetime
import os
class File(models.Model):
  file = models.FileField(blank=False, null=False)
  remark = models.CharField(max_length=20)
  timestamp = models.DateTimeField(auto_now_add=True)
def video_upload_to(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base, extension = os.path.splitext(filename)
    unique_filename = f"{timestamp}{extension}"
    return f'videos/{unique_filename}'

class video_image(models.Model):
     images = models.ImageField(upload_to='images/')  
     video = models.FileField(upload_to='video/')

'''
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

'''










