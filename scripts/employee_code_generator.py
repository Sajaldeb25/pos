from django.db import connection
import datetime


def generate_employee_code(two_letter):
    two_letter = two_letter.upper()
    cur_date = datetime.datetime.now()
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(RIGHT(code, 4)) FROM core_user WHERE LEFT(code, 2)='%s'" % two_letter)
    row = cursor.fetchone()
    if type(row[0]) == str and row[0] != '':
        row = int(row[0]) + 1
        return str(two_letter) + str(row)
        # return str(two_letter) + str(cur_date.strftime("%d"))\
        #     + str(cur_date.strftime("%m"))\
        #     + str(cur_date.strftime("%y")) + str(row)

    return str(two_letter) + str(1000)
    # return str(two_letter) + str(cur_date.strftime("%d"))\
    #     + str(cur_date.strftime("%m"))\
    #     + str(cur_date.strftime("%y")) + str(1000)
