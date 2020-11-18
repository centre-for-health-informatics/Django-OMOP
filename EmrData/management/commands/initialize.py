from django.core.management.base import BaseCommand
from django.core.management import call_command
from datetime import datetime


class Command(BaseCommand):

    help = 'Run commands to initialize OMOP vocabulary data tables.'

    def handle(self, *args, **kwargs):

        start = datetime.now()
        call_command("importDomains", path="secrets/OMOP_assets/DOMAIN.csv")
        call_command("importVocabulary", path="secrets/OMOP_assets/VOCABULARY.csv")
        call_command("importConceptClasses", path="secrets/OMOP_assets/CONCEPT_CLASS.csv")
        call_command("importConcepts", path="secrets/OMOP_assets/CONCEPT_CPT4.csv")
        call_command("importConcepts", path="secrets/OMOP_assets/CONCEPT.csv", append=True)
        call_command("importRelationships", path="secrets/OMOP_assets/RELATIONSHIP.csv")
        call_command("importConceptRelationships", path="secrets/OMOP_assets/CONCEPT_RELATIONSHIP.csv")
        call_command("importConceptSynonyms", path="secrets/OMOP_assets/CONCEPT_SYNONYM.csv")
        call_command("importConceptAncestors", path="secrets/OMOP_assets/CONCEPT_ANCESTOR.csv")
        call_command("importDrugStrength", path="secrets/OMOP_assets/DRUG_STRENGTH.csv")
        stop = datetime.now()
        print(f"Finished in {stop-start}")
