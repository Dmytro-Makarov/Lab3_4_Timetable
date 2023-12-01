from collections import namedtuple

week_schedule = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}
time_schedule = {
    1: "8:40-10:15",
    2: "10:35-12:10",
    3: "12:20-13:55",
}

#  Main data classes
Classroom = namedtuple("Classroom", "room is_big")
Time = namedtuple("Time", "weekday time")
Teacher = namedtuple("Teacher", "name")
Subject = namedtuple("Subject", "name")
Group = namedtuple("Group", "name")
Lesson = namedtuple("Lesson", "teacher subject group is_lecture per_week")
Schedule = namedtuple("Schedule", "lessons classrooms times")
DomainElement = namedtuple("DomainElement", "day time room")

Classroom.__repr__ = lambda c: f"{c.room} ({'big' if c.is_big else 'small'})"
Teacher.__repr__ = lambda t: f"{t.name.split()[1]}"
Subject.__repr__ = lambda s: f"{s.name.split()[1]}"
Group.__repr__ = lambda g: f"{g.name}"
Lesson.__repr__ = (
    lambda l: f"{l.teacher} | {l.subject} | {l.group} | "
    f"{'Lecture' if l.is_lecture else 'Seminar'} {l.per_week}/week"
)


def gen_repr(g: Schedule):
    output = ""
    for i in range(len(g.lessons)):
        output += f"{g.lessons[i]},   {g.classrooms[i]},   {g.times[i]}\n"
    return output


Schedule.__repr__ = lambda g: gen_repr(g)

#  Sample data for schedule
classrooms = [
    Classroom(43, True),
    Classroom(42, True),
    Classroom(41, True),
    Classroom(228, False),
    Classroom(217, False),
    Classroom(206, False),
]

schedule = [
    Time(w, n)
    for w in range(1, len(week_schedule.keys()) + 1)
    for n in range(1, len(week_schedule.keys()) + 1)
]

teachers = [
    Teacher(name)
    for name in (
        "0 Teacher_1",
        "1 Teacher_2",
        "2 Teacher_3",
        "3 Teacher_4",
        "4 Teacher_5",
        "5 Teacher_6",
        "6 Teacher_7",
        "7 Teacher_8",
        "8 Teacher_9",
        "9 Teacher_10",
        "10 Teacher_11",
        "11 Teacher_12",
        "12 Teacher_13",
        "13 Teacher_14",
        "14 Teacher_15",
        "15 Teacher_16",
        "16 Teacher_17",
        "17 Teacher_18",
        "18 Teacher_19",
    )
]

subjects = [
    Subject(name)
    for name in (
        "0 Subject_1",
        "1 Subject_2",
        "2 Subject_3",
        "3 Subject_4",
        "4 Subject_5",
        "5 Subject_6",
        "6 Subject_7",
        "7 Subject_8",
        "8 Subject_9",
        "9 Subject_10",
        "10 Subject_11",
        "11 Subject_12",
        "12 Subject_13",
        "13 Subject_14",
        "14 Subject_15",
        "15 Subject_16",
        "16 Subject_17",
        "17 Subject_18",
    )
]

groups = [
    Group(name)
    for name in (
        "Group_1",
        "Group_2",
        "Group_3",
        "Group_4",
        "Group_5",
    )
]

lessons = [
    Lesson(teachers[0], subjects[0], groups[0], False, 1),
    Lesson(teachers[1], subjects[1], groups[0:5], True, 1),
    Lesson(teachers[2], subjects[2], groups[0], True, 2),
    Lesson(teachers[2], subjects[2], groups[0], True, 2),
    Lesson(teachers[3], subjects[12], groups[0], True, 1),
    Lesson(teachers[4], subjects[4], groups[0:5], True, 1),
    Lesson(teachers[5], subjects[4], groups[0], False, 1),
    Lesson(teachers[5], subjects[15], groups[0], True, 1),
    Lesson(teachers[9], subjects[6], groups[0:5], True, 1),
    Lesson(teachers[13], subjects[4], groups[0], False, 1),
    Lesson(teachers[13], subjects[16], groups[0], True, 2),
    Lesson(teachers[13], subjects[16], groups[0], True, 2),
    Lesson(teachers[5], subjects[4], groups[1], False, 1),
    Lesson(teachers[5], subjects[4], groups[2], False, 1),
    Lesson(teachers[6], subjects[4], groups[1], False, 1),
    Lesson(teachers[7], subjects[4], groups[2], False, 1),
    Lesson(teachers[8], subjects[3], groups[1:3], True, 1),
    Lesson(teachers[10], subjects[7], groups[1], False, 2),
    Lesson(teachers[10], subjects[7], groups[1], False, 2),
    Lesson(teachers[10], subjects[7], groups[2], False, 2),
    Lesson(teachers[10], subjects[7], groups[2], False, 2),
    Lesson(teachers[11], subjects[8], groups[1:3], True, 2),
    Lesson(teachers[11], subjects[8], groups[1:3], True, 2),
    Lesson(teachers[12], subjects[9], groups[1:3], True, 2),
    Lesson(teachers[12], subjects[9], groups[1:3], True, 2),
    Lesson(teachers[18], subjects[10], groups[1:3], True, 1),
    Lesson(teachers[5], subjects[4], groups[3], False, 1),
    Lesson(teachers[5], subjects[4], groups[4], False, 1),
    Lesson(teachers[6], subjects[4], groups[3], False, 1),
    Lesson(teachers[6], subjects[4], groups[4], False, 1),
    Lesson(teachers[14], subjects[12], groups[3:5], True, 2),
    Lesson(teachers[14], subjects[12], groups[3:5], True, 2),
    Lesson(teachers[15], subjects[13], groups[3:5], False, 1),
    Lesson(teachers[16], subjects[11], groups[3:5], True, 2),
    Lesson(teachers[16], subjects[11], groups[3:5], True, 2),
    Lesson(teachers[17], subjects[14], groups[3:5], True, 1),
    Lesson(teachers[17], subjects[17], groups[3:5], True, 1),
]