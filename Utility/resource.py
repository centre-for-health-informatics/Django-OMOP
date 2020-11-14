def checkCsvColumns(expectedColumns, columns):

    if len(expectedColumns) != len(columns):
        raise ValueError(f"Expected columns: {expectedColumns}, encountered columns: {columns}")

    for i, column in enumerate(columns):
        if column.lower().strip() != expectedColumns[i].lower():
            raise ValueError(f"Expected columns: {expectedColumns}, encountered columns: {columns}")

    return True


def getRowCount(filename):
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    return lines


def genCsvChunks(reader, chunksize=10000):
    '''
    Chunk generator. Take a CSV `reader` and yield
    `chunksize` sized slices. 
    '''

    chunk = []
    for index, line in enumerate(reader):
        if (index % chunksize == 0 and index > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk
