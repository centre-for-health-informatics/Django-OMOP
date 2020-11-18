from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import RELATIONSHIP


class Command(AbstractImportCommand):
    help = "Import OMOP RELATIONSHIP.csv."

    def printMsg(self):
        print("Importing OMOP Relationships...")

    def expectedCsvColumns(self):
        return ['relationship_id', 'relationship_name', 'is_hierarchical',
                'defines_ancestry', 'reverse_relationship_id', 'relationship_concept_id']

    def deleteAllModelInstances(self):
        RELATIONSHIP.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        RELATIONSHIP.objects.bulk_create(objs)

    @staticmethod
    def makeObjFromRow(row):

        relationship_id, relationship_name, is_hierarchical, defines_ancestry, reverse_relationship_id, relationship_concept_id = row

        return RELATIONSHIP(relationship_id=relationship_id, relationship_name=relationship_name, is_hierarchical=is_hierarchical, defines_ancestry=defines_ancestry, reverse_relationship_id=reverse_relationship_id, relationship_concept_id_id=relationship_concept_id)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data,))
        return results.get()
