# -*- coding: utf-8 -*-
from campaigns.models import *

def get_populated_student_specialties(campaign, system_programing_count, computer_networks_count, start_position):
    student_set = campaign.student_set.all()
    output_set = dict()
    start_position = int(start_position)
    end_position = start_position + int(system_programing_count) + int(computer_networks_count)

    # print(start_position, end_position)

    # for s in student_set:
    #     print(s.entry_number, s.grades_evaluated)
    requested_students = sorted(
        student_set,
        key = lambda student: student.grades_evaluated,
        reverse = True
    )[start_position-1:end_position]
    # print("+++++++++++++++++++++++++++")
    # for s in requested_students:
    #     print(s.entry_number, s.grades_evaluated)

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

    # print("++++++++++++++++++++++++++++")
    # print(output_set)

    return output_set
