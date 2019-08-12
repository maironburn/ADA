from rest_framework import serializers
from core.vodafone.smart.user.models import User
from core.vodafone.smart.privclass.serializers import PrivclassSerializer

class UserSerializer(serializers.ModelSerializer):

    user_access2privclass = PrivclassSerializer()
    class Meta:

        model = User
        depth = 1
        fields =  ('s_login_name','user_access2privclass')
