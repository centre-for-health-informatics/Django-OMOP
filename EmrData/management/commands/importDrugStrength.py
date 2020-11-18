from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import DRUG_STRENGTH

import pytz
from datetime import datetime


class Command(AbstractImportCommand):
    help = "Import OMOP DRUG_STRENGTH.csv."

    def printMsg(self):
        print("Importing OMOP Drug Strength...")

    def expectedCsvColumns(self):
        return ['drug_concept_id', 'ingredient_concept_id', 'amount_value', 'amount_unit_concept_id', 'numerator_value',
                'numerator_unit_concept_id', 'denominator_value', 'denominator_unit_concept_id', 'box_size', 'valid_start_date',
                'valid_end_date', 'invalid_reason']

    def deleteAllModelInstances(self):
        DRUG_STRENGTH.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        DRUG_STRENGTH.objects.bulk_create(objs)

    @staticmethod
    def makeObjFromRow(row):
        drug_concept_id, ingredient_concept_id, amount_value, amount_unit_concept_id, numerator_value, numerator_unit_concept_id, \
            denominator_value, denominator_unit_concept_id, box_size, valid_start_date, valid_end_date, invalid_reason = row
        try:
            amount_value_fl = float(amount_value)
        except:
            amount_value_fl = None
        try:
            numerator_value_fl = float(numerator_value)
        except:
            numerator_value_fl = None
        try:
            denominator_value_fl = float(denominator_value)
        except:
            denominator_value_fl = None
        try:
            box_size_in = int(box_size)
        except:
            box_size_in = None

        return DRUG_STRENGTH(drug_concept_id_id=drug_concept_id, ingredient_concept_id_id=ingredient_concept_id, amount_value=amount_value_fl,
                             amount_unit_concept_id_id=amount_unit_concept_id, numerator_value=numerator_value_fl, numerator_unit_concept_id_id=numerator_unit_concept_id,
                             denominator_value=denominator_value_fl, denominator_unit_concept_id_id=denominator_unit_concept_id, box_size=box_size_in,
                             valid_start_date=pytz.timezone('UTC').localize(
                                 datetime.strptime(valid_start_date, '%Y%m%d')), valid_end_date=pytz.timezone('UTC').localize(datetime.strptime(valid_end_date, '%Y%m%d')),
                             invalid_reason=invalid_reason)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data,))
        return results.get()
