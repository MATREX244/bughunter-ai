import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

class AIEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def analyze_recon_data(self, recon_data):
        prompt = f"""
        Você é um Bug Hunter sênior com 15 anos de experiência.
        Analise os seguintes dados de reconhecimento e identifique os alvos mais promissores para exploração.
        Foque em vulnerabilidades de impacto Crítico, Alto ou Médio.
        
        DADOS DE RECONHECIMENTO:
        {json.dumps(recon_data, indent=2)}
        
        Responda em formato JSON com os seguintes campos:
        - reasoning: Sua análise detalhada.
        - prioritized_targets: Lista de objetos com 'url', 'reason' e 'suggested_tool'.
        """
        
        response = await self.model.generate_content_async(prompt)
        try:
            # Tenta extrair JSON da resposta
            content = response.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except:
            return {"reasoning": response.text, "prioritized_targets": []}

    async def decide_next_action(self, current_state):
        prompt = f"""
        Como um expert em segurança ofensiva, decida o próximo passo com base no estado atual:
        {json.dumps(current_state, indent=2)}
        
        Considere ferramentas como: subfinder, nmap, nuclei, sqlmap, dalfox, ffuf.
        
        Responda em JSON:
        - reasoning: Por que esta ação?
        - action: O comando exato a ser executado ou a ferramenta a usar.
        """
        response = await self.model.generate_content_async(prompt)
        try:
            content = response.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except:
            return {"reasoning": response.text, "action": "wait"}

    async def analyze_result(self, command_output):
        prompt = f"""
        Analise o output desta ferramenta de segurança e identifique vulnerabilidades reais.
        Ignore informativos e severidade baixa.
        
        OUTPUT:
        {command_output}
        
        Responda em JSON:
        - findings: Lista de vulnerabilidades encontradas (título, severidade, url, descrição, poc).
        - requires_follow_up: booleano indicando se precisa de mais testes.
        """
        response = await self.model.generate_content_async(prompt)
        try:
            content = response.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except:
            return {"findings": [], "requires_follow_up": False}
