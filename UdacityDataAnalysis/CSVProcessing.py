import unicodecsv
from datetime import datetime as dt
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv(enrollments_filename)
daily_engagement = read_csv(engagement_filename)
project_submissions = read_csv(submissions_filename)

# print(enrollments[0])
# print(daily_engagement[0])
# print(project_submissions[0])

def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students

def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0

def remove_free_trial_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data

def get_test_account_keys(data):
    test_account_keys = set()
    for data_point in data:
        if data_point['is_udacity']:
            test_account_keys.add(data_point['account_key'])
    return test_account_keys

def remove_test_accounts(data, enrollments_dictionary):
    test_account_keys = get_test_account_keys(enrollments_dictionary)
    new_data = []
    for data_point in data:
        if data_point['account_key'] not in test_account_keys:
            new_data.append(data_point)
    return new_data

def get_students_by_id(ids_to_get, data):
    records_by_id = []
    for student_id in ids_to_get:
        for data_point in data:
            if data_point['account_key'] == student_id:
                records_by_id.append(data_point)
    return records_by_id

def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data

def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total
    return summed_data

def count_grouped_items(grouped_data, field_name):
    count_data = {}
    for key, data_points in grouped_data.items():
        count = 0
        for data_point in data_points:
            if data_point[field_name] > 0:
                count += 1
        count_data[key] = count
    return count_data

def describe_data(data):
    print("Mean: " + str(np.mean(list(data.values()))))
    print("Std: " + str(np.std(list(data.values()))))
    print("Min: " + str(np.min(list(data.values()))))
    print("Max: " + str(np.max(list(data.values()))))

def show_hists(data, x_axis_label, y_axis_label, plot_title):
    plt.show()
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.title(plot_title)
    plt.hist(list(data.values()))

for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

# print(enrollments[0])
# print(daily_engagement[0])
# print(project_submissions[0])

# print(len(get_unique_students(enrollments)))
# print(len(enrollments))
# print(len(get_unique_students(daily_engagement)))
# print(len(daily_engagement))
# print(len(get_unique_students(project_submissions)))
# print(len(project_submissions))

enrolled_student_ids = get_unique_students(enrollments)
engaged_student_ids = get_unique_students(daily_engagement)
surprising_ids = set()

for enrolled_student_id in enrolled_student_ids:
    if enrolled_student_id not in engaged_student_ids:
        surprising_ids.add(enrolled_student_id)

# print(surprising_ids)

# for enrollment in enrollments:
#     if enrollment['account_key'] in surprising_ids:
#         if enrollment['days_to_cancel'] != 0:
#             print(enrollment)

paid_students = {}
for enrollment in enrollments:
    if not enrollment['is_udacity']:
        if enrollment['days_to_cancel'] is None or enrollment['days_to_cancel'] > 7:
            if enrollment['account_key'] not in paid_students \
                    or enrollment['join_date'] > paid_students[enrollment['account_key']]:
                paid_students[enrollment['account_key']] = enrollment['join_date']

# print(len(paid_students))

non_udacity_enrollments = remove_test_accounts(enrollments, enrollments)
non_udacity_engagement = remove_test_accounts(daily_engagement, enrollments)
non_udacity_submissions = remove_test_accounts(project_submissions, enrollments)

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)

# print(len(paid_enrollments))
# print(len(paid_engagement))
# print(len(paid_submissions))

for engagement_record in paid_engagement:
    if engagement_record['num_courses_visited'] > 0:
        engagement_record['has_visited'] = 1
    else:
        engagement_record['has_visited'] = 0

paid_engagement_in_first_week = []

for engagement_record in paid_engagement:
    account_key = engagement_record['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement_record['utc_date']

    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement_record)

# print(len(paid_engagement_in_first_week))

# engagement_by_account = defaultdict(list)
# for engagement_record in paid_engagement_in_first_week:
#     account_key = engagement_record['account_key']
#     engagement_by_account[account_key].append(engagement_record)

# total_minutes_by_account = {}
# for account_key, engagement_for_student in engagement_by_account.items():
#     total_minutes = 0
#     for engagement_record in engagement_for_student:
#         total_minutes += engagement_record['total_minutes_visited']
#     total_minutes_by_account[account_key] = total_minutes

# average_minutes_all_accounts = 0
# for account_key, total_minutes in total_minutes_by_account.items():
#     average_minutes_all_accounts += total_minutes
# average_minutes_all_accounts /= len(total_minutes_by_account)
# print(average_minutes_all_accounts)

