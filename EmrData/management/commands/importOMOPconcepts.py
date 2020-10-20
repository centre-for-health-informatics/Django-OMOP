from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from EmrData.vocabularyModels import *

import pytz
from datetime import datetime, date


class Command(BaseCommand):

    help = 'Import OMOP CONCEPT.csv.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="File path to CONCEPT.CSV")

    def handle(self, *args, **kwargs):

        filePath = kwargs.get('path')
        timeZone = pytz.timezone('UTC')

        if not filePath:
            print("File path not specified.")
            return

        with open(filePath, 'r') as f:
            csvReader = csv.reader(f, delimiter='\t')
            next(csvReader)

            createdCounter = 0
            updatedCounter = 0

            with transaction.atomic():

                for i, row in enumerate(csvReader):
                    row = [item.strip() for item in row]

                    concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, standard_concept, concept_code, valid_start_date, valid_end_date, invalid_reason = row

                    defaults = {
                        'concept_id': concept_id,
                        'concept_code': concept_code,
                        'concept_name': concept_name,
                        'concept_class_id': concept_class_id,
                        'standard_concept': standard_concept,
                        'valid_start_date': timeZone.localize(datetime.strptime(valid_start_date, '%Y%m%d')),
                        'valid_end_date': timeZone.localize(datetime.strptime(valid_end_date, '%Y%m%d')),
                        'invalid_reason': invalid_reason,
                        'domain_id': domain_id,
                        'vocabulary_id': vocabulary_id
                    }

                    obj, created = CONCEPT.objects.update_or_create(concept_id=concept_id, defaults=defaults)

                    if created:
                        createdCounter += 1
                    else:
                        updatedCounter += 1

                    if i % 500 == 0:
                        print(f"Created {createdCounter}, updated {updatedCounter} OMOP concepts.", end="\r")
