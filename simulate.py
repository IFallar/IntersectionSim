import simpy
import random
import statistics

wait_times = []


class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.servers = simpy.Resource(env, num_servers)
        self.ushers = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 5))


def go_to_movies(env, moviegoer, theater):
    arrival_time = env.now

    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))

    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))

    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.sell_food(moviegoer))

    if random.choice([True, False]):
        with theater.servers.request() as request:
            yield request
            yield request
            yield env.process(theater.sell_food(moviegoer))

        wait_times.append(env.now - arrival_time)


def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)

    for moviegoer in range(3):
        env.process(go_to_movies(env, moviegoer, theater))

    while True:
        yield env.timeout(0.20)

        moviegoer += 1


def get_average_wait_time(wait_times):

    average_wait = statistics.mean(wait_times)
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def get_user_input():

    num_cashiers = input("Input # of cashiers working: ")
    num_servers = input("Input # of servers working: ")
    num_ushers = input("Input # of ushers working: ")
    params = [num_cashiers, num_servers, num_ushers]
      
    if all(str(i).isdigit() for i in params):
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:", 
            "\n1 cashier, 1 server, 1 usher.",
            )
        params = [1, 1, 1]
            
    return params


def main():

    random.seed(42)
    num_cashiers, num_servers, num_ushers = get_user_input()

    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
    env.run(until=90)
    mins, secs = get_average_wait_time(wait_times)
    print("Running simulation...")
    print(f"\nThe average wait time is {mins} minutes and {secs} seconds.")


if __name__ == '__main__':
    main()

    