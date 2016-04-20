# -*- coding: utf-8 -*-
from django.http import HttpResponse

from campaigns.models import *

import csv

def get_populated_student_specialties(campaign, system_programing_count, computer_networks_count, start_position):
    student_set = campaign.student_set.all()
    output_set = dict()
    start_position = int(start_position)
    end_position = start_position + int(system_programing_count) + int(computer_networks_count)

    requested_students = sorted(
        student_set,
        key = lambda student: student.grades_evaluated,
        reverse = True
    )[start_position-1:end_position-1]

    sp_counter = int(system_programing_count)
    cn_counter = int(computer_networks_count)
    student_counter = 0

    while(len(requested_students) > student_counter):
        current_student = requested_students[student_counter]

        if current_student.first_choice == 'СП' and sp_counter > 0:
            output_set[current_student.get_full_name()] = ['СП', current_student.entry_number]
            sp_counter -= 1
        else:
            output_set[current_student.get_full_name()] = ['КМ', current_student.entry_number]
            cn_counter -= 1

        student_counter += 1

    return output_set


def build_specialties_csv_file_response(information_set):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Входящ номер', 'Имена', 'Приет в специалност',
    ])

    for key, value in information_set.iteritems():
        writer.writerow([
            value[1], key, value[0],
        ])

    return response
