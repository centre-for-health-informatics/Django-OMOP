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
