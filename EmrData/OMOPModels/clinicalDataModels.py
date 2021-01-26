from EmrData.OMOPModels.healthSystemDataModels import CARE_SITE, LOCATION, PROVIDER
from django.db import models
from django.db.models import Q
from EmrData.OMOPModels.vocabularyModels import CONCEPT


class PERSON(models.Model):
    person_id = models.BigIntegerField(primary_key=True)
    gender_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                       limit_choices_to=Q(domain__domain_id='Gender') & Q(standard_concept='S'), related_name="+")
    year_of_birth = models.IntegerField(null=True)
    month_of_birth = models.IntegerField(null=True)
    day_of_birth = models.IntegerField(null=True)
    birth_datetime = models.DateTimeField(null=True)
    death_datetime = models.DateField(null=True)
    race_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                     limit_choices_to=Q(domain__domain_id='Race') & Q(standard_concept='S'), null=True, related_name="+")
    ethnicity_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                          limit_choices_to=Q(domain__domain_id='Ethnicity') & Q(standard_concept='S'), null=True, related_name="+")
    location = models.ForeignKey(LOCATION, on_delete=models.DO_NOTHING, null=True, related_name="person")
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    care_site = models.ForeignKey(CARE_SITE, on_delete=models.DO_NOTHING, null=True, related_name="+")
    person_source_value = models.CharField(max_length=50, null=True)
    gender_source_value = models.CharField(max_length=50, null=True)
    gender_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    race_source_value = models.CharField(max_length=50, null=True)
    race_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    ethnicity_source_value = models.CharField(max_length=50, null=True)
    ethnicity_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")

    class Meta:
        db_table = "PERSON"


class OBSERVATION_PERIOD(models.Model):
    observation_period_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="observation_period")
    observation_period_start_date = models.DateField()
    observation_period_end_date = models.DateField()
    period_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")

    class Meta:
        db_table = "OBSERVATION_PERIOD"


class VISIT_OCCURRENCE(models.Model):
    visit_occurrence_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="visit_occurrence")
    visit_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'), related_name="+")
    visit_start_date = models.DateField(null=True)
    visit_start_datetime = models.DateTimeField()
    visit_end_date = models.DateField(null=True)
    visit_end_datetime = models.DateTimeField()
    visit_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept'), related_name="+")
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    care_site = models.ForeignKey(CARE_SITE, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_source_value = models.CharField(max_length=50, null=True)
    visit_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    admitted_from_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'), related_name="+")
    admitted_from_source_value = models.CharField(max_length=50, null=True)
    discharge_to_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'), related_name="+")
    discharge_to_source_value = models.CharField(max_length=50, null=True)
    preceding_visit_occurrence = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, related_name="following_visit_occurence")

    class Meta:
        db_table = "VISIT_OCCURRENCE"


class VISIT_DETAIL(models.Model):
    visit_detail_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="visit_detail")
    visit_detail_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Visit'),  related_name="+")
    visit_detail_start_date = models.DateField()
    visit_detail_start_datetime = models.DateTimeField(null=True)
    visit_detail_end_date = models.DateField()
    visit_detail_end_datetime = models.DateTimeField(null=True)
    visit_detail_type_concept = models.ForeignKey(CONCEPT,  on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept'),  related_name="+")
    provider = models.ForeignKey(PROVIDER,  on_delete=models.DO_NOTHING, null=True, related_name="+")
    care_site = models.ForeignKey(CARE_SITE, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_detail_source_value = models.CharField(max_length=50, null=True)
    visit_detail_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    admitting_source_value = models.CharField(max_length=50, null=True)
    admitting_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,  limit_choices_to=Q(
        domain__domain_id='Visit') & Q(standard_concept='S'), related_name="+")
    discharge_to_source_value = models.CharField(max_length=50, null=True)
    discharge_to_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,  limit_choices_to=Q(
        domain__domain_id='Visit') & Q(standard_concept='S'), related_name="+")
    preceding_visit_detail = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, related_name="following_visit_detail")
    visit_detail_parent = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, related_name="visit_detail_children")
    visit_occurrence = models.ForeignKey(VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, related_name="visit_detail")

    class Meta:
        db_table = "VISIT_DETAIL"


class CONDITION_OCCURRENCE(models.Model):
    condition_occurrence_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="condition_occurrence")
    condition_concept = models.ForeignKey(CONCEPT,  on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Condition') & Q(standard_concept='S'),  related_name="+")
    condition_start_date = models.DateField()
    condition_start_datetime = models.DateTimeField(null=True)
    condition_end_date = models.DateField(null=True)
    condition_end_datetime = models.DateTimeField(null=True)
    condition_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'),  related_name="+")
    condition_status_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Condition Status') & Q(standard_concept='S'),  related_name="+")
    stop_reason = models.CharField(max_length=20, null=True)
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="condition_occurrence")
    visit_detail = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                     null=True, related_name="condition_occurrence")
    condition_source_value = models.CharField(max_length=50, null=True)
    condition_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    condition_status_source_value = models.CharField(max_length=50)

    class Meta:
        db_table = "CONDITION_OCCURRENCE"


