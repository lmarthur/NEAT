import csv
import random

from individual import individual, make_gene
from player import get_action, get_nodes

class Population:
	def __init__(self, init_indiv_function, init_gen_size):
		'''
		function init_indiv_function: returns one individual for the first generation
		integer  init_gen_size: size of the first generation
		'''

		#create List of generations, create first generation (list of dicts)
		self.generation_list = []
		self.add_generation() #create first generation

		#create list of parents ids. Only keeps track of most recent set of parents
		self.parents_IDs_list = []

		for i in range(init_gen_size):
			self.add_individual(init_indiv_function(), [], [])

	def add_generation(self):
		self.generation_list.append([]) #this is a dumb function

	def add_individual(self, genome, parent_ID_list, mutation_list=[], generation=-1):
		#add individual with ID i
		indiv_dict = {
		'id': len(self.generation_list[generation]), #id just the index in list. Unecessary, but for testing
		'genome': genome,
		'parents': parent_ID_list,
		'mutations': mutation_list,
		'fitness': -float('inf') #not yet tested
		}
		self.generation_list[generation].append(indiv_dict) #add indiv to most recent generation

	def test_generation(self, test_func, fitness_arg, generation=-1):
		#score all individuals in most recent gen
		for indiv in self.generation_list[generation]:
			genome = indiv['genome'] #actual code of indiv
			score = test_func(genome, fitness_arg)
			indiv['fitness'] = score

	def choose_parents_percentile(self, top_percent, high_low='high', generation=-1):
		'''
		Chooses parents for next generation via top_percentile based on fitness
		input:
			top_percent: float 0-1 indicating percent of pop to choose as parents
			high_low: is highest fitness best, or lowest? Input 'high' or 'low'
		output:
			list of IDs of parents
		'''
		ID_scores = [(indiv['id'], indiv['fitness']) for indiv in self.generation_list[generation]]
		if high_low == 'high':
			ID_scores = sorted(ID_scores, key=lambda x:x[1], reverse=True)
		elif high_low == 'low':
			ID_scores = sorted(ID_scores, key=lambda x:x[1])
		else:
			raise ValueError("Must input 'high' or 'low' for best fitness choice.")

		top_ID_scores = ID_scores[:int(len(ID_scores)*top_percent)]
		top_parent_IDs = [indiv[0] for indiv in top_ID_scores]

		self.parents_IDs_list = top_parent_IDs

	def create_next_generation(self, create_child_func, gen_size, mutation_rates):
		'''
		Generate next generation by randomly choosing parents, and applying create_child() function
		input: 
			function create_child: func to make a child from two parents
			gen_size: number of individuals in the new generation
		output: nothing
		'''

		#create new empty generation
		self.add_generation()

		for i in range(gen_size):
			#choose two parents from previous gen
			parent1 = random.choice(self.parents_IDs_list)
			parent2 = random.choice(self.parents_IDs_list)
			parent1_genome = self.generation_list[-2][parent1]['genome']
			parent2_genome = self.generation_list[-2][parent2]['genome']

			child_genome, mutation_list = create_child_func(parent1_genome, parent2_genome, mutation_rates)
			self.add_individual(child_genome, [parent1, parent2], mutation_list)


	def output_header_string(self):
		'''
		Output CSV header string for generation
		'''
		header = ['Generation', 'Population','Avg Fitness'] +['p'+str(n) for n in range(pop_size)] 
		#header += [x[0] for x in user_metrics]
		return header

	def output_generation_string(self, string_func):
		'''
		Input function turning genome into string for printing
		Output line for csv of current generation
		'''
		average_fitness = sum([indiv['fitness'] for indiv in self.generation_list[-1]])/len(self.generation_list[-1])
		csv_line = [len(self.generation_list), len(self.generation_list[-1]), average_fitness] + [string_func(indiv['genome']) for indiv in self.generation_list[-1]] 
		return csv_line

	def output_winners_strings(self, string_func):
		'''
		Output list of list for all lines in victor CSV
		'''
		lines = []
		lines.append(['Fitness', 'Individual'])
		for indiv in self.generation_list[-1]:
			lines.append([indiv['fitness'], indiv['genome']])
		return lines


### USER PROVIDED CODE
depth=10

input_number=9
internal_number=3
output_number=9
gene_length=7
genome_length=input_number+internal_number+output_number

def create_new_indiv():
	'''
	input: None
	output: runnable genome for individual
	'''
	return individual(genome_length)

