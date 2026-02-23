from rest_framework import serializers
from .models import District, County, Subcounty, Parish, Village

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'name']

class ParishSerializer(serializers.ModelSerializer):
    villages = VillageSerializer(many=True, read_only=True)
    class Meta:
        model = Parish
        fields = ['id', 'name', 'villages']

class SubcountySerializer(serializers.ModelSerializer):
    parishes = ParishSerializer(many=True, read_only=True)
    class Meta:
        model = Subcounty
        fields = ['id', 'name', 'parishes']

class CountySerializer(serializers.ModelSerializer):
    subcounties = SubcountySerializer(many=True, read_only=True)
    class Meta:
        model = County
        fields = ['id', 'name', 'subcounties']

class DistrictSerializer(serializers.ModelSerializer):
    counties = CountySerializer(many=True, read_only=True)
    class Meta:
        model = District
        fields = ['id', 'name', 'counties']
