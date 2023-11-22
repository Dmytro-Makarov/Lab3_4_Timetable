from copy import copy
from dataclasses import dataclass
import random


@dataclass
class Group:
    name: str
    required_subjects: list[str]


@dataclass
class Teacher:
    name: str
    available_time: int
    knowledgeable_subjects: list[str]


@dataclass
class Timeslot:
    subject_id: int
    teacher_id: int
    group_id: int


class Schedule:
    def __init__(self, subjects, teachers, groups, days, timeslots_per_day):
        self.subjects = subjects
        self.teachers = teachers
        self.groups = groups
        self.days = days
        self.timeslots_per_day = timeslots_per_day
        self.timetable = self.generate_random_schedule()

    def generate_random_schedule(self):
        timetable_size = len(self.days) * self.timeslots_per_day
        timetable = list()
        for _ in range(timetable_size):
            timetable.append(
                Timeslot(
                    subject_id=random.randint(0, subjects_size - 1),
                    teacher_id=random.randint(0, teachers_size - 1),
                    group_id=random.randint(0, groups_size - 1)
                ))
        return timetable

    def fitness(self):
        conflicts = 0

        # Teacher's available time conflict
        for _ in range(teachers_size):
            if len([timeslot for timeslot in self.timetable if timeslot.teacher_id == _]) > self.teachers[
                _].available_time:
                conflicts += 1

        # Subject conflict
        for _ in self.timetable:
            # Teachers
            if self.subjects[_.subject_id] not in self.teachers[_.teacher_id].knowledgeable_subjects:
                conflicts += 1

            # Groups
            if self.subjects[_.subject_id] not in self.groups[_.group_id].required_subjects:
                conflicts += 1

        return 1.0 / (conflicts + 1.0)


class GeneticAlgorithm:
    def __init__(self, population_size):
        self.population = self.generate_population(population_size)

    @staticmethod
    def generate_population(population_size):
        return [Schedule(SUBJECTS, TEACHERS, GROUPS, DAYS, TIMESLOTS_PER_DAY) for _ in range(population_size)]

    @staticmethod
    def crossover(schedule1, schedule2):
        crossover_point1 = random.randint(1, len(schedule1.timetable) - 1)
        crossover_point2 = random.randint(1, len(schedule1.timetable) - 1)

        start = min(crossover_point1, crossover_point2)
        end = max(crossover_point1, crossover_point2)

        child1 = copy(schedule1)
        child2 = copy(schedule2)

        child1.timetable = schedule1.timetable[:start] + schedule2.timetable[start:end] + schedule1.timetable[end:]
        child2.timetable = schedule2.timetable[:start] + schedule1.timetable[start:end] + schedule2.timetable[end:]
        return child1, child2

    def select_best(self, fitness_scores):
        best_index = max(range(len(self.population)), key=lambda i: fitness_scores[i])

        return self.population[best_index], fitness_scores[best_index]

    def mutate(self, schedule):
        if random.random() < MUTATION_RATE:
            timeslot_id = random.randint(0, len(schedule.days) * schedule.timeslots_per_day - 1)
            timeslot = schedule.timetable[timeslot_id]
            timeslot_property = random.randint(0, 2)
            if timeslot_property == 0:
                timeslot.subject_id = random.randint(0, len(schedule.subjects) - 1)
            elif timeslot_property == 1:  # Attempt to pick a teacher with fitting subject
                i = 0
                timeslot.teacher_id = random.randint(0, len(schedule.teachers) - 1)  # At least one mutation is required
                while schedule.subjects[timeslot.subject_id] not in schedule.teachers[
                    timeslot.teacher_id].knowledgeable_subjects:
                    i += 1
                    if i > 20:
                        break
                    timeslot.teacher_id = random.randint(0, len(schedule.teachers) - 1)

            else:  # Attempt to pick a group with fitting subject
                i = 0
                timeslot.group_id = random.randint(0, len(schedule.groups) - 1)  # At least one mutation is required
                while schedule.subjects[timeslot.subject_id] not in schedule.groups[
                    timeslot.group_id].required_subjects:
                    i += 1
                    if i > 20:
                        break
                    timeslot.group_id = random.randint(0, len(schedule.groups) - 1)
        return schedule

    def start(self):
        best_schedule = None
        best_fitness_score = 0
        for _ in range(GENERATIONS):
            fitness_scores = [schedule.fitness() for schedule in self.population]
            best_schedule, best_fitness_score = self.select_best(fitness_scores)
            new_population = []
            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = random.choices(self.population, weights=fitness_scores, k=2)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            self.population = new_population
        return best_schedule, best_fitness_score


TIMESLOTS_PER_DAY = 3

POPULATION_SIZE = 20
MUTATION_RATE = 0.1
GENERATIONS = 100

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SUBJECTS = ["A", "B", "C", "D", "E"]

TEACHERS = [
    Teacher(
        name="TA",
        available_time=6,
        knowledgeable_subjects=[
            "B",
            "A"
        ]
    ),
    Teacher(
        name="TB",
        available_time=4,
        knowledgeable_subjects=[
            "C",
        ]
    ),
    Teacher(
        name="TC",
        available_time=5,
        knowledgeable_subjects=[
            "D",
            "C"
        ]
    ),
    Teacher(
        name="TD",
        available_time=2,
        knowledgeable_subjects=[
            "B",
            "C",
            "E"
        ]
    )
]

GROUPS = [
    Group(
        name="GA",
        required_subjects=[
            "A",
            "B"
        ]
    ),
    Group(
        name="GB",
        required_subjects=[
            "B",
            "C",
            "D"
        ]
    ),
    Group(
        name="GC",
        required_subjects=[
            "D",
            "E"
        ]
    )
]

subjects_size = len(SUBJECTS)
teachers_size = len(TEACHERS)
groups_size = len(GROUPS)

if __name__ == '__main__':
    genetic = GeneticAlgorithm(POPULATION_SIZE)
    best_schedule, fitness = genetic.start()
    best_schedule.timetable.reverse()

    for day in DAYS:
        for _ in range(0, TIMESLOTS_PER_DAY):
            timeslot = best_schedule.timetable.pop()
            print(f'{day}, Class {_}: {SUBJECTS[timeslot.subject_id]} by {TEACHERS[timeslot.teacher_id].name} for {GROUPS[timeslot.group_id].name}')

    print(f'Fitness score: {fitness}')

