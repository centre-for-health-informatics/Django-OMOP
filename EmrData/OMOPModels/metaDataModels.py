from EmrData.OMOPModels.vocabularyModels import CONCEPT
from django.db import models


class METADATA(models.Model):
    metadata_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    metadata_type_concept = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    name = models.CharField(max_length=250)
    value_as_string = models.CharField(max_length=250, null=True)
    value_as_concept = models.ForeignKey(CONCEPT,  on_delete=models.DO_NOTHING, null=True, related_name="+")
    metadata_date = models.DateField(null=True)
    metadata_datetime = models.DateTimeField(null=True)

    class Meta:
        db_table = "METADATA"


class CDM_SOURCE(models.Model):
    cdm_source_name = models.CharField(max_length=255)
    cdm_source_abbreviation = models.CharField(max_length=25, null=True)
    cdm_holder = models.CharField(max_length=255, null=True)
    source_description = models.TextField(null=True)
    source_documentation_reference = models.CharField(max_length=255, null=True)
    cdm_etl_reference = models.CharField(max_length=255, null=True)
    source_release_date = models.DateField(null=True)
    cdm_release_date = models.DateField(null=True)
    cdm_version = models.CharField(max_length=10, null=True)
    vocabulary_version = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "CDM_SOURCE"
