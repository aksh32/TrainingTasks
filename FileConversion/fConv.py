import csv
import json


class ConvertFile():
    def getcsvfile(self, csv_file_path):
        #         with open(csv_file_path) as CsvFile:
        #             clean_data = []
        #             csv_reader = csv.DictReader(CsvFile)
        #             print(csv_reader)
        #             for rows in csv_reader:
        #                 clean_data.append(rows)
        #
        #             print(clean_data)
        clean_data = list()
        count = list()
        csv_final_data = dict()
        with open(csv_file_path, 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            for rows in csv_data:
                print(rows)

            rows = [x.strip() for x in rows]
            rows = [x.replace(' ', '') for x in rows]
            rows = [x.strip("'") for x in rows]
            rows = [x.strip('"') for x in rows]
            rows = [x.replace('o', "0") for x in rows]

            print(rows)

            extra_data = list()

            for row in rows:
                # print(row)
                # clean_data.append(str(row).split('/'))
                clean_data = str(row).split('/')
                if len(clean_data) <= 1:
                    csv_final_data[clean_data[0]] = " "
                else:
                    if clean_data[0] not in csv_final_data:
                        csv_final_data[clean_data[0]] = []

                    for item in clean_data[1:]:
                        csv_final_data[clean_data[0]].append(item)
            return csv_final_data

    def convertFileToJson(self, csvoutput):
        with open('csv_export.json', 'w') as outputFile:
            json.dump(csvoutput, outputFile)


c1 = ConvertFile()
fPath = "test.csv"
output = c1.getcsvfile(fPath)
c1.convertFileToJson(output)
# raw_data = []
# with open("test.csv") as CsvFile:
#     csv_reader = csv.reader(CsvFile)
#     for row in csv_reader:
#         if row:
#             print("Data Fetched Successfully!!!!!!!")
#         else:
#             print("try again!!!!")
# for i in row:
#     raw_data.append(i.strip(" "))
#     raw_data.append(i.strip('"'))
#     print(i)

# with open("test.csv") as csvfile:
#     csv_reader = csv.DictReader(csvfile)
#     for row in csv_reader:
#         print(row)
# clean_data = []
# with open("test.csv") as csvfile:
#     main_data = []
#     for rows in csvfile:
#         print(rows[0:10])
#         for item in rows:
#             clean_data.append(item)
#     print(clean_data)
#
# data = []
# clean_data = []
# csv_file = open("test.csv", 'r')
#
# csv_data = csv.reader(csv_file)
# for rows in csv_data:
#     print(rows)
#
# rows = [x.strip() for x in rows]
# rows = [x.replace(' ','') for x in rows]
# rows = [x.strip("'") for x in rows]
# rows = [x.strip('"') for x in rows]
# rows = [x.replace("/",":") for x in rows]
# rows = [x.replace('o',"0") for x in rows]
#
# for row in rows:
#     print(row)





