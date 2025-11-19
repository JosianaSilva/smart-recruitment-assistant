import json
from typing import Dict, List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from ..utils.config import config
from ..models.cv_model import CVSummary

class LLMService:
    def __init__(self):
        config.validate_config()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=config.GOOGLE_API_KEY
        )
    
    def generate_cv_summary(self, cv_text: str, filename: str) -> CVSummary:
        """Gera um resumo estruturado do CV"""
        prompt = f"""
        Analise o seguinte currículo e gere um resumo estruturado em JSON:
        
        CV Text: {cv_text}
        
        Retorne APENAS um JSON válido com a seguinte estrutura:
        {{
            "filename": "{filename}",
            "summary": "Resumo profissional do candidato",
            "key_skills": ["skill1", "skill2", "skill3"],
            "experience_years": numero_de_anos_experiencia_ou_null,
            "education": "Formação acadêmica principal ou null",
            "contact_info": {{
                "email": "email_se_encontrado_ou_null",
                "phone": "telefone_se_encontrado_ou_null",
                "location": "localização_se_encontrada_ou_null"
            }}
        }}
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            # Valida o JSON retornado
            json_text = response.content.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            summary_data = json.loads(json_text)
            return CVSummary(**summary_data)
        except Exception as e:
            return CVSummary(
                filename=filename,
                summary=f"Erro ao gerar resumo: {str(e)}",
                key_skills=[],
                experience_years=None,
                education=None,
                contact_info={}
            )
    
    def compare_candidates(self, cv_summaries: List[CVSummary], query: str) -> Dict[str, Any]:
        """Compara candidatos com base na query"""
        summaries_text = "\n\n".join([
            f"Candidato: {summary.filename}\n"
            f"Resumo: {summary.summary}\n"
            f"Skills: {', '.join(summary.key_skills)}\n"
            f"Experiência: {summary.experience_years or 'Não informado'} anos\n"
            f"Formação: {summary.education or 'Não informado'}"
            for summary in cv_summaries
        ])
        
        prompt = f"""
        Baseado nos seguintes candidatos e na query do usuário, faça uma análise comparativa:
        
        Query: {query}
        
        Candidatos:
        {summaries_text}
        
        Retorne APENAS um JSON válido com:
        {{
            "ranking": [
                {{
                    "filename": "nome_arquivo",
                    "score": numero_de_0_a_100,
                    "reasoning": "justificativa",
                    "strengths": ["ponto_forte_1", "ponto_forte_2"],
                    "weaknesses": ["ponto_fraco_1", "ponto_fraco_2"]
                }}
            ],
            "summary": "Resumo da análise comparativa",
            "recommendation": "Recomendação baseada na query"
        }}
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            json_text = response.content.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            return json.loads(json_text)
        except Exception as e:
            return {
                "ranking": [],
                "summary": f"Erro na análise: {str(e)}",
                "recommendation": "Não foi possível gerar recomendação"
            }
    
    def answer_query(self, cv_summaries: List[CVSummary], query: str) -> str:
        """Responde query específica sobre os CVs"""
        summaries_text = "\n\n".join([
            f"Candidato: {summary.filename}\n"
            f"Resumo: {summary.summary}\n"
            f"Skills: {', '.join(summary.key_skills)}\n"
            f"Experiência: {summary.experience_years or 'Não informado'} anos\n"
            f"Formação: {summary.education or 'Não informado'}"
            for summary in cv_summaries
        ])
        
        prompt = f"""
        Com base nos seguintes currículos, responda à pergunta do usuário:
        
        Pergunta: {query}
        
        Candidatos:
        {summaries_text}
        
        Forneça uma resposta clara e objetiva.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"Erro ao processar query: {str(e)}"

# Instância global do serviço
llm_service = LLMService()
