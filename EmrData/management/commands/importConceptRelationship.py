from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from EmrData.OMOPModels.vocabularyModels import *
from Utility.resource import checkCsvColumns, getRowCount, genCsvChunks
from Utility.progress import printProgressBar

from multiprocessing import Pool, cpu_count

import pytz
from datetime import datetime


class Command(BaseCommand):

    help = 'Import OMOP CONCEPT_RELATIONSHIP.csv.'

    timeZone = pytz.timezone('UTC')

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="File path to CONCEPT_RELATIONSHIP.CSV")

    def handle(self, *args, **kwargs):
        expectedColumns = ['concept_id_1', 'concept_id_2', 'relationship_id',
                           'valid_start_date', 'valid_end_date', 'invalid_reason']

        filePath = kwargs.get('path')

        print(f"Importing OMOP concept relationships from: {filePath}")

        if not filePath:
            print("File path not specified.")
            return

        maxRows = getRowCount(filePath) - 1
        chunkSize = 5000
        chunks = maxRows // chunkSize + 1

        with open(filePath, 'r') as f:
            csvReader = csv.reader(f, delimiter='\t')

            columns = next(csvReader)
            checkCsvColumns(expectedColumns, columns)

            with transaction.atomic():
                CONCEPT_RELATIONSHIP.objects.all().delete()
                i = 0

                numProcesses = cpu_count()
                pool = Pool(numProcesses)

                for rows in genCsvChunks(csvReader, chunksize=chunkSize):
                    results = pool.apply_async(Command.processRow, args=(rows,))
                    CONCEPT_RELATIONSHIP.objects.bulk_create(results.get())
                    i += 1

                    printProgressBar(i, chunks, prefix="Importing OMOP CONCEPT RELATIONSHIP: ",
                                     suffix=f"{'{:,}'.format(i*chunkSize)}/{'{:,}'.format(maxRows)}", decimals=2, length=5)

                pool.close()
                pool.join()

        print(
            f"Finished importing OMOP concept relationships: {maxRows} concept relationships created.")

    @classmethod
    def processRow(cls, data):
        objs = []
        for row in data:

            concept_id_1, concept_id_2, relationship_id, valid_start_date, valid_end_date, invalid_reason = row

            objs.append(CONCEPT_RELATIONSHIP(concept_id_1_id=concept_id_1, concept_id_2_id=concept_id_2, relationship_id_id=relationship_id,
                                             valid_start_date=Command.timeZone.localize(
                                                 datetime.strptime(valid_start_date, '%Y%m%d')),
                                             valid_end_date=Command.timeZone.localize(datetime.strptime(valid_end_date, '%Y%m%d')), invalid_reason=invalid_reason))
        return objs