def test_indiv(individual, filled_tiles, iterations):
	#'''
	#input: individual, which is runnable instantiation of class to test for fitness
			#fitness_arg: argument to change over time, in case you want to test criteria to vary. Can simply be gen #
	#output: numerical fitness score
	#'''
    
    #Turn board state into variable assignments for input nodes
    nodes=get_nodes(individual)
    input_nodes=nodes[0]
    
    #Initialize fitness variables
    fitness=0
    win_points=1/iterations
    lose_points=-(9-filled_tiles)/(iterations*filled_tiles)
    
    #Iterate to test multiple times
    for i in range(iterations):
        board_state=fill_ttt_board(filled_tiles)
        for node in input_nodes:
            ID=node.ID
            input_nodes[ID].initial=board_state[ID]
    
        #Get action step
        action=get_action(individual)
    
        #If action in filled board state, then bad fitness. If not, good fitness
        if board_state[action]==0:
            fitness+=win_points
        elif board_state[action]!=0:
            fitness+=lose_points
    
    return fitness

def create_child(parent1, parent2, mutation_rates):
    
    addition_rate     = 0.1
    subtraction_rate  = 0.1
    substitution_rate = 0.1
    crossover_rate    = 0.9
    
    parent_length=int(((len(parent1.genome)+len(parent2.genome))/(2*gene_length)))
    #Crossover
    if random.random()<crossover_rate:
        randvar=random.randint(0, parent_length)
        first_half=parent1.genome[0:randvar*gene_length]
        second_half=parent2.genome[len(first_half)::]
        new_genome=first_half+second_half
    else:
        new_genome=parent1.genome
        
    #Substitution
    if random.random()<substitution_rate:
        alphabet="0123456789abcdef"
        insertion=alphabet[random.randint(0, 15)]
        randvar=random.randint(0, len(new_genome))
        update=new_genome[:randvar-1]+insertion+new_genome[randvar:]
        new_genome=update
        
    #Addition
    if random.random()<addition_rate:
        new_genome=new_genome+make_gene(7)
    
    #Subtraction
    if random.random()<subtraction_rate:
        new_genome=new_genome[0:-7]
    
            
    #instantiate child
    child_length=parent_length
    child=individual(child_length)
    child.genome=new_genome
    
    
    return child

def genome_to_string(individual):
	'''
	input: runnable genome of individual
	output: string representing that genome
	'''
	return None

#Function to create random board state with filled_tiles number of filled tiles
def fill_ttt_board(filled_tiles):
	'''
	Input: number of tiles to be filled
	output: board state where -1 is o and +1 is x
	'''

	if filled_tiles % 2 == 0:
		x_tiles = random.sample(range(9), filled_tiles//2)
		o_tiles = random.sample([o for o in range(9) if o not in x_tiles], filled_tiles//2)
	else:
		#give one extra to x or o:
		if random.random() < 0.5:
			x_tiles = random.sample(range(9), filled_tiles//2+1)
			o_tiles = random.sample([o for o in range(9) if o not in x_tiles], filled_tiles//2)
		else:
			x_tiles = random.sample(range(9), filled_tiles//2)
			o_tiles = random.sample([o for o in range(9) if o not in x_tiles], filled_tiles//2+1)

	#get board state
	board_state = [0]*9
	for x in x_tiles:
		board_state[x] = 1 
	for o in o_tiles:
		board_state[o] = -1 

	#print_board(board_state)
	#print()
	return board_state

### RUN PARAMETERS
#by calculating as a function of gen, these can change over time.
pop_size = 10
generations = 10
parents_percentile = 0.2
mutation_rates = (0,0,0,0)

#population size, parent selection, mutation rates, 

### START RUN
population = Population(create_new_indiv, pop_size)
run_data = open('run_data.csv', 'w')
writer = csv.writer(run_data)
writer.writerow(population.output_header_string())

for gen in range(generations):
	print('Generation:', gen)
	writer.writerow(population.output_generation_string(genome_to_string))
	#score current generation 
	fitness_arg = gen
	population.test_generation(test_indiv, fitness_arg, 10)

	#choose parents
	population.choose_parents_percentile(parents_percentile, 'high')

	#make next generation
	population.create_next_generation(create_child, pop_size, mutation_rates)

run_data.close()
final_data = open('final_data.csv', 'w')
writer = csv.writer(final_data)
for line in population.output_winners_strings(genome_to_string):
	writer.writerow(line)
final_data.close()



###GP run skeleton
'''
generate starting population
	parameters?
	size?
loop:
evaluate + score population
	individual scoring funcs
	tournament funcs
choose parents
	different funcs
make next gen population from parents
	mutation rate, crossover rate. dT?
	next gen size. Same, dT?
	Keep track of parents.

Output best individual from final generation
'''


