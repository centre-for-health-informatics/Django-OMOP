from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import CONCEPT_ANCESTOR


class Command(AbstractImportCommand):
    help = 'Import OMOP CONCEPT_ANCESTOR.csv.'

    def printMsg(self):
        print("Importing OMOP Concept Ancestors...")

    def expectedCsvColumns(self):
        return ['ancestor_concept_id', 'descendant_concept_id', 'min_levels_of_separation', 'max_levels_of_separation']

    def deleteAllModelInstances(self):
        CONCEPT_ANCESTOR.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        CONCEPT_ANCESTOR.objects.bulk_create(objs)

    def bulkUpdateModelInstances(self, objs):
        CONCEPT_ANCESTOR.objects.bulk_update(objs)

    @staticmethod
    def makeObjFromRow(row):
        ancestor_concept_id, descendant_concept_id, min_levels_of_separation, max_levels_of_separation = row
        return CONCEPT_ANCESTOR(ancestor_concept_id_id=ancestor_concept_id, descendant_concept_id_id=descendant_concept_id,
                                min_levels_of_separation=min_levels_of_separation, max_levels_of_separation=max_levels_of_separation)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data, ))
        return results.get()