# print(np.mean(list(total_minutes_by_account.values())))
# print(np.max(list(total_minutes_by_account.values())))
# print(np.min(list(total_minutes_by_account.values())))
# print(np.std(list(total_minutes_by_account.values())))

# mins_in_week = 10080
# surprising_weekly_engagement = []
# for account_key in total_minutes_by_account.keys():
#     if total_minutes_by_account[account_key] >= mins_in_week:
#         surprising_weekly_engagement.append(account_key)

# max_total_minutes_account = ['']
# max_total_minutes = 0
# for account_key, minutes_spent in total_minutes_by_account.items():
#     if minutes_spent > max_total_minutes:
#         max_total_minutes_account[0] = account_key
#         max_total_minutes = minutes_spent
#
# print(get_students_by_id(max_total_minutes_account, daily_engagement))
# print(get_students_by_id(max_total_minutes_account, enrollments))
# print(get_students_by_id(max_total_minutes_account, paid_engagement_in_first_week))

# total_lessons_by_account = {}
# for account_key, engagement_for_student in engagement_by_account.items():
#     total_lessons_completed = 0
#     for engagement_record in engagement_for_student:
#         total_lessons_completed += engagement_record['lessons_completed']
#     total_lessons_by_account[account_key] = total_lessons_completed
#
# print(np.mean(list(total_lessons_by_account.values())))
# print(np.std(list(total_lessons_by_account.values())))
# print(np.min(list(total_lessons_by_account.values())))
# print(np.max(list(total_lessons_by_account.values())))

# engagement_by_account = group_data(paid_engagement_in_first_week, 'account_key')
# summed_lessons = sum_grouped_items(engagement_by_account, 'lessons_completed')
# summed_time = sum_grouped_items(engagement_by_account, 'total_minutes_visited')
# describe_data(summed_lessons)
# describe_data(summed_time)

# engagement_days_by_account = group_data(paid_engagement_in_first_week, 'account_key')
# count_of_lessons = count_grouped_items(engagement_days_by_account, 'num_courses_visited')
# describe_data(count_of_lessons)
#
# engagement_days_by_account = group_data(paid_engagement_in_first_week, 'account_key')
# count_of_lessons = sum_grouped_items(engagement_days_by_account, 'has_visited')
# describe_data(count_of_lessons)

subway_project_lesson_keys = ['746169184', '3176718735']
passing_engagement = []
non_passing_engagement = []
passed_subway_project_accounts = set()

for submission in paid_submissions:
    project = submission['lesson_key']
    rating = submission['assigned_rating']
    if project in subway_project_lesson_keys and (rating == 'PASSED' or rating == 'DISTINCTION'):
        passed_subway_project_accounts.add(submission['account_key'])

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] in passed_subway_project_accounts:
        passing_engagement.append(engagement_record)
    else:
        non_passing_engagement.append(engagement_record)

# print(len(passing_engagement))
# print(len(non_passing_engagement))

passing_engagement_by_account = group_data(passing_engagement, 'account_key')
non_passing_engagement_by_account = group_data(non_passing_engagement, 'account_key')

minutes_passing = sum_grouped_items(passing_engagement_by_account, 'total_minutes_visited')
minutes_non_passing = sum_grouped_items(non_passing_engagement_by_account, 'total_minutes_visited')

# print("Passing by minutes:")
# describe_data(minutes_passing)
# print("Non-passing by minutes:")
# describe_data(minutes_non_passing)
# show_hists(minutes_passing)
# show_hists(minutes_non_passing)

lessons_passing = sum_grouped_items(passing_engagement_by_account, 'lessons_completed')
lessons_non_passing = sum_grouped_items(non_passing_engagement_by_account, 'lessons_completed')

# print("Passing by lessons:")
# describe_data(lessons_passing)
# print("Non-passing by lessons:")
# describe_data(lessons_non_passing)
# show_hists(lessons_passing, "Lessons", "Number of Students", "Passed")
# show_hists(lessons_non_passing, "Lessons", "Number of Students", "Not Passed")

days_passing = sum_grouped_items(passing_engagement_by_account, 'has_visited')
days_non_passing = sum_grouped_items(non_passing_engagement_by_account, 'has_visited')

# print("Passing by days:")
# describe_data(days_passing)
# print("Non-passing by days:")
# describe_data(days_non_passing)
# show_hists(days_passing)
# show_hists(days_non_passing)