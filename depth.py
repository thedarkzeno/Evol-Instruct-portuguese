base_instruction = "Quero que você atue como um Reescritor de Prompt.\r\n \
Seu objetivo é reescrever um determinado prompt em uma versão mais complexa para tornar os famosos sistemas de IA (por exemplo, chatgpt e GPT4) um pouco mais difíceis de manusear.\r\n \
Mas a solicitação reescrita deve ser razoável e deve ser compreendida e respondida por humanos.\r\n \
Sua reescrita não pode omitir as partes não textuais, como a tabela e o código em #Prompt Dado#:. Além disso, não omita a entrada em #Prompt Dado#. \r\n \
Você DEVE complicar o prompt fornecido usando o seguinte método: \r\n\
{} \r\n\
Você deve tentar o seu melhor para não tornar o #Prompt Reescrito# detalhado, #Prompt Reescrito# só pode adicionar 10 a 20 palavras em #Prompt Dado#. \r\n\
'#Prompt Dado#', '#Prompt Reescrito#', 'prompt dado' e 'prompt reescrito' não podem aparecer em #Prompt Reescrito#\r\n"


def createConstraintsPrompt(instruction):
	prompt = base_instruction.format("Por favor, adicione mais uma restrição/requisito em #Prompt Dado#'")
	prompt += "#Prompt Dado#: \r\n {} \r\n".format(instruction)
	prompt += "#Prompt Reescrito#:\r\n"
	return prompt

def createDeepenPrompt(instruction):
	prompt = base_instruction.format("Se #Prompt Dado# contiver perguntas sobre determinados assuntos, a profundidade e a amplitude da pergunta poderão ser aumentadas.")
	prompt += "#Prompt Dado#: \r\n {} \r\n".format(instruction)
	prompt += "#Prompt Reescrito#:\r\n"
	return prompt

def createConcretizingPrompt(instruction):
	prompt = base_instruction.format("Substitua conceitos gerais por conceitos mais específicos.")
	prompt += "#Prompt Dado#: \r\n {} \r\n".format(instruction)
	prompt += "#Prompt Reescrito#:\r\n"
	return prompt


def createReasoningPrompt(instruction):
	prompt = base_instruction.format("Se #Prompt Dado# puder ser resolvido com apenas alguns processos de pensamento simples, você poderá reescrevê-lo para solicitar explicitamente o raciocínio em múltiplas etapas.")
	prompt += "#Prompt Dado#: \r\n {} \r\n".format(instruction)
	prompt += "#Prompt Reescrito#:\r\n"
	return prompt
