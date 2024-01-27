import json
import random

from gemini_access import call_gemini
from depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from breadth import createBreadthPrompt


fr = open('alpaca_data.json','r')

all_objs = json.load(fr)

evol_objs = []


for cur_obj in all_objs:
	
	instruction = cur_obj['instruction'].strip() + '\r\n'+ cur_obj['input'].strip()

	strategy = random.randint(0, 4)
	
	if strategy == 0:
		selected_evol_prompt = createConstraintsPrompt(instruction)
	elif strategy == 1:
		selected_evol_prompt = createDeepenPrompt(instruction)
	elif strategy == 2:
		selected_evol_prompt = createConcretizingPrompt(instruction)
	elif strategy == 3:
		selected_evol_prompt = createReasoningPrompt(instruction)
	else:
		selected_evol_prompt = createBreadthPrompt(instruction)
	
	

	evol_instruction = call_gemini(selected_evol_prompt)
	answer = call_gemini(evol_instruction)

	evol_objs.append({"instruction":evol_instruction,"output":answer})



with open('alpaca_data_evol.json', 'w') as f:	
	json.dump(evol_objs, f, indent=4)
