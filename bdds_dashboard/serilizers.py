from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import  serializers
from bdds_dashboard.models import *
from .models import File


#-----------designation--------
class designation_serilizer(serializers.ModelSerializer):
    class Meta:
        model=N_degignation
        fields="__all__"
#---------location-----------
class location_serilization(serializers.ModelSerializer):
  class Meta:
      model=N_location
      fields="__all__"

#------------------juridiction-----------------
class juridiction_serilization(serializers.ModelSerializer):
    class Meta:
        model=N_juridiction
        fields="__all__"
#-------------incident----------------------
class incident_serilization(serializers.ModelSerializer):
    class Meta:
        model=N_incident
        fields="__all__"
#---------weigth---------------
class weight_serilization(serializers.ModelSerializer):
  class Meta:
        model=N_weight
        fields="__all__"
#--------------explosive-----------
class  explosive_serilization(serializers.ModelSerializer):
    class Meta:
        model=N_explosive
        fields="__all__"

#---------------assused----------
class assused_serilization(serializers.ModelSerializer):
    class Meta:
        model=N_assused
        fields="__all__"
#-----------post------------
class post_serilization(serializers.ModelSerializer):
    class Meta:
         model=N_post
         fields="__all__"
#--------------detection_serilization-------------
class detection_serilization(serializers.ModelSerializer):
   class  Meta:
       model=N_ditection
       fields="__all__"

#---------despose_serilization-------------
class despose_serilization(serializers.ModelSerializer):
    class Meta:
        model=N_dispose
        fields="__all__"
#---------dalam_serilization-------------
class dalam_serilization(serializers.ModelSerializer):
    class Meta:
        model=N_dalam
        fields="__all__"

#-------------form_data_serilization---------------
class form_serilization(serializers.ModelSerializer):
    class Meta:
        model=Form_data
        fields="__all__"
#--------------form_serialization-----------
class form_list(serializers.ModelSerializer):
    class Meta:
        model=Form_data
        fields=('id','fserial','d_bomb','fdate', 'flocation','flocation_type')
#----------------image/video----------------
class images_serilizer(serializers.ModelSerializer):

    class Meta:
        model=images
        fields='__all__'

#---------------death_serilizer
class death_serilizer(serializers.ModelSerializer):
    class Meta:
        model=death_person
        fields = '__all__'

class injured_serilizer(serializers.ModelSerializer):
    class Meta:
        model=injured_person
        fields = '__all__'
#------------exploded------------------
class exploded_serilizer(serializers.ModelSerializer):
    class Meta:
        model=exploded
        fields = '__all__'

class image_serilizer(serializers.ModelSerializer):
    class Meta:
        model=images
        # exclude = ('form', )
        fields = '__all__'

class reports_serilizer(serializers.ModelSerializer):
    class Meta:
        model=s_report
        fields = '__all__'
class sketch_serializer(serializers.ModelSerializer):
    class Meta:
        model=sk_report
        fields = '__all__'

class image_videoSerializer(serializers.ModelSerializer):
    class Meta:
        model=video_image
        fields = '__all__'        

''' def  validate(self, data):
        if data['im_vi']  is not None:

         raise serializers.ValidationError("hi")
        else:
            raise serializers.ValidationError("No")
        return data'''

#class FileSerializer(serializers.Serializer):
#    file = serializers.FileField(max_length=None, allow_empty_file=False)

'''class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = File
    fields = ('file', 'remark', 'timestamp')'''








