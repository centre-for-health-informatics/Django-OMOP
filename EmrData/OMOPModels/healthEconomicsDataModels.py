from EmrData.OMOPModels.clinicalDataModels import PERSON
from django.db import models
from EmrData.OMOPModels.vocabularyModels import CONCEPT, DOMAIN
from EmrData.OMOPModels.clinicalDataModels import PERSON
from django.db.models import Q


class PAYER_PLAN_PERIOD(models.Model):
    payer_plan_period_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="payer_plan_period")
    contract_person = models.ForeignKey(PERSON, on_delete=models.DO_NOTHING, related_name="+", null=True)
    payer_plan_period_start_date = models.DateField()
    payer_plan_period_end_date = models.DateField()
    payer_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Payer") & Q(standard_concept='S'), related_name="+")
    payer_source_value = models.CharField(max_length=50, null=True)
    payer_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    plan_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Plan") & Q(standard_concept='S'), related_name="+")
    plan_source_value = models.CharField(max_length=50, null=True)
    plan_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+", null=True)
    contract_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Relationship") & Q(standard_concept='S'), related_name="+")
    contract_source_value = models.CharField(max_length=50)
    contract_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    sponsor_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Sponsor") & Q(standard_concept='S'), related_name="+", null=True)
    sponsor_source_value = models.CharField(max_length=50, null=True)
    sponsor_source_concept = models.ForeignKey(
        CONCEPT, on_delete=models.DO_NOTHING, related_query_name="+", null=True)
    family_source_value = models.CharField(max_length=50, null=True)
    stop_reason_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, limit_choices_to=Q(
        domain__domain_id="Plan Stop Reason") & Q(standard_concept='S'), related_name="+", null=True)
    stop_reason_source_value = models.CharField(max_length=50, null=True)
    stop_reason_source_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+", null=True)

    class Meta:
        db_table = "PAYER_PLAN_PERIOD"


class COST(models.Model):
    cost_id = models.AutoField(primary_key=True)
    cost_event_id = models.BigIntegerField()
    cost_domain = models.ForeignKey(DOMAIN, on_delete=models.DO_NOTHING, related_name="+")
    cost_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    currency_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+", null=True)
    total_charge = models.FloatField(null=True)
    total_cost = models.FloatField(null=True)
    total_paid = models.FloatField(null=True)
    paid_by_payer = models.FloatField(null=True)
    paid_by_patient = models.FloatField(null=True)
    paid_patient_copay = models.FloatField(null=True)
    paid_patient_coinsurance = models.FloatField(null=True)
    paid_patient_deductible = models.FloatField(null=True)
    paid_by_primary = models.FloatField(null=True)
    paid_ingredient_cost = models.FloatField(null=True)
    paid_dispensing_fee = models.FloatField(null=True)
    payer_plan_period_id = models.BigIntegerField(null=True)
    amount_allowed = models.FloatField(null=True)
    revenue_code_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+", null=True)
    revenue_code_source_value = models.CharField(max_length=50, null=True)
    drg_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+", null=True)
    drg_source_value = models.CharField(max_length=3, null=True)

    class Meta:
        db_table = "COST"
