import re
from typing import Tuple, List
from src.llm import load_client, CHAT_MODEL
from src.agent.prompts import REACT_SYSTEM_PROMPT
from src.agent.tools import TOOLS, execute_tool

def react_agent(task: str, context_code: str = "") -> Tuple[str, List[str]]:
    """
    Roda um agente interativo base ReAct construindo o raciocínio conversacionalmente.
    Params:
      task - A instrução base geradora da documentação
      context_code - (opcional) O texto/codigo estático originado do Streamlit uploader
    Returns:
      (document_string_final, history_of_logs_list)
    """
    client = load_client()
    
    tool_names = ", ".join(TOOLS.keys())
    tool_desc = "\n".join([t["description"] for t in TOOLS.values()])
    
    system_inst = REACT_SYSTEM_PROMPT.format(tool_names=tool_names, tool_descriptions=tool_desc)
    
    # Inicia prompt
    question = f"Tarefa Principal: {task}\n\nCódigo de Contexto Suplementar recebido no Frontend:\n```python\n{context_code}\n```"
    prompt = f"{system_inst}\n\nQuestion: {question}\n"
    
    log = []
    max_steps = 7  # Prevenir loops infindáveis em Tier Free e queimar tokens
    
    for _ in range(max_steps):
        # Inferência
        resp = client.models.generate_content(
            model=CHAT_MODEL,
            contents=prompt
        )
        
        output = getattr(resp, "text", "").strip()
        log.append(f"🤖 LLM Turn:\n{output}\n")
        
        # Concatena log no raciocinio central para o próximo turno
        prompt += f"{output}\n"
        
        # Checa conclusão
        if "Final Answer:" in output:
            final_answer = output.split("Final Answer:")[-1].strip()
            return final_answer, log
            
        # Parseio Reativo de Regex
        action_match = re.search(r"Action:\s*(.*?)(?:\n|$)", output)
        action_input_match = re.search(r"Action Input:\s*(.*?)(?:\n|$)", output)
        
        if action_match and action_input_match:
            action = action_match.group(1).strip()
            action_input = action_input_match.group(1).strip()
            
            # Action!
            observation = execute_tool(action, action_input)
            obs_text = f"Observation: {observation}"
            log.append(f"🛠️ Tool Execution:\n{obs_text}\n")
            
            # Retorna para LLM a observação final do print do Sistema
            prompt += f"{obs_text}\n"
        else:
            # LLM Alucinou ou quebrou formatação, força-o a pensar na falha
            prompt += "Observation: Formato inválido! Você não preencheu 'Action:' ou 'Action Input:'. Siga o gabarito ou chame 'Final Answer:'.\n"

    return "Erro: O agente falhou em processar e abortou antes do loop infindável.", log
