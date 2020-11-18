from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import CONCEPT_RELATIONSHIP

import pytz
from datetime import datetime


class Command(AbstractImportCommand):
    help = "Import OMOP CONCEPT_RELATIONSHIP.csv."

    def printMsg(self):
        print("Importing OMOP Concept Relationships...")

    def expectedCsvColumns(self):
        return ['concept_id_1', 'concept_id_2', 'relationship_id',
                'valid_start_date', 'valid_end_date', 'invalid_reason']

    def deleteAllModelInstances(self):
        CONCEPT_RELATIONSHIP.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        CONCEPT_RELATIONSHIP.objects.bulk_create(objs)

    @staticmethod
    def makeObjFromRow(row):

        concept_id_1, concept_id_2, relationship_id, valid_start_date, valid_end_date, invalid_reason = row

        return CONCEPT_RELATIONSHIP(concept_id_1_id=concept_id_1, concept_id_2_id=concept_id_2, relationship_id_id=relationship_id,
                                    valid_start_date=pytz.timezone('UTC').localize(
                                        datetime.strptime(valid_start_date, '%Y%m%d')),
                                    valid_end_date=pytz.timezone('UTC').localize(datetime.strptime(valid_end_date, '%Y%m%d')), invalid_reason=invalid_reason)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data, ))
        return results.get()
