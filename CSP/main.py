from time import time
from heuristic import *
from data import *


def print_schedule(
    solution: Schedule,
):
    for day in week_schedule:
        print("\n" + "=" * 100)
        print(f"{week_schedule[day].upper()}")
        for time in time_schedule:
            print("\n\n" + time_schedule[time])
            for c in classrooms:
                print(f"\n{c}", end="\t\t")
                for i in range(len(solution.lessons)):
                    if (
                        solution.times[i].weekday == day
                        and solution.times[i].time == time
                        and solution.classrooms[i].room == c.room
                    ):
                        print(solution.lessons[i], end="")


def main():

    solution = run_benchmark(minimum_remaining_values)
    print_schedule(solution)

    print()

    #  Minimum Remaining Values
    start_time = time()
    run_benchmark(minimum_remaining_values)
    print(f"MRV: {time() - start_time}")

    #  Least Constraining Value
    start_time = time()
    run_benchmark(least_constraining_value)
    print(f"LCV: {time() - start_time}")

    #  Degree
    start_time = time()
    run_benchmark(largest_degree)
    print(f"Degree: {time() - start_time}")

    #  Forward checking
    run_benchmark(forward_checking)
    print(f"Forward checking: {time() - start_time}")


if __name__ == "__main__":
    main()
