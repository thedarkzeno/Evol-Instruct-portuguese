base_instruction = "Quero que você atue como um Criador de Prompt.\r\n\
Seu objetivo é inspirar-se no #Prompt Dado# para criar um novo prompt.\r\n\
Este novo prompt deve pertencer ao mesmo domínio que o #Prompt Dado#, mas será ainda mais raro.\r\n\
O COMPRIMENTO e a complexidade do #Prompt Criado# devem ser semelhantes aos do #Prompt Dado#.\r\n\
O #Prompt Criado# deve ser razoável e deve ser compreendido e respondido por humanos.\r\n\
'#Prompt Dado#', '#Prompt Criado#', 'prompt dado' e 'prompt criado' não podem aparecer em #Prompt Criado#\r\n"



def createBreadthPrompt(instruction):
	prompt = base_instruction
	prompt += "#Prompt Dado#: \r\n {} \r\n".format(instruction)
	prompt += "#Prompt Criado#:\r\n"
	return prompt
