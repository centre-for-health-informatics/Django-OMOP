from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from EmrData.OMOPModels.vocabularyModels import *
from Utility.resource import checkCsvColumns, getRowCount
from Utility.progress import printProgressBar


class Command(BaseCommand):

    help = 'Import OMOP DOMAIN.csv.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="File path to DOMAIN.CSV")

    def handle(self, *args, **kwargs):
        expectedColumns = ['domain_id', 'domain_name', 'domain_concept_id']

        filePath = kwargs.get('path')

        print(f"Importing OMOP domains from: {filePath}")

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

                    domain_id, domain_name, domain_concept_id = row

                    conceptObj = CONCEPT.objects.get(concept_id=domain_concept_id)

                    defaults = {
                        'domain_id': domain_id,
                        'domain_name': domain_name,
                        'domain_concept_id': conceptObj,
                    }

                    _, created = DOMAIN.objects.update_or_create(domain_id=domain_id, defaults=defaults)

                    if created:
                        createdCounter += 1
                    else:
                        updatedCounter += 1

                    if i % 500 == 0:
                        printProgressBar(i, maxRow, prefix="Importing OMOP DOMAINS: ",
                                         suffix=f"{'{:,}'.format(i)}/{'{:,}'.format(maxRow)}", decimals=2, length=5)

            print(
                f"Finished importing OMOP domains: {createdCounter} domains created, {updatedCounter} domains updated.")
