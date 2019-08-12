from rest_framework import serializers
from core.vodafone.smart.contract.models import Contract
from core.vodafone.smart.user.serializers import UserSerializer

class ContractSerializer(serializers.ModelSerializer):

    contr_originator2user = UserSerializer()
    owner2user = UserSerializer()
    class Meta:

        model = Contract
        depth = 1
        fields = ('objid', 's_id', 'type', 'start_date', 'expire_date', 'pay_options', 'title', 'close_eff_dt', 'last_update', 'ready_to_bill', 'create_dt', 'order_status', 'owner2user', 'contr_originator2user', 'x_estado_excepcion', 'x_fec_venta', 'x_contract2x_clas_orden', 'x_child_contract2contract', 'x_sc_origen')
