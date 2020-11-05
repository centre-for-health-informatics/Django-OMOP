from django.db.models.fields import CharField
from EmrData.OMOPModels.healthSystemDataModels import CARE_SITE, LOCATION, PROVIDER
from django.db import models
from django.db.models import Q
from EmrData.OMOPModels.vocabularyModels import CONCEPT


class PERSON(models.Model):
    person_id = models.BigIntegerField(primary_key=True)
    gender_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                          limit_choices_to=Q(domain__domain_id='Gender') & Q(standard_concept='S'), related_name="+")
    year_of_birth = models.IntegerField(null=True)
    month_of_birth = models.IntegerField(null=True)
    day_of_birth = models.IntegerField(null=True)
    birth_datetime = models.DateTimeField(null=True)
    death_datetime = models.DateField(null=True)
    race_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                        limit_choices_to=Q(domain__domain_id='Race') & Q(standard_concept='S'), null=True, related_name="+")
    ethnicity_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                             limit_choices_to=Q(domain__domain_id='Ethnicity') & Q(standard_concept='S'), null=True, related_name="+")
    location_id = models.ForeignKey(LOCATION, on_delete=models.DO_NOTHING, null=True, related_name="person")
    provider_id = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    care_site_id = models.ForeignKey(CARE_SITE, on_delete=models.DO_NOTHING, null=True, related_name="+")
    person_source_value = models.CharField(max_length=50, null=True)
    gender_source_value = models.CharField(max_length=50, null=True)
    gender_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    race_source_value = models.CharField(max_length=50, null=True)
    race_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    ethnicity_source_value = models.CharField(max_length=50, null=True)
    ethnicity_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")

    class Meta:
        db_table = "PERSON"


class OBSERVATION_PERIOD(models.Model):
    observation_period_id = models.BigAutoField(primary_key=True)
    person_id = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="observation_period")
    observation_period_start_date = models.DateField()
    observation_period_end_date = models.DateField()
    period_type_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")

    class Meta:
        db_table = "OBSERVATION_PERIOD"


class VISIT_OCCURRENCE(models.Model):
    visit_occurrence_id = models.BigIntegerField(primary_key=True)
    person_id = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="visit_occurrence")
    visit_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'), related_name="+")
    visit_start_date = models.DateField(null=True)
    visit_start_datetime = models.DateTimeField()
    visit_end_date = models.DateField(null=True)
    visit_end_datetime = models.DateTimeField()
    visit_type_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept'), related_name="+")
    provider_id = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    care_site_id = models.ForeignKey(CARE_SITE, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_source_value = models.CharField(max_length=50, null=True)
    visit_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    admitted_from_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'), related_name="+")
    admitted_from_source_value = models.CharField(max_length=50, null=True)
    discharge_to_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'), related_name="+")
    discharge_to_source_value = models.CharField(max_length=50, null=True)
    preceding_visit_occurrence_id = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, related_name="following_visit_occurence")

    class Meta:
        db_table = "VISIT_OCCURRENCE"


class VISIT_DETAIL(models.Model):
    visit_detail_id = models.BigAutoField(primary_key=True)
    person_id = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="visit_detail")
    visit_detail_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'),  related_name="+")
    visit_detail_start_date = models.DateField()
    visit_detail_start_datetime = models.DateTimeField(null=True)
    visit_detail_end_date = models.DateField()
    visit_detail_end_datetime = models.DateTimeField(null=True)
    visit_detail_type_concept_id = models.ForeignKey(CONCEPT,  on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept'),  related_name="+")
    provider_id = models.ForeignKey(PROVIDER,  on_delete=models.DO_NOTHING, null=True, related_name="+")
    care_site_id = models.ForeignKey(CARE_SITE, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_detail_source_value = models.CharField(max_length=50, null=True)
    visit_detail_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    admitting_source_value = models.CharField(max_length=50, null=True)
    admitting_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,  limit_choices_to=Q(
        domain__domain_id='Visit') & Q(standard_concept='S'), related_name="+")
    discharge_to_source_value = models.CharField(max_length=50, null=True)
    discharge_to_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,  limit_choices_to=Q(
        domain__domain_id='Visit') & Q(standard_concept='S'), related_name="+")
    preceding_visit_detail_id = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, related_name="following_visit_detail")
    visit_detail_parent_id = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, related_name="visit_detail_children")
    visit_occurrence_id = models.ForeignKey(VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, related_name="visit_detail")

    class Meta:
        db_table = "VISIT_DETAIL"


