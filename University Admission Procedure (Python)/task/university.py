departments = sorted(('Mathematics', 'Physics', 'Biotech', 'Chemistry', 'Engineering'))


def average_results(results, dep1, dep2):
    return (results[dep1] + results[dep2]) / 2


def score(applicant, department):
    results = applicant['gpa']
    match department:
        case 'Physics':
            gpa_result = average_results(results, 'Physics', 'Mathematics')
        case 'Mathematics':
            gpa_result = results['Mathematics']
        case 'Chemistry':
            gpa_result = results['Chemistry']
        case 'Engineering':
            gpa_result = average_results(results, 'Mathematics', 'Computer Science')
        case 'Biotech':
            gpa_result = average_results(results, 'Chemistry', 'Physics')
        case _:
            gpa_result = 0
    return max(gpa_result, applicant['special'])


max_in_department = int(input())
with open('applicants.txt') as f:
    data = [line.strip().split() for line in f.readlines()]

applicants = []
for row in data:
    app = {'name': row[0],
           'surname': row[1],
           'gpa': {'Physics': float(row[2]),
                   'Chemistry': float(row[3]),
                   'Mathematics': float(row[4]),
                   'Computer Science': float(row[5])},
           'special': float(row[6]),
           'first': row[7],
           'second': row[8],
           'third': row[9]
           }
    applicants.append(app)

mapping_gpa = {
    'Physics': 'Physics',
    'Chemistry': 'Chemistry',
    'Mathematics': 'Mathematics',
    'Engineering': 'Computer Science',
    'Biotech': 'Chemistry'
}

selected_applicants = {dep: [] for dep in departments}
for wave in ('first', 'second', 'third'):
    for dep in departments:
        if len(selected_applicants[dep]) < max_in_department:
            candidates_in_dep = [app for app in applicants if app[wave] == dep]
            candidates_in_dep.sort(key=lambda x: (-score(x, dep), x[wave], x['name'], x['surname']))
            free_places = max_in_department - len(selected_applicants[dep])
            for i in range(min(free_places, len(candidates_in_dep))):
                selected = candidates_in_dep[i]
                selected_applicants[dep].append(selected)
                applicants.remove(selected)

for dep in departments:
    selected_applicants[dep] = sorted(selected_applicants[dep],
                                      key=lambda x: (-score(x, dep), x['name'], x['surname']))
    fields = [(app['name'], app['surname'], str(score(app, dep))) for app in selected_applicants[dep]]
    formatted_best = [' '.join(field) for field in fields]
    with open(f'{dep}.txt', 'w') as f:
        for line in formatted_best:
            f.write(line + '\n')
