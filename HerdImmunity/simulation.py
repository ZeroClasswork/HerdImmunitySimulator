import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.

        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = initial_infected # Int
        self.current_infected = initial_infected # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            self.virus.name, self.pop_size, self.vacc_percentage, self.initial_infected)
        self.newly_infected = []

        # Populated self.population using _create_population() method
        self.population = self._create_population() # List of Person objects

        # Created a Logger object and bind it to self.logger
        self.logger = Logger(self.file_name) 

    def _create_population(self):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.

        population = []

        for i in range(self.initial_infected):
            new_person = Person(i, False, self.virus)
            population.append(new_person)

        vaccinated_population_count = int(self.vacc_percentage * self.pop_size)

        for i in range(vaccinated_population_count):
            new_person = Person(i + self.initial_infected, True)
            population.append(new_person)

        healthy_unvaccinated_population_count = self.pop_size - self.initial_infected - vaccinated_population_count
        for i in range(healthy_unvaccinated_population_count):
            new_person = Person(self.pop_size - i, False)
            population.append(new_person)
        return population

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.
        for person in self.population:
            if person.is_alive and not person.is_vaccinated:
                return True
        return False

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper

        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, 
                self.virus.mortality_rate, self.virus.repro_rate)

        time_step_counter = 0
        while self._simulation_should_continue():
            # TODO: for every iteration of this loop, call self.time_step() to compute another
            # round of this simulation.
            time_step_counter += 1
            print(time_step_counter)
            self.time_step()
            self._evaluate_infected()
            self._infect_newly_infected()

        print('The simulation has ended after {} turns.'.format(time_step_counter))

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.
        interaction_count = 0
        for person in self.population:
            if person.infection == self.virus and person.is_alive and not person.is_vaccinated:
                for i in range(100):
                    if not self._simulation_should_continue():
                        return interaction_count
                    other_person = random.choice(self.population)
                    while not other_person.is_alive:
                        other_person = random.choice(self.population)
                    self.interaction(person, other_person)
                    interaction_count += 1 
        return interaction_count

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.
        did_infect = False
        if (not random_person.is_vaccinated) and (not random_person.infection == self.virus):
            if self.virus.repro_rate > random.random():
                self.newly_infected.append(random_person)
                did_infect = True
        
        self.logger.log_interaction(person, random_person, random_person.infection is not None,
                random_person.is_vaccinated, did_infect)

    def _evaluate_infected(self):
        ''' This method should iterate through the population and either kill off or immunize the infected. '''
        for person in self.population:
            if person.infection is not None:
                person.did_survive_infection()

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of Person objects stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.newly_infected:
            person.infection = self.virus
        self.newly_infected = []

if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_rate = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()
