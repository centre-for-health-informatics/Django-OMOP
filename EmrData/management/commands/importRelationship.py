from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from EmrData.OMOPModels.vocabularyModels import *
from Utility.resource import checkCsvColumns, getRowCount
from Utility.progress import printProgressBar


class Command(BaseCommand):

    help = 'Import OMOP RELATIONSHIP.csv.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="File path to RELATIONSHIP.CSV")

    def handle(self, *args, **kwargs):
        expectedColumns = ['relationship_id', 'relationship_name', 'is_hierarchical',
                           'defines_ancestry', 'reverse_relationship_id', 'relationship_concept_id']

        filePath = kwargs.get('path')

        print(f"Importing OMOP relationships from: {filePath}")

        if not filePath:
            print("File path not specified.")
            return

        maxRow = getRowCount(filePath) - 1

        with open(filePath, 'r') as f:
            csvReader = csv.reader(f, delimiter='\t')

            columns = next(csvReader)
            checkCsvColumns(expectedColumns, columns)

            createdCounter = 0
            updatedCounter = 0

            with transaction.atomic():

                for i, row in enumerate(csvReader):
                    row = [item.strip() for item in row]

                    relationship_id, relationship_name, is_hierarchical, defines_ancestry, reverse_relationship_id, relationship_concept_id = row

                    conceptObj = CONCEPT.objects.get(concept_id=relationship_concept_id)

                    defaults = {
                        'relationship_id': relationship_id,
                        'relationship_name': relationship_name,
                        'is_hierarchical': is_hierarchical,
                        'defines_ancestry': defines_ancestry,
                        'reverse_relationship_id': reverse_relationship_id,
                        'relationship_concept_id': conceptObj
                    }

                    _, created = RELATIONSHIP.objects.update_or_create(
                        relationship_id=relationship_id, defaults=defaults)

                    if created:
                        createdCounter += 1
                    else:
                        updatedCounter += 1

                    if i % 500 == 0:
                        printProgressBar(i, maxRow, prefix="Importing OMOP RELATIONSHIP: ",
                                         suffix=f"{'{:,}'.format(i)}/{'{:,}'.format(maxRow)}", decimals=2, length=5)

            print(
                f"Finished importing OMOP relationships: {createdCounter} relationships created, {updatedCounter} relationships updated.")