class CONDITION_OCCURRENCE(models.Model):
    condition_occurrence_id = models.BigAutoField(primary_key=True)
    person_id = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="condition_occurrence")
    condition_concept_id = models.ForeignKey(CONCEPT,  on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Condition') & Q(standard_concept='S'),  related_name="+")
    condition_start_date = models.DateField()
    condition_start_datetime = models.DateTimeField(null=True)
    condition_end_date = models.DateField(null=True)
    condition_end_datetime = models.DateTimeField(null=True)
    condition_type_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'),  related_name="+")
    condition_status_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Condition Status') & Q(standard_concept='S'),  related_name="+")
    stop_reason = models.CharField(max_length=20, null=True)
    provider_id = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence_id = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="condition_occurrence")
    visit_detail_id = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                        null=True, related_name="condition_occurrence")
    condition_source_value = models.CharField(max_length=50, null=True)
    condition_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    condition_status_source_value = models.CharField(max_length=50)

    class Meta:
        db_table = "CONDITION_OCCURRENCE"


class DRUG_EXPOSURE(models.Model):
    drug_exposure_id = models.BigIntegerField(primary_key=True)
    person_id = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="drug_exposure")
    drug_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Drug') & Q(standard_concept='S'), related_name="+")
    drug_exposure_start_date = models.DateField()
    drug_exposure_start_datetime = models.DateTimeField(null=True)
    drug_exposure_end_date = models.DateField()
    drug_exposure_end_datetime = models.DateTimeField(null=True)
    verbatim_end_date = models.DateField(null=True)
    drug_type_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'),  related_name="+")
    stop_reason = models.CharField(max_length=20, null=True)
    refills = models.IntegerField(null=True)
    quantity = models.FloatField(null=True)
    days_supply = models.IntegerChoices(null=True)
    sig = models.TextField(null=True)
    route_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Route"), null=True, related_name="+")
    lot_number = CharField(max_length=50, null=True)
    provider_id = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence_id = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="drug_exposure")
    visit_detail_id = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                        null=True, related_name="drug_exposure")
    drug_source_value = models.CharField(max_length=50, null=True)
    drug_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    route_source_value = models.CharField(max_length=50, null=True)
    dose_unit_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "DRUG_EXPOSURE"


class PROCEDURE_OCCURRENCE(models.Model):
    procedure_occurrence_id = models.BigIntegerField(primary_key=True)
    person_id = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="PROCEDURE_OCCURRENCE")
    procedure_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Procedure') & Q(standard_concept='S'), related_name="+")
    procedure_date = models.DateField(null=True)
    procedure_datetime = models.DateTimeField()
    procedure_type_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'), related_name="+")
    modifier_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=(Q(concept_class__concept_class_id='CPT4 Modifier') | Q(
        concept_class__concept_class_id='HCPCS Modifier')) & (Q(vocabulary__vocabulary_id='CPT4') | Q(vocabulary__vocabulary_id='HCPCS')) & Q(standard_concept='S'), related_name="+")
    quantity = models.IntegerField(null=True)
    provider_id = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence_id = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="procedure_occurrence")
    visit_detail_id = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                        null=True, related_name="procedure_occurrence")
    procedure_source_value = models.CharField(max_length=50, null=True)
    procedure_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    modifier_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "PROCEDURE_OCCURRENCE"


class DEVICE_EXPOSURE(models.Model):
    device_exposure_id = models.BigIntegerField(primary_key=True)
    person_id = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="device_exposure")
    device_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Device'), related_name="+")
    device_exposure_start_date = models.DateField()
    device_exposure_start_datetime = models.DateTimeField(null=True)
    device_exposure_end_date = models.DateField()
    device_exposure_end_datetime = models.DateTimeField(null=True)
    device_type_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'), related_name="+")
    unique_device_id = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(null=True)
    provider_id = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence_id = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="device_exposure")
    visit_detail_id = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                        null=True, related_name="device_exposure")
    device_source_value = models.CharField(max_length=50, null=True)
    device_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")

    class Meta:
        db_table = "DEVICE_EXPOSURE"
