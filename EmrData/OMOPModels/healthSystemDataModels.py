from EmrData.OMOPModels.vocabularyModels import CONCEPT
from django.db import models
from django.db.models import Q


class LOCATION(models.Model):
    location_id = models.BigIntegerField(primary_key=True)
    address_1 = models.CharField(max_length=50, null=True)
    address_2 = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=2, null=True)
    zip = models.CharField(max_length=9, null=True)
    country = models.CharField(max_length=20, null=True)
    location_source_value = models.CharField(max_length=20, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        db_table = "LOCATION"


class LOCATION_HISTORY(models.Model):
    location_id = models.ForeignKey(LOCATION, on_delete=models.DO_NOTHING, related_name="history")
    relationship_type_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        concept_class__concept_class_id="Location") & Q(standard_concept='S'), related_name="+")
    domain_id = models.CharField(max_length=50)
    entity_id = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    class Meta:
        db_table = "LOCATION_HISTORY"


class CARE_SITE(models.Model):
    care_site_id = models.BigIntegerField(primary_key=True)
    care_site_name = models.CharField(max_length=255, null=True)
    place_of_service_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Visit") & Q(standard_concept='S'), related_name="+")
    location_id = models.ForeignKey(LOCATION, on_delete=models.DO_NOTHING, null=True)
    care_site_source_value = models.CharField(max_length=50, null=True)
    place_of_service_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "CARE_SITE"


class PROVIDER(models.Model):
    provider_id = models.BigIntegerField(primary_key=True)
    provider_name = models.CharField(max_length=255, null=True)
    npi = models.CharField(max_length=20, null=True)
    dea = models.CharField(max_length=20, null=True)
    specialty_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Provider") & Q(standard_concept='S'), related_name="+")
    care_site_id = models.ForeignKey(CARE_SITE, on_delete=models.DO_NOTHING, null=True, related_name='provider')
    year_of_birth = models.IntegerField(null=True)
    gender_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Gender") & Q(standard_concept='S'), related_name="+")
    provider_source_value = models.CharField(max_length=50, null=True)
    specialty_source_value = models.CharField(max_length=50, null=True)
    specialty_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    gender_source_value = models.CharField(max_length=50, null=True)
    gender_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")

    class Meta:
        db_table = "PROVIDER"
