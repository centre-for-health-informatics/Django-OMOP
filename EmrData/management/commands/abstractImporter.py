from abc import abstractmethod
from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from Utility.resource import checkCsvColumns, getRowCount, genCsvChunks
from Utility.progress import printProgressBar

from multiprocessing import Pool, cpu_count


class AbstractImportCommand(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="File path to CSV")
        parser.add_argument('-a', '--append', action='store_true',
                            help='Keep current records, and import data from file as new records.')
        parser.add_argument('--chuckSize', type=int, help='Number of rows to process in each chunk.')

    def printMsg(self):
        print("")

    @abstractmethod
    def expectedCsvColumns(self):
        '''Returns a list expected column headers as strings.'''
        return NotImplemented

    @abstractmethod
    def deleteAllModelInstances(self):
        '''Delete all model instances, ie: MODEL.objects.all().delete()'''
        raise NotImplementedError

    @abstractmethod
    def bulkCreateModelInstances(self, objs):
        '''Bulk create models instances, ie: MODEL.objects.bulk_create(objs)'''
        raise NotImplementedError

    @abstractmethod
    def asyncProcessData(self, pool, data):
        '''Process data using provided multiprocessing pool, return results.'''
        return NotImplemented

    def handle(self, *args, **kwargs):

        expectedColumns = self.expectedCsvColumns()
        filePath = kwargs.get('path')
        append = kwargs.get('append')
        chunkSize = kwargs.get('chunkSize') or 10000

        self.printMsg()
        print(f"Reading: {filePath}")

        if not filePath:
            print("File path not specified.")
            return

        maxRows = getRowCount(filePath) - 1
        chunks = maxRows // chunkSize + 1

        with open(filePath, 'r') as f:
            csvReader = csv.reader(f, delimiter='\t')

            columns = next(csvReader)
            checkCsvColumns(expectedColumns, columns)
            numProcesses = cpu_count()
            pool = Pool(numProcesses)

            with transaction.atomic():

                if not append:
                    self.deleteAllModelInstances()

                dataChunks = genCsvChunks(csvReader, chunksize=chunkSize)

                for i, rows in enumerate(dataChunks):
                    objs = self.asyncProcessData(pool, rows)
                    self.bulkCreateModelInstances(objs)

                    printProgressBar(i+1, chunks, prefix="Importing",
                                     suffix=f"{'{:,}'.format(min((i+1)*chunkSize, maxRows))}/{'{:,}'.format(maxRows)}", decimals=2, length=5)

            pool.close()
            pool.join()
