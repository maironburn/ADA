from rest_framework import serializers
from .models import Tunnelssh

class TunnelSSHSerializer(serializers.ModelSerializer):       
    
    def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.host = validated_data.get('host', instance.host)
            instance.port = validated_data.get('port', instance.port)
            instance.target_host = validated_data.get('target_host', instance.target_host)
            instance.target_port = validated_data.get('target_port', instance.target_port)
            instance.tunnel_type = validated_data.get('tunnel_type', instance.tunnel_type)

            if (str(instance.tunnel_type) == "0"):
                instance.parent_tunnel=None
                instance.tunnel_host = validated_data.get('tunnel_host', instance.tunnel_host)
                instance.tunnel_port = validated_data.get('tunnel_port', instance.tunnel_port)
            elif (str(instance.tunnel_type) == "1"):    
                instance.parent_tunnel = validated_data.get('parent_tunnel', instance.parent_tunnel_id)
                instance.tunnel_host = None
                instance.tunnel_port = None

  
            instance.tunnel_user = validated_data.get('tunnel_user', instance.tunnel_user)
            instance.tunnel_password = validated_data.get('tunnel_password', instance.tunnel_password)
            instance.pid = validated_data.get('pid', instance.pid)
            instance.save()

            return instance

    class Meta:
        model = Tunnelssh
        fields = ('id','name','host','port','target_host','target_port','tunnel_host','tunnel_port','tunnel_password','parent_tunnel','tunnel_type','tunnel_user','pid','isConnected')


