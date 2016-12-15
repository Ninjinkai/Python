import unicodecsv
from datetime import datetime as dt

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

print(surprising_ids)

for enrollment in enrollments:
    if enrollment['account_key'] in surprising_ids:
        if enrollment['days_to_cancel'] != 0:
            print(enrollment)

paid_students = {}
for enrollment in enrollments:
    if not enrollment['is_udacity']:
        if enrollment['days_to_cancel'] is None or enrollment['days_to_cancel'] > 7:
            if enrollment['account_key'] not in paid_students \
                    or enrollment['join_date'] > paid_students[enrollment['account_key']]:
                paid_students[enrollment['account_key']] = enrollment['join_date']

print(len(paid_students))