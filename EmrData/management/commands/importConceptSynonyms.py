from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import CONCEPT_SYNONYM


class Command(AbstractImportCommand):
    help = "Import OMOP CONCEPT_SYNONYM.csv."

    def printMsg(self):
        print("Importing OMOP Concept Synonyms...")

    def expectedCsvColumns(self):
        return ['concept_id', 'concept_synonym_name', 'language_concept_id']

    def deleteAllModelInstances(self):
        CONCEPT_SYNONYM.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        CONCEPT_SYNONYM.objects.bulk_create(objs)

    @staticmethod
    def makeObjFromRow(row):
        concept_id, concept_synonym_name, language_concept_id = row
        return CONCEPT_SYNONYM(concept_id=concept_id, concept_synonym_name=concept_synonym_name, language_concept_id=language_concept_id)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data,))
        return results.get()