class DRUG_EXPOSURE(models.Model):
    drug_exposure_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="drug_exposure")
    drug_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Drug') & Q(standard_concept='S'), related_name="+")
    drug_exposure_start_date = models.DateField()
    drug_exposure_start_datetime = models.DateTimeField(null=True)
    drug_exposure_end_date = models.DateField()
    drug_exposure_end_datetime = models.DateTimeField(null=True)
    verbatim_end_date = models.DateField(null=True)
    drug_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'),  related_name="+")
    stop_reason = models.CharField(max_length=20, null=True)
    refills = models.IntegerField(null=True)
    quantity = models.FloatField(null=True)
    days_supply = models.IntegerField(null=True)
    sig = models.TextField(null=True)
    route_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Route"), null=True, related_name="+")
    lot_number = models.CharField(max_length=50, null=True)
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="drug_exposure")
    visit_detail = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                     null=True, related_name="drug_exposure")
    drug_source_value = models.CharField(max_length=50, null=True)
    drug_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    route_source_value = models.CharField(max_length=50, null=True)
    dose_unit_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "DRUG_EXPOSURE"


class PROCEDURE_OCCURRENCE(models.Model):
    procedure_occurrence_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="PROCEDURE_OCCURRENCE")
    procedure_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Procedure') & Q(standard_concept='S'), related_name="+")
    procedure_date = models.DateField(null=True)
    procedure_datetime = models.DateTimeField()
    procedure_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'), related_name="+")
    modifier_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=(Q(concept_class__concept_class_id='CPT4 Modifier') | Q(
        concept_class__concept_class_id='HCPCS Modifier')) & (Q(vocabulary__vocabulary_id='CPT4') | Q(vocabulary__vocabulary_id='HCPCS')) & Q(standard_concept='S'), related_name="+")
    quantity = models.IntegerField(null=True)
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="procedure_occurrence")
    visit_detail = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                     null=True, related_name="procedure_occurrence")
    procedure_source_value = models.CharField(max_length=50, null=True)
    procedure_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    modifier_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "PROCEDURE_OCCURRENCE"


class DEVICE_EXPOSURE(models.Model):
    device_exposure_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="device_exposure")
    device_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Device'), related_name="+")
    device_exposure_start_date = models.DateField()
    device_exposure_start_datetime = models.DateTimeField(null=True)
    device_exposure_end_date = models.DateField()
    device_exposure_end_datetime = models.DateTimeField(null=True)
    device_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'), related_name="+")
    unique_device_id = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(null=True)
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="device_exposure")
    visit_detail = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                     null=True, related_name="device_exposure")
    device_source_value = models.CharField(max_length=50, null=True)
    device_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")

    class Meta:
        db_table = "DEVICE_EXPOSURE"


class MEASUREMENT(models.Model):
    measurement_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="measurement")
    measurement_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Measurement') & Q(standard_concept='S'), related_name="+")
    measurement_date = models.DateField()
    measurement_datetime = models.DateTimeField(null=True)
    measurement_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'), related_name="+")
    operator_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Meas Value Operator') & Q(standard_concept='S'), null=True, related_name="+")
    value_as_number = models.FloatField(null=True)
    value_as_concept = models.ForeignKey(CONCEPT,  on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Meas Value') & Q(standard_concept='S'), null=True, related_name="+")
    unit_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Unit'), null=True, related_name="+")
    range_low = models.FloatField(null=True)
    range_high = models.FloatField(null=True)
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="measurement")
    visit_detail = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                     null=True, related_name="measurement")
    measurement_source_value = models.CharField(max_length=50, null=True)
    measurement_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    unit_source_value = models.CharField(max_length=50, null=True)
    value_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "MEASUREMENT"


class OBSERVATION(models.Model):
    observation_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="observation")
    observation_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    observation_date = models.DateField(null=True)
    observation_datetime = models.DateTimeField()
    observation_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'), related_name="+")
    value_as_number = models.FloatField(null=True)
    value_as_string = models.CharField(max_length=60, null=True)
    value_as_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    qualifier_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    unit_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True,
                                     limit_choices_to=Q(domain__domain_id='Unit'), related_name="+")
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="observation")
    visit_detail = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING,
                                     null=True, related_name="observation")
    observation_source_value = models.CharField(max_length=50, null=True)
    observation_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    unit_source_value = models.CharField(max_length=50, null=True)
    qualifier_source_value = models.CharField(max_length=50, null=True)
    observation_event_id = models.BigIntegerField(null=True)
    obs_event_field_concept = models.ForeignKey(CONCEPT,  on_delete=models.DO_NOTHING, null=True, related_name="+")
    value_as_datetime = models.DateTimeField(null=True)

    class Meta:
        db_table = "OBSERVATION"


