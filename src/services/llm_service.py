import json
from typing import Dict, List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from ..utils import config, decode_toon_to_json
from ..models.cv_model import CVSummary
from toon_python import encode, EncodeOptions, Delimiter

class LLMService:
    def __init__(self):
        config.validate_config()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=config.GOOGLE_API_KEY
        )
    
    def generate_cv_summary(self, cv_text: str, filename: str) -> CVSummary:
        """Gera um resumo estruturado do CV"""
        cv_data = encode({
            "filename": f"{filename}",
            "summary": "Resumo profissional do candidato",
            "key_skills": ["skill1", "skill2", "skill3"],
            "experience_years": "numero_de_anos_experiencia_ou_null",
            "education": "Formação acadêmica principal ou null",
            "contact_info": {
                "email": "email_se_encontrado_ou_null",
                "phone": "telefone_se_encontrado_ou_null",
                "location": "localização_se_encontrada_ou_null"
            }
        })

        prompt = f"""
        Analise o seguinte currículo e gere um resumo estruturado em TOON (Token-Oriented Object Notation):
        
        CV Text: {cv_text}
        
        Retorne APENAS um TOON válido com a seguinte estrutura:
        ```toon
        {cv_data}
        ```
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            print(f"Resposta LLM para {filename}: {response.content}")

            # Valida o TOON retornado
            toon_text = response.content.strip()
            if toon_text.startswith('```toon'):
                toon_text = toon_text[7:-3]
            elif toon_text.startswith('```'):
                toon_text = toon_text[3:-3]
            
            toon_object = decode_toon_to_json(toon_text.strip())
            summary_data = json.loads(toon_object)
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
        
        comparison_data = encode({
            "ranking": [
                {
                    "filename": "nome_arquivo",
                    "score": "numero_de_0_a_100",
                    "reasoning": "justificativa",
                    "strengths": ["ponto_forte_1", "ponto_forte_2"],
                    "weaknesses": ["ponto_fraco_1", "ponto_fraco_2"]
                }
            ],
            "summary": "Resumo da análise comparativa",
            "recommendation": "Recomendação baseada na query"
        })
        
        prompt = f"""
        Baseado nos seguintes candidatos e na query do usuário, faça uma análise comparativa:
        
        Query: {query}
        
        Candidatos:
        {summaries_text}
        
        Retorne APENAS um TOON válido com a seguinte estrutura:
        ```toon
        {comparison_data}
        ```
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            toon_text = response.content.strip()
            if toon_text.startswith('```toon'):
                toon_text = toon_text[7:-3]
            elif toon_text.startswith('```'):
                toon_text = toon_text[3:-3]
            
            toon_object = decode_toon_to_json(toon_text.strip())
            return json.loads(toon_object)
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
        
        answer_data = encode({
            "answer": "Resposta clara e objetiva à pergunta do usuário",
            "relevant_candidates": ["candidato1", "candidato2"],
            "confidence": "alto_medio_baixo"
        })
        
        prompt = f"""
        Com base nos seguintes currículos, responda à pergunta do usuário:
        
        Pergunta: {query}
        
        Candidatos:
        {summaries_text}
        
        Retorne APENAS um TOON válido com a seguinte estrutura:
        ```toon
        {answer_data}
        ```
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            toon_text = response.content.strip()
            if toon_text.startswith('```toon'):
                toon_text = toon_text[7:-3]
            elif toon_text.startswith('```'):
                toon_text = toon_text[3:-3]
            
            toon_object = decode_toon_to_json(toon_text.strip())
            answer_data = json.loads(toon_object)
            return answer_data.get("answer", "Erro ao processar resposta")
        except Exception as e:
            return f"Erro ao processar query: {str(e)}"

# Instância global do serviço
llm_service = LLMService()
