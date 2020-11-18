from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import VOCABULARY


class Command(AbstractImportCommand):
    help = "Import OMOP VOCABULARY.csv."

    def printMsg(self):
        print("Importing OMOP Vocabulary...")

    def expectedCsvColumns(self):
        return ['vocabulary_id', 'vocabulary_name',
                'vocabulary_reference', 'vocabulary_version', 'vocabulary_concept_id']

    def deleteAllModelInstances(self):
        VOCABULARY.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        VOCABULARY.objects.bulk_create(objs)

    @staticmethod
    def makeObjFromRow(row):

        vocabulary_id, vocabulary_name, vocabulary_reference, vocabulary_version, vocabulary_concept_id = row

        return VOCABULARY(vocabulary_id=vocabulary_id, vocabulary_name=vocabulary_name, vocabulary_reference=vocabulary_reference, vocabulary_version=vocabulary_version, vocabulary_concept_id=vocabulary_concept_id)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data,))
        return results.get()
