from django.db import models


class CONCEPT(models.Model):
    concept_id = models.BigIntegerField(primary_key=True)
    concept_name = models.CharField(max_length=255)
    standard_concept = models.CharField(max_length=1, null=True)
    concept_code = models.CharField(max_length=50)
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = "CONCEPT"

        indexes = [
            models.Index(fields=['concept_name']),
            models.Index(fields=['standard_concept']),
        ]


class VOCABULARY(models.Model):
    vocabulary_id = models.CharField(max_length=20, primary_key=True)
    vocabulary_name = models.CharField(max_length=255)
    vocabulary_reference = models.CharField(max_length=255)
    vocabulary_version = models.CharField(max_length=255, null=True)
    vocabulary_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name='vocabulary')

    class Meta:
        db_table = "VOCABULARY"


class DOMAIN(models.Model):
    domain_id = models.CharField(max_length=20, primary_key=True)
    domain_name = models.CharField(max_length=255)
    domain_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name='domain')

    class Meta:
        db_table = "DOMAIN"


class CONCEPT_CLASS(models.Model):
    concept_class_id = models.CharField(max_length=20, primary_key=True)
    concept_class_name = models.CharField(max_length=255)
    concept_class_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name='concept_class')

    class Meta:
        db_table = "CONCEPT_CLASS"


class RELATIONSHIP(models.Model):
    relationship_id = models.CharField(max_length=20, primary_key=True)
    relationship_name = models.CharField(max_length=255)
    is_hierarchical = models.CharField(max_length=1)
    defines_ancestry = models.CharField(max_length=1)
    reverse_relationship_id = models.CharField(max_length=20)
    relationship_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "RELATIONSHIP"


class CONCEPT_RELATIONSHIP(models.Model):
    concept_id_1 = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    concept_id_2 = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    relationship_id = models.ForeignKey(RELATIONSHIP, on_delete=models.DO_NOTHING, related_name="+")
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = "CONCEPT_RELATIONSHIP"


class CONCEPT_SYNONYM(models.Model):
    concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    concept_synonym_name = models.CharField(max_length=1000)
    language_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")

    class Meta:
        db_table = "CONCEPT_SYNONYM"


class CONCEPT_ANCESTOR(models.Model):
    ancestor_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    descendant_concept_id = models.ForeignKey(
        CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    min_levels_of_separation = models.IntegerField()
    max_levels_of_separation = models.IntegerField()

    class Meta:
        db_table = "CONCEPT_ANCESTOR"


class SOURCE_TO_CONCEPT_MAP(models.Model):
    source_code = models.CharField(max_length=50)
    source_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    source_vocabulary_id = models.CharField(max_length=20)
    source_code_description = models.CharField(max_length=255, null=True)
    target_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    target_vocabulary_id = models.ForeignKey(VOCABULARY, on_delete=models.DO_NOTHING, related_name="+")
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = "SOURCE_TO_CONCEPT_MAP"


class DRUG_STRENGTH(models.Model):
    drug_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    ingredient_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, related_name="+")
    amount_value = models.FloatField(null=True)
    amount_unit_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    numerator_value = models.FloatField(null=True)
    numerator_unit_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    denominator_value = models.FloatField(null=True)
    denominator_unit_concept_id = models.ForeignKey(CONCEPT, on_delete=models.DO_NOTHING, null=True, related_name="+")
    box_size = models.IntegerField(null=True)
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, null=True)
