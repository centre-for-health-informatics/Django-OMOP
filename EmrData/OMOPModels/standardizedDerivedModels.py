from django.db.models.fields import AutoField, BigAutoField
from EmrData.OMOPModels.vocabularyModels import CONCEPT
from django.db import models
from django.db.models import Q
from EmrData.OMOPModels.clinicalDataModels import PERSON


class DRUG_ERA(models.Model):
    drug_era_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="drug_era")
    drug_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                     limit_choices_to=Q(domain__domain_id='Drug'), related_name="+")
    drug_era_start_date = models.DateTimeField()
    drug_era_end_date = models.DateTimeField()
    drug_exposure_count = models.IntegerField(null=True)
    gap_days = models.IntegerField(null=True)

    class Meta:
        db_table = "DRUG_ERA"


class DOSE_ERA(models.Model):
    dose_era_id = BigAutoField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="dose_era")
    drug_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                     limit_choices_to=Q(domain__domain_id='Drug'), related_name="+")
    unit_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                     limit_choices_to=Q(domain__domain_id='Unit'), related_name="+")
    dose_value = models.FloatField()
    dose_era_start_date = models.DateTimeField()
    dose_era_end_date = models.DateTimeField()

    class Meta:
        db_table = "DOSE_ERA"


class CONDITION_ERA(models.Model):
    condition_era_id = AutoField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="condition_era")
    condition_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                          limit_choices_to=Q(domain__domain_id='Condition'), related_name="+")
    condition_era_start_date = models.DateTimeField()
    condition_era_end_date = models.DateTimeField()
    condition_occurrence_count = models.IntegerField(null=True)

    class Meta:
        db_table = "CONDITION_ERA"
