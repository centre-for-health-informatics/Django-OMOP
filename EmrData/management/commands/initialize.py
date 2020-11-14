from django.core.management.base import BaseCommand
from django.core.management import call_command
from datetime import datetime


class Command(BaseCommand):

    help = 'Run commands to initialize OMOP vocabulary databases.'

    def handle(self, *args, **kwargs):

        start = datetime.now()
        # call_command("importConcepts", path="secrets/OMOP_assets/CONCEPT.csv")
        # call_command("importConcepts", path="secrets/OMOP_assets/CONCEPT_CPT4.csv")
        # call_command("importDomains", path="secrets/OMOP_assets/DOMAIN.csv")
        # call_command("importVocabulary", path="secrets/OMOP_assets/VOCABULARY.csv")
        # call_command("importConceptClass", path="secrets/OMOP_assets/CONCEPT_CLASS.csv")
        # call_command("importRelationship", path="secrets/OMOP_assets/RELATIONSHIP.csv")
        call_command("importConceptRelationship", path="secrets/OMOP_assets/CONCEPT_RELATIONSHIP.csv")
        stop = datetime.now()
        print(f"Finished in {stop-start}")