class NOTE(models.Model):
    note_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="note")
    note_date = models.DateField()
    note_datetime = models.DateTimeField(null=True)
    note_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Type Concept') & Q(standard_concept='S'), related_name="+")
    note_class_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=(Q(concept_class__concept_class_id='Doc Kind') | Q(concept_class__concept_class_id='Doc Role') | Q(
        concept_class__concept_class_id='Doc Setting') | Q(concept_class__concept_class_id='Doc Subject Matter') | Q(concept_class__concept_class_id='Doc Type of Service')) & Q(domain__domain_id='Meas Value') & Q(standard_concept='S'), related_name="+")
    note_title = models.CharField(max_length=250, null=True)
    note_text = models.TextField()
    encoding_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    language_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="note")
    visit_detail = models.ForeignKey(VISIT_DETAIL, on_delete=models.DO_NOTHING, null=True, related_name="note")
    note_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "NOTE"


class NOTE_NLP(models.Model):
    note_nlp_id = models.BigIntegerField(primary_key=True)
    note = models.ForeignKey(NOTE, on_delete=models.DO_NOTHING, related_name="note_nlp")
    section_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    snippet = models.CharField(max_length=250, null=True)
    offset = models.CharField(max_length=50, null=True)
    lexical_variant = models.CharField(max_length=250)
    note_nlp_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    note_nlp_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    nlp_system = models.CharField(max_length=250, null=True)
    nlp_date = models.DateField()
    nlp_datetime = models.DateTimeField(null=True)
    term_exists = models.BooleanField(null=True)
    term_temporal = models.CharField(max_length=50)
    term_modifiers = models.CharField(max_length=2000, null=True)

    class Meta:
        db_table = "NOTE_NLP"


class SPECIMEN(models.Model):
    specimen_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="+")
    specimen_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id='Specimen') & Q(standard_concept='S'), related_name="+")
    specimen_date = models.DateField()
    specimen_datetime = models.DateTimeField(null=True)
    quantity = models.FloatField(null=True)
    unit_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True,
                                     limit_choices_to=Q(domain__domain_id='Unit') & Q(standard_concept='S'), related_name="+")
    anatomic_site_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, limit_choices_to=Q(
        domain__domain_id='Spec Anatomic Site') & Q(concept_class__concept_class_id='Body Structure') & Q(standard_concept='S'), related_name="+")
    disease_status_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    specimen_source_id = models.CharField(max_length=50, null=True)
    specimen_source_value = models.CharField(max_length=50, null=True)
    unit_source_value = models.CharField(max_length=50, null=True)
    anatomic_site_source_value = models.CharField(max_length=50, null=True)
    disease_status_source_value = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "SPECIMEN"


class FACT_RELATIONSHIP(models.Model):
    domain_concept_id_1 = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    fact_id_1 = models.BigIntegerField()
    domain_concept_id_2 = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    fact_id_2 = models.BigIntegerField()
    relationship_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")

    class Meta:
        db_table = "FACT_RELATIONSHIP"


class SURVEY_CONDUCT(models.Model):
    survey_conduct_id = models.BigIntegerField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="survey_conduct")
    survey_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, limit_choices_to=Q(
        concept_class__concept_class_id='Staging / Scales') & Q(standard_concept='S'), related_name="+")
    survey_start_date = models.DateField(null=True)
    survey_start_datetime = models.DateTimeField(null=True)
    survey_end_date = models.DateField(null=True)
    survey_end_datetime = models.DateTimeField()
    provider = models.ForeignKey(PROVIDER, on_delete=models.DO_NOTHING, null=True, related_name="+")
    assisted_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    respondent_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    timing_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    collection_method_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    assisted_source_value = models.CharField(max_length=50, null=True)
    respondent_type_source_value = models.CharField(max_length=100, null=True)
    timing_source_value = models.CharField(max_length=100, null=True)
    collection_method_source_value = models.CharField(max_length=100, null=True)
    survey_source_value = models.CharField(max_length=100, null=True)
    survey_source_concept = models.ForeignKey(CONCEPT, null=True, on_delete=models.DO_NOTHING, related_name="+")
    survey_source_identifier = models.CharField(max_length=100, null=True)
    validated_survey_concept = models.ForeignKey(CONCEPT, null=True, on_delete=models.DO_NOTHING, related_name="+")
    validated_survey_source_value = models.IntegerField(null=True)
    survey_version_number = models.CharField(max_length=20, null=True)
    visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="survey_conduct")
    response_visit_occurrence = models.ForeignKey(
        VISIT_OCCURRENCE, on_delete=models.DO_NOTHING, null=True, related_name="+")

    class Meta:
        db_table = "SURVEY_CONDUCT"
