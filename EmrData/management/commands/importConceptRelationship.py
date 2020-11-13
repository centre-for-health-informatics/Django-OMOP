from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from EmrData.OMOPModels.vocabularyModels import *
from Utility.resource import checkCsvColumns, getRowCount
from Utility.progress import printProgressBar

import pytz
from datetime import datetime


class Command(BaseCommand):

    help = 'Import OMOP CONCEPT_RELATIONSHIP.csv.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="File path to CONCEPT_RELATIONSHIP.CSV")

    def handle(self, *args, **kwargs):
        expectedColumns = ['concept_id_1', 'concept_id_2', 'relationship_id',
                           'valid_start_date', 'valid_end_date', 'invalid_reason']

        filePath = kwargs.get('path')
        timeZone = pytz.timezone('UTC')

        print(f"Importing OMOP concept relationships from: {filePath}")

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

                    concept_id_1, concept_id_2, relationship_id, valid_start_date, valid_end_date, invalid_reason = row

                    try:
                        concept1 = CONCEPT.objects.get(concept_id=concept_id_1)
                        concept2 = CONCEPT.objects.get(concept_id=concept_id_2)
                        relation = RELATIONSHIP.objects.get(relationship_id=relationship_id)
                    except:
                        print(
                            f"Not found: concept1={concept_id_1}, concept2={concept_id_2}, relation={relationship_id}")
                        return

                    defaults = {
                        'concept_id_1': concept1,
                        'concept_id_2': concept2,
                        'relationship_id': relation,
                        'valid_start_date': timeZone.localize(datetime.strptime(valid_start_date, '%Y%m%d')),
                        'valid_end_date': timeZone.localize(datetime.strptime(valid_end_date, '%Y%m%d')),
                        'invalid_reason': invalid_reason,
                    }

                    _, created = CONCEPT_RELATIONSHIP.objects.update_or_create(
                        concept_id_1=concept1, concept_id_2=concept2, relationship_id=relation, defaults=defaults)

                    if created:
                        createdCounter += 1
                    else:
                        updatedCounter += 1

                    if i % 500 == 0:
                        printProgressBar(i, maxRow, prefix="Importing OMOP CONCEPT RELATIONSHIP: ",
                                         suffix=f"{'{:,}'.format(i)}/{'{:,}'.format(maxRow)}", decimals=2, length=5)

            print(
                f"Finished importing OMOP concept relationships: {createdCounter} concept relationships created, {updatedCounter} concept relationships updated.")
