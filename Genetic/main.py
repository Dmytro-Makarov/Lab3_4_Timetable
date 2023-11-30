import random

POPULATION_SIZE = 500

GENERATION_LIMIT = 100000

TIMETABLE_SIZE = 15

SUBJECTS = ["Math", "Philosophy", "Physics", "Geography"]
TEACHERS = ["Smith", "Camber", "Keppler", "Barack"]
GROUPS = ["A-1", "A-2", "B-1"]

GROUPS_W_SUBJECTS = [
    ("A-1", {"Math": 3, "Physics": 2}),
    ("A-2", {"Math": 2, "Physics": 2, "Philosophy": 1}),
    ("B-1", {"Physics": 1, "Philosophy": 2, "Geography": 2})
]

TEACHERS_W_SUBJECTS = [
    ("Smith", ["Math", "Physics"], 3),
    ("Camber", ["Math"], 5),
    ("Keppler", ["Philosophy", "Geography"], 6),
    ("Barack", ["Philosophy", "Physics"], 7),
]


class Class:
    def __init__(self, subject, teacher, group):
        self.subject = subject
        self.teacher = teacher
        self.group = group

    @classmethod
    def random_class(cls):
        subject = random.choice(SUBJECTS)
        teacher = random.choice(TEACHERS_W_SUBJECTS)
        group = random.choice(GROUPS_W_SUBJECTS)
        return Class(subject, teacher, group)


class Schedule(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls, gene):
        if gene is None:
            # Random gene
            gene = Class.random_class()
        else:
            prob = random.random()
            prob_list = []

            # Bigger Mutations are less probable
            if prob < 0.2:
                for _ in range(3):
                    prob_list.append(random.randint(0, 2))
            elif prob < 0.5:
                for _ in range(2):
                    prob_list.append(random.randint(0, 2))
            else:
                for _ in range(1):
                    prob_list.append(random.randint(0, 2))
            # Mutate an attribute
            for _ in prob_list:
                if _ == 0:
                    # Change Subject
                    gene.subject = random.choice(SUBJECTS)
                if _ == 1:
                    # Change Teacher
                    gene.teacher = random.choice(TEACHERS_W_SUBJECTS)
                if _ == 2:
                    # Change Group
                    gene.group = random.choice(GROUPS_W_SUBJECTS)

        return gene

    @classmethod
    def create_gnome(cls):
        global TIMETABLE_SIZE
        gnome_len = TIMETABLE_SIZE
        return [cls.mutated_genes(None) for _ in range(gnome_len)]

    def mate(self, par2):
        # chromosome for offspring
        child_chromosome = []

        # Avoid having an empty chromosome
        while not child_chromosome:
            # Uniform Crossover
            if random.random() < 0.7:
                for gp1, gp2 in zip(self.chromosome, par2.chromosome):
                    # insert gene from parent 1
                    if random.random() < 0.50:
                        child_chromosome.append(gp1)

                    # insert gene from parent 2
                    else:
                        child_chromosome.append(gp2)

            if random.random() < 0.2:
                # Self Mutation
                if not child_chromosome:
                    child_chromosome = self.chromosome

                number_of_mutations = random.randint(1, TIMETABLE_SIZE // 2)
                for _ in range(number_of_mutations):
                    gene = random.choice(child_chromosome)
                    child_chromosome[child_chromosome.index(gene)] = self.mutated_genes(gene)

        return Schedule(child_chromosome)

    def cal_fitness(self):
        teacher_overtime = 0
        teacher_wrong_subject = 0
        group_wrong_subject = 0
        group_not_enough_time_for_subject = 0

        for teacher in TEACHERS_W_SUBJECTS:
            if len([lecture for lecture in self.chromosome if lecture.teacher[0] == teacher[0]]) > teacher[2]:
                teacher_overtime += 1

        for group in GROUPS_W_SUBJECTS:
            # List all lectures of certain group with proper subject
            group_subject_lectures = [lecture for lecture in self.chromosome if
                                      lecture.subject in lecture.group[1] and lecture.group[0] == group[0]]
            if len(group_subject_lectures) == 0:
                continue

            for subject in SUBJECTS:
                if subject not in group_subject_lectures[0].group[1]:
                    continue

                if len([group_subject for group_subject in group_subject_lectures if
                        subject in group_subject.group[1]]) < group_subject_lectures[0].group[1][subject]:
                    group_not_enough_time_for_subject += 0

        for lecture in self.chromosome:
            if lecture.subject not in lecture.teacher[1]:
                teacher_wrong_subject += 1
            if lecture.subject not in lecture.group[1]:
                group_wrong_subject += 1

        fitness = teacher_overtime + teacher_wrong_subject + group_wrong_subject + group_not_enough_time_for_subject
        # if fitness <= 1:
        #     print("TO: {}, TWS: {}, GWO: {}, GTS: {}".format(teacher_overtime,teacher_wrong_subject, group_wrong_subject, group_not_enough_time_for_subject))
        return fitness


def main():
    global POPULATION_SIZE

    generation = 1

    stop = False
    population = []
    avg_fitness = 0

    # create initial population
    for _ in range(POPULATION_SIZE):
        gnome = Schedule.create_gnome()
        population.append(Schedule(gnome))

    while not stop:

        # sort the population in increasing order of fitness score
        population = sorted(population, key=lambda x: x.fitness)

        avg_fitness = 0
        for _ in population:
            avg_fitness += _.fitness
        avg_fitness /= len(population)

        # if the individual having lowest fitness score ie.
        # 0 then we know that we have reached to the target
        # and break the loop
        if population[0].fitness < 1 or generation > GENERATION_LIMIT:
            stop = True
            break

        # Otherwise generate new offsprings for new generation
        new_generation = []

        # Elitism, 10% of fittest population goes to the next generation
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:s])

        # From 50% of fittest population, population
        # will mate to produce offspring
        s = int((90 * POPULATION_SIZE) / 100)
        for _ in range(s):
            parent1 = random.choice(population[:POPULATION_SIZE // 2])
            parent2 = random.choice(population[:POPULATION_SIZE // 2])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        generation += 1

        if generation % 10 == 0:
            print_chromosome(generation, population[0].chromosome, population[0].fitness, population[-1].fitness,
                             avg_fitness)

    print_chromosome(generation, population[0].chromosome, population[0].fitness, population[-1].fitness, avg_fitness)


def print_chromosome(generation, chromosome, best_fitness, worst_fitness, avg_fitness):
    print("Generation: {}\tBest Fitness:{}\tWorst Fitness: {}\t Average Fitness: {}".format(generation, best_fitness,
                                                                                            worst_fitness, avg_fitness))
    for lecture in chromosome:
        print(
            "Class: {}\tTeacher: {} | Subject: {} | Group: {}".format(chromosome.index(lecture) + 1, lecture.teacher[0],
                                                                      lecture.subject, lecture.group[0]))
    print()


if __name__ == '__main__':
    main()
