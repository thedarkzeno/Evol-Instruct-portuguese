import json
import random

from gemini_access import call_gemini
from depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from breadth import createBreadthPrompt
from tqdm.auto import tqdm

with open('cabrita-dataset-52k.json','r', encoding="utf-8") as file:

	all_objs = json.load(file)

try:
	with open('alpaca_data_evol.json','r', encoding="utf-8") as file:

		evol_objs = json.load(file)
except:
    evol_objs = []


i=0
for cur_obj in tqdm(all_objs[len(evol_objs):]):
	
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
	if i>0 and i%10 == 0:
		with open('alpaca_data_evol.json', 'w') as f:	
			json.dump(evol_objs, f, indent=4)
	i+=1

with open('alpaca_data_evol.json', 'w', encoding="utf-8") as f:	
	json.dump(evol_objs, f, indent=4)
