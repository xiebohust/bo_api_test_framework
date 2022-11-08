import os.path

import xlrd
import config


class ExcelHandle:

    def __init__(self,file_path):
        self.wb = xlrd.open_workbook(file_path)
        self.table = self.wb.sheet_by_index(0)
        self.nrow = self.table.nrows
        self.ncol = self.table.ncols
        self.data = self.get_data()

    def get_data(self):
        result = []
        # 第一行是表头
        first_row = self.table.row_values(0)

        for row_id in range(1, self.nrow):
            row_data = self.table.row_values(row_id)
            row_dict = dict(zip(first_row,row_data))

            for k, v in row_dict.items():
                if v == '':
                    row_dict[k] = None
            result.append(row_dict)
        return result

    def get_cell_value(self,row,col):
        return self.table.cell_value(row,col)

if __name__ == '__main__':
    r = ExcelHandle(config.casefile_path)
    r = r.get_data()[4]['data']
    # re = r.get_cell_value(4, 4)
    # r = eval(r.get_data()[0])
    print(eval(r))