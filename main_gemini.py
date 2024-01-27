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

	evol_prompts = []
	evol_prompts.append(createConstraintsPrompt(instruction))
	evol_prompts.append(createDeepenPrompt(instruction))
	evol_prompts.append(createConcretizingPrompt(instruction))
	evol_prompts.append(createReasoningPrompt(instruction))
	evol_prompts.append(createBreadthPrompt(instruction))

	selected_evol_prompt = random.choice(evol_prompts)


	evol_instruction = call_gemini(selected_evol_prompt)
	answer = call_gemini(evol_instruction)

	evol_objs.append({"instruction":evol_instruction,"output":answer})



with open('alpaca_data_evol.json', 'w') as f:	
	json.dump(evol_objs, f, indent=4)
