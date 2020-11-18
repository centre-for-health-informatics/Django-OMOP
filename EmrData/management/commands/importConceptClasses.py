
from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import CONCEPT_CLASS


class Command(AbstractImportCommand):
    help = "Import OMOP CONCEPT_CLASS.csv."

    def printMsg(self):
        print("Importing OMOP Concept Classes...")

    def expectedCsvColumns(self):
        return ['concept_class_id', 'concept_class_name', 'concept_class_concept_id']

    def deleteAllModelInstances(self):
        CONCEPT_CLASS.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        CONCEPT_CLASS.objects.bulk_create(objs)

    @staticmethod
    def makeObjFromRow(row):

        concept_class_id, concept_class_name, concept_class_concept_id = row
        return CONCEPT_CLASS(concept_class_id=concept_class_id, concept_class_name=concept_class_name, concept_class_concept_id=concept_class_concept_id)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data,))
        return results.get()
