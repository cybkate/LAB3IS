from ortools.sat.python import cp_model

lecturers = ['Lecturer1', 'Lecturer2', 'Lecturer3']
groups = ['Group1', 'Group2', 'Group3']
auditoriums = ['Auditorium1', 'Auditorium2', 'Auditorium3']
subjects = ['Math', 'Physics', 'Chemistry', 'Biology']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
time_slots = [1, 2, 3, 4]  # 1 - перша пара, 4 - четверта пара

# Множина змінних для задач CSP
model = cp_model.CpModel()

# Змінні: розклад для кожного предмета (лектора, групи, аудиторії, дня)
schedule = {}
for subject in subjects:
    for group in groups:
        for lecturer in lecturers:
            for auditorium in auditoriums:
                for day in days:
                    for time_slot in time_slots:
                        # Задаем переменные для расписания
                        schedule[(subject, group, lecturer, auditorium, day, time_slot)] = model.NewBoolVar(
                            f'{subject}_{group}_{lecturer}_{auditorium}_{day}_{time_slot}'
                        )

# Оюмеження:
# 1. Лектор не може вести дві пари одночасно.
for lecturer in lecturers:
    for day in days:
        for time_slot in time_slots:
            model.Add(
                sum(schedule[(subject, group, lecturer, auditorium, day, time_slot)]
                    for subject in subjects for group in groups for auditorium in auditoriums) <= 1
            )

# 2. Група не може мати два предмета одночасно
for group in groups:
    for day in days:
        for time_slot in time_slots:
            model.Add(
                sum(schedule[(subject, group, lecturer, auditorium, day, time_slot)]
                    for subject in subjects for lecturer in lecturers for auditorium in auditoriums) <= 1
            )

# 3. Аудиторія не може бути занята більш ніж одним предметом одночасно
for auditorium in auditoriums:
    for day in days:
        for time_slot in time_slots:
            model.Add(
                sum(schedule[(subject, group, lecturer, auditorium, day, time_slot)]
                    for subject in subjects for group in groups for lecturer in lecturers) <= 1
            )

# 4. Заняття має бути проведене (тобто по кожному предмету для кожної групи та лектора буде призначено заняття)
for subject in subjects:
    for group in groups:
        for lecturer in lecturers:
            model.Add(
                sum(schedule[(subject, group, lecturer, auditorium, day, time_slot)]
                    for auditorium in auditoriums for day in days for time_slot in time_slots) == 1
            )

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10.0  # Ограничение времени на поиск решения

status = solver.Solve(model)

# Вивід результата в табличному виді
if status == cp_model.OPTIMAL:
    # Ств. пустий розклад
    timetable = {day: {time_slot: [] for time_slot in time_slots} for day in days}

    # Заповнюємо розклад
    for subject in subjects:
        for group in groups:
            for lecturer in lecturers:
                for auditorium in auditoriums:
                    for day in days:
                        for time_slot in time_slots:
                            if solver.Value(schedule[(subject, group, lecturer, auditorium, day, time_slot)]) == 1:
                                timetable[day][time_slot].append(f'{subject} ({group}, {lecturer}, {auditorium})')

    print("Розклад на тиждень:")
    for day in days:
        print(f'\n{day}:')
        for time_slot in time_slots:
            print(f'  Пара {time_slot}:')
            if timetable[day][time_slot]:
                for session in timetable[day][time_slot]:
                    print(f'    {session}')
            else:
                print('    Нема пари')

else:
    print('Нема рішення')