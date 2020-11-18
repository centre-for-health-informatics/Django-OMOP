from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import CONCEPT

import pytz
from datetime import datetime


class Command(AbstractImportCommand):
    help = 'Import OMOP CONCEPT.csv.'

    def printMsg(self):
        print("Importing OMOP Concepts...")

    def expectedCsvColumns(self):
        return ['concept_id', 'concept_name', 'domain_id', 'vocabulary_id', 'concept_class_id',
                'standard_concept', 'concept_code', 'valid_start_date', 'valid_end_date', 'invalid_reason']

    def deleteAllModelInstances(self):
        CONCEPT.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        CONCEPT.objects.bulk_create(objs)

    def bulkUpdateModelInstances(self, objs):
        CONCEPT.objects.bulk_update(objs)

    @staticmethod
    def makeObjFromRow(row):

        concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, standard_concept, concept_code, valid_start_date, valid_end_date, invalid_reason = row

        return CONCEPT(concept_id=concept_id, concept_code=concept_code, domain_id_id=domain_id, vocabulary_id_id=vocabulary_id, concept_class_id_id=concept_class_id,
                       concept_name=concept_name, standard_concept=standard_concept, valid_start_date=pytz.timezone('UTC').localize(
                           datetime.strptime(valid_start_date, '%Y%m%d')),
                       valid_end_date=pytz.timezone('UTC').localize(datetime.strptime(valid_end_date, '%Y%m%d')), invalid_reason=invalid_reason)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data, ))
        return results.get()
