# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import PartnerVoucher


class CreateVoucherSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartnerVoucher
        fields = ('code', 'event_id', 'customer_id', 'end_time')


class ShowVoucherSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event_id.name')
    partner_name = serializers.CharField(source='event_id.partner_id.name')
    content = serializers.CharField(source='event_id.content')
    area = serializers.CharField(source='event_id.partner_id.area')

    class Meta:
        model = PartnerVoucher
        fields = ('code', 'event_name', 'partner_name', 'end_time', 'content', 'area', )