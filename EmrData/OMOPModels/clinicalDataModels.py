from django.db import models
from django.db.models import Q
from EmrData.OMOPModels.vocabularyModels import CONCEPT


class PERSON(models.Model):
    person_id = models.BigIntegerField(primary_key=True)
    gender_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                          limit_choices_to=Q(domain__domain_id__icontains='Gender') & Q(standard_concept='S'), related_name="+")
    year_of_birth = models.IntegerField(null=True)
    month_of_birth = models.IntegerField(null=True)
    day_of_birth = models.IntegerField(null=True)
    birth_datetime = models.DateTimeField(null=True)
    death_datetime = models.DateField(null=True)
    race_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                        limit_choices_to=Q(domain__domain_id__icontains='Race') & Q(standard_concept='S'), null=True, related_name="+")
    ethnicity_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING,
                                             limit_choices_to=Q(domain__domain_id__icontains='Ethnicity') & Q(standard_concept='S'), null=True, related_name="+")
    # location_id TODO
    # provider_id TODO
    # care_site_id TODO
    person_source_value = models.CharField(max_length=50, null=True)
    gender_source_value = models.CharField(max_length=50, null=True)
    gender_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    race_source_value = models.CharField(max_length=50, null=True)
    race_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    ethnicity_source_value = models.CharField(max_length=50, null=True)
    ethnicity_source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")

    class Meta:
        db_table = "PERSON"
