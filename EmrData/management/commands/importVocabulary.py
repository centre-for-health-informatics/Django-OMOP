from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from EmrData.OMOPModels.vocabularyModels import *
from Utility.resource import checkCsvColumns, getRowCount
from Utility.progress import printProgressBar


class Command(BaseCommand):

    help = 'Import OMOP VOCABULARY.csv.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="File path to VOCABULARY.CSV")

    def handle(self, *args, **kwargs):
        expectedColumns = ['vocabulary_id', 'vocabulary_name',
                           'vocabulary_reference', 'vocabulary_version', 'vocabulary_concept_id']

        filePath = kwargs.get('path')

        print(f"Importing OMOP vocabulary from: {filePath}")

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

                    vocabulary_id, vocabulary_name, vocabulary_reference, vocabulary_version, vocabulary_concept_id = row

                    conceptObj = CONCEPT.objects.get(concept_id=vocabulary_concept_id)

                    defaults = {
                        'vocabulary_id': vocabulary_id,
                        'vocabulary_name': vocabulary_name,
                        'vocabulary_reference': vocabulary_reference,
                        'vocabulary_version': vocabulary_version,
                        'vocabulary_concept_id': conceptObj
                    }

                    _, created = VOCABULARY.objects.update_or_create(
                        vocabulary_id=vocabulary_id, defaults=defaults)

                    if created:
                        createdCounter += 1
                    else:
                        updatedCounter += 1

                    if i % 500 == 0:
                        printProgressBar(i, maxRow, prefix="Importing OMOP VOCABULARY: ",
                                         suffix=f"{'{:,}'.format(i)}/{'{:,}'.format(maxRow)}", decimals=2, length=5)

            print(
                f"Finished importing OMOP vocabulary: {createdCounter} vocabulary created, {updatedCounter} vocabulary updated.")
