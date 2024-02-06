import json
import random


from depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from breadth import createBreadthPrompt
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from tqdm.auto import tqdm

with open('cabrita-dataset-52k.json','r', encoding="utf-8") as file:
	all_objs = json.load(file)

model_list = ["NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO", "NousResearch/Nous-Hermes-2-SOLAR-10.7B", "cognitivecomputations/dolphin-2.5-mixtral-8x7b", "cognitivecomputations/dolphin-2.6-mistral-7b-dpo-laser"]

for model_id in model_list:
    # model = AutoModelForCausalLM.from_pretrained(model_id, 
    #                                              torch_dtype=torch.bfloat16, 
    #                                              load_in_8bit=True, 
    #                                              llm_int8_has_fp16_weight=True,
    #                                              llm_int8_enable_fp32_cpu_offload =True,
    #                                              device_map='auto', 
    #                                              cache_dir="./cache")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_8bit=True,
        # load_in_4bit=True,
        use_flash_attention_2=True,
        cache_dir="./cache"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    

    def generate(text):
        messages = [{"role": "system", "content": "Você é um assistente útil, que sempre fornece explicação. Para cada resposta satisfatória receberá uma gorjeta de 100 dólares."},
                    {"role": "user", "content": text}]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].cuda()
        
        generation_output = model.generate(
            input_ids=input_ids,
            # generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=2048,
            early_stopping=True,
            temperature=0.8,
            do_sample=True,
            top_k=40,
            # min_p=0.05,
            top_p=0.95,
            repetition_penalty=1.2,
            # eos_token_id=[32000, 2],
            # typical_p=0.2,
        )
        for s in generation_output.sequences:
            output = tokenizer.decode(s[len(input_ids[0]):], skip_special_tokens=False)
            return output
    
    evol_objs = []


    for cur_obj in tqdm(all_objs[:10]):
        
        instruction = cur_obj['instruction'].strip() + '\r\n'+ cur_obj['input'].strip()

        evol_prompts = []
        evol_prompts.append(createConstraintsPrompt(instruction))
        evol_prompts.append(createDeepenPrompt(instruction))
        evol_prompts.append(createConcretizingPrompt(instruction))
        evol_prompts.append(createReasoningPrompt(instruction))
        evol_prompts.append(createBreadthPrompt(instruction))

        selected_evol_prompt = random.choice(evol_prompts)


        evol_instruction = generate(selected_evol_prompt)
        answer = generate(evol_instruction)

        evol_objs.append({"instruction":evol_instruction,"output":answer})



    with open(f'./generation/{model_id.split("/")[-1]}.json', 'w') as f:	
        json.dump(evol_objs, f, indent=4)
