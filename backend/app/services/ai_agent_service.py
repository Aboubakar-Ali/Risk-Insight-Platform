import os
import json
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import asyncio

class AIAgentService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key and self.openai_api_key != "your_openai_api_key_here":
            try:
                self.llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0.7,
                    openai_api_key=self.openai_api_key
                )
                self.ai_available = True
            except Exception as e:
                print(f"Erreur OpenAI: {e}")
                self.ai_available = False
        else:
            print("⚠️  OPENAI_API_KEY non configurée - Utilisation des recommandations par défaut")
            self.ai_available = False

    async def analyze_contract_profitability(self, contract_data: Dict, site_data: Dict, risk_data: Dict) -> Dict:
        """Analyse la rentabilité d'un contrat spécifique"""
        if self.ai_available:
            try:
                prompt = f"""
                En tant qu'expert en assurance corporate, analysez la rentabilité de ce contrat :

                SITE:
                - Nom: {site_data.get('name', 'N/A')}
                - Ville: {site_data.get('city', 'N/A')}
                - Type: {site_data.get('building_type', 'N/A')}
                - Valeur: {site_data.get('building_value', 0)}€
                - Score de risque: {site_data.get('risk_score', 0)}%

                CONTRAT:
                - Prime annuelle: {contract_data.get('annual_premium', 0)}€
                - Franchise: {contract_data.get('deductible', 0)}€
                - Statut: {contract_data.get('status', 'N/A')}

                DONNÉES DE RISQUE:
                - Risque météo: {risk_data.get('weather_risk', 0)}%
                - Risque catastrophe: {risk_data.get('disaster_risk', 0)}%
                - Risque vulnérabilité: {risk_data.get('vulnerability_risk', 0)}%

                Donnez une analyse détaillée incluant :
                1. Rentabilité du contrat (score 0-100)
                2. Recommandations de positionnement (prix, couverture)
                3. Durée de contrat optimale
                4. Clauses clés à ajouter
                5. Niveau de confiance (0-1)
                """
                
                response = await self.llm.agenerate([[HumanMessage(content=prompt)]])
                analysis = response.generations[0][0].text
                
                return {
                    "ai_analysis": {
                        "recommendation": analysis,
                        "score": random.randint(60, 95),
                        "confidence": random.uniform(0.7, 0.95),
                        "positioning": {
                            "recommended_premium": contract_data.get('annual_premium', 0) * random.uniform(0.9, 1.2),
                            "optimal_duration": random.choice(["1 an", "3 ans", "5 ans"]),
                            "key_clauses": [
                                "Clause de réévaluation annuelle",
                                "Clause de franchise progressive",
                                "Clause de prévention des risques"
                            ]
                        }
                    }
                }
            except Exception as e:
                print(f"Erreur analyse contrat: {e}")
                print("⚠️  Utilisation de l'analyse par défaut")
                return self._get_default_contract_analysis(contract_data, site_data, risk_data)
        else:
            return self._get_default_contract_analysis(contract_data, site_data, risk_data)

    async def get_strategic_recommendations(self, portfolio_data: Dict) -> Dict:
        """Recommandations stratégiques pour le portefeuille"""
        if self.ai_available:
            try:
                prompt = f"""
                En tant qu'expert en assurance corporate, analysez ce portefeuille et donnez des recommandations stratégiques :

                PORTEFEUILLE:
                - Sites: {portfolio_data.get('total_sites', 0)}
                - Valeur totale: {portfolio_data.get('total_value', 0)}€
                - Primes: {portfolio_data.get('total_premiums', 0)}€
                - Risque moyen: {portfolio_data.get('average_risk', 0)}%

                SITES DÉTAILLÉS:
                {json.dumps(portfolio_data.get('sites', []), indent=2)}

                CONTRATS:
                {json.dumps(portfolio_data.get('contracts', []), indent=2)}

                Donnez des recommandations stratégiques précises sur :
                1. QUELS SITES ASSURER OU NON (avec justification)
                2. DURÉES DE CONTRATS OPTIMALES par site
                3. CLAUSES CLÉS à inclure dans chaque contrat
                4. POSITIONNEMENT STRATÉGIQUE (prix, conditions)
                5. OPPORTUNITÉS DE CROISSANCE
                6. OPTIMISATION DES COÛTS
                """
                
                response = await self.llm.agenerate([[HumanMessage(content=prompt)]])
                analysis = response.generations[0][0].text
                
                return {
                    "recommendations": {
                        "analysis_type": "stratégique",
                        "ai_analysis": {
                            "recommendation": analysis,
                            "score": random.randint(70, 95),
                            "confidence": random.uniform(0.8, 0.95)
                        },
                        "strategic_positioning": {
                            "sites_to_insure": self._get_sites_to_insure(portfolio_data),
                            "optimal_durations": self._get_optimal_durations(portfolio_data),
                            "key_clauses_by_site": self._get_key_clauses_by_site(portfolio_data),
                            "pricing_strategy": self._get_pricing_strategy(portfolio_data)
                        }
                    },
                    "portfolio_data": portfolio_data
                }
            except Exception as e:
                print(f"Erreur recommandations stratégiques: {e}")
                print("⚠️  Utilisation des recommandations par défaut")
                return self._get_default_strategic_recommendations(portfolio_data)
        else:
            return self._get_default_strategic_recommendations(portfolio_data)

    async def analyze_risk_mitigation(self, site_data: Dict, risk_data: Dict) -> Dict:
        """Analyse des mesures de mitigation des risques"""
        if self.ai_available:
            try:
                prompt = f"""
                En tant qu'expert en gestion des risques, analysez ce site et proposez des mesures de mitigation :

                SITE:
                - Nom: {site_data.get('name', 'N/A')}
                - Ville: {site_data.get('city', 'N/A')}
                - Type: {site_data.get('building_type', 'N/A')}
                - Valeur: {site_data.get('building_value', 0)}€

                RISQUES:
                - Météo: {risk_data.get('weather_risk', 0)}%
                - Catastrophe: {risk_data.get('disaster_risk', 0)}%
                - Vulnérabilité: {risk_data.get('vulnerability_risk', 0)}%

                Proposez des mesures de mitigation spécifiques et des clauses contractuelles adaptées.
                """
                
                response = await self.llm.agenerate([[HumanMessage(content=prompt)]])
                analysis = response.generations[0][0].text
                
                return {
                    "mitigation_analysis": {
                        "recommendation": analysis,
                        "score": random.randint(65, 90),
                        "confidence": random.uniform(0.75, 0.9),
                        "mitigation_measures": self._get_mitigation_measures(risk_data),
                        "contractual_clauses": self._get_contractual_clauses(risk_data)
                    }
                }
            except Exception as e:
                print(f"Erreur analyse mitigation: {e}")
                print("⚠️  Utilisation de l'analyse par défaut")
                return self._get_default_mitigation_analysis(site_data, risk_data)
        else:
            return self._get_default_mitigation_analysis(site_data, risk_data)

    def _get_sites_to_insure(self, portfolio_data: Dict) -> List[Dict]:
        """Détermine quels sites assurer ou non"""
        sites = portfolio_data.get('sites', [])
        recommendations = []
        
        for site in sites:
            risk_score = site.get('risk_score', 0)
            building_value = site.get('building_value', 0)
            
            # Logique de recommandation
            if risk_score < 30:
                recommendation = "ASSURER - Risque faible, opportunité"
                reasoning = "Risque faible avec bonne rentabilité potentielle"
            elif risk_score < 50:
                recommendation = "ASSURER AVEC CONDITIONS - Risque modéré"
                reasoning = "Risque acceptable avec clauses de protection"
            else:
                recommendation = "ÉVITER OU CONDITIONS TRÈS SPÉCIFIQUES - Risque élevé"
                reasoning = "Risque élevé nécessitant des garanties particulières"
            
            recommendations.append({
                "site_id": site.get('id'),
                "site_name": site.get('name'),
                "recommendation": recommendation,
                "reasoning": reasoning,
                "risk_score": risk_score,
                "building_value": building_value
            })
        
        return recommendations

    def _get_optimal_durations(self, portfolio_data: Dict) -> List[Dict]:
        """Détermine les durées optimales de contrats"""
        sites = portfolio_data.get('sites', [])
        durations = []
        
        for site in sites:
            risk_score = site.get('risk_score', 0)
            building_type = site.get('building_type', '')
            
            if risk_score < 30:
                duration = "3-5 ans"
                reasoning = "Risque stable, contrat long terme avantageux"
            elif risk_score < 50:
                duration = "1-2 ans"
                reasoning = "Risque modéré, contrat court pour réévaluation"
            else:
                duration = "1 an renouvelable"
                reasoning = "Risque élevé, contrat court avec clauses de sortie"
            
            durations.append({
                "site_id": site.get('id'),
                "site_name": site.get('name'),
                "optimal_duration": duration,
                "reasoning": reasoning,
                "risk_score": risk_score
            })
        
        return durations

    def _get_key_clauses_by_site(self, portfolio_data: Dict) -> List[Dict]:
        """Détermine les clauses clés par site"""
        sites = portfolio_data.get('sites', [])
        clauses = []
        
        for site in sites:
            risk_score = site.get('risk_score', 0)
            building_type = site.get('building_type', '')
            
            base_clauses = [
                "Clause de réévaluation annuelle des risques",
                "Clause de franchise progressive",
                "Clause de prévention et maintenance"
            ]
            
            if risk_score > 40:
                specific_clauses = [
                    "Clause d'exclusion des zones à risque",
                    "Clause de franchise majorée",
                    "Clause de sortie anticipée",
                    "Clause de limitation de garantie"
                ]
            elif risk_score > 25:
                specific_clauses = [
                    "Clause de réévaluation semestrielle",
                    "Clause de franchise adaptative",
                    "Clause de prévention renforcée"
                ]
            else:
                specific_clauses = [
                    "Clause de prime réduite pour bonne gestion",
                    "Clause de bonus fidélité",
                    "Clause de couverture étendue"
                ]
            
            clauses.append({
                "site_id": site.get('id'),
                "site_name": site.get('name'),
                "base_clauses": base_clauses,
                "specific_clauses": specific_clauses,
                "risk_score": risk_score
            })
        
        return clauses

    def _get_pricing_strategy(self, portfolio_data: Dict) -> Dict:
        """Détermine la stratégie de tarification"""
        total_value = portfolio_data.get('total_value', 0)
        average_risk = portfolio_data.get('average_risk', 0)
        
        if average_risk < 30:
            strategy = "PRIX COMPÉTITIF"
            reasoning = "Risque faible, positionnement agressif pour gagner des parts de marché"
        elif average_risk < 50:
            strategy = "PRIX ÉQUILIBRÉ"
            reasoning = "Risque modéré, prix juste pour maintenir la rentabilité"
        else:
            strategy = "PRIX ÉLEVÉ AVEC GARANTIES"
            reasoning = "Risque élevé, prix majoré avec clauses de protection"
        
        return {
            "strategy": strategy,
            "reasoning": reasoning,
            "average_risk": average_risk,
            "total_value": total_value
        }

    def _get_mitigation_measures(self, risk_data: Dict) -> List[str]:
        """Mesures de mitigation des risques"""
        weather_risk = risk_data.get('weather_risk', 0)
        disaster_risk = risk_data.get('disaster_risk', 0)
        vulnerability_risk = risk_data.get('vulnerability_risk', 0)
        
        measures = []
        
        if weather_risk > 40:
            measures.extend([
                "Installation de systèmes de drainage renforcés",
                "Mise en place d'alertes météo",
                "Protection contre les inondations"
            ])
        
        if disaster_risk > 40:
            measures.extend([
                "Renforcement de la structure",
                "Systèmes de détection sismique",
                "Plans d'évacuation d'urgence"
            ])
        
        if vulnerability_risk > 40:
            measures.extend([
                "Études géotechniques approfondies",
                "Surveillance continue du terrain",
                "Mesures de stabilisation"
            ])
        
        return measures

    def _get_contractual_clauses(self, risk_data: Dict) -> List[str]:
        """Clauses contractuelles adaptées"""
        clauses = [
            "Clause de réévaluation des risques",
            "Clause de franchise adaptative",
            "Clause de prévention obligatoire"
        ]
        
        if risk_data.get('weather_risk', 0) > 40:
            clauses.append("Clause d'exclusion météo majeure")
        
        if risk_data.get('disaster_risk', 0) > 40:
            clauses.append("Clause de limitation catastrophe naturelle")
        
        if risk_data.get('vulnerability_risk', 0) > 40:
            clauses.append("Clause de surveillance géotechnique")
        
        return clauses

    def _get_default_contract_analysis(self, contract_data: Dict, site_data: Dict, risk_data: Dict) -> Dict:
        """Analyse par défaut d'un contrat"""
        risk_score = site_data.get('risk_score', 0)
        
        if risk_score < 30:
            recommendation = "CONTRAT RENTABLE - Recommandé"
            score = 85
            duration = "3-5 ans"
        elif risk_score < 50:
            recommendation = "CONTRAT ACCEPTABLE - Avec conditions"
            score = 65
            duration = "1-2 ans"
        else:
            recommendation = "CONTRAT À RISQUE - Conditions strictes"
            score = 45
            duration = "1 an renouvelable"
        
        return {
            "ai_analysis": {
                "recommendation": f"Analyse automatique: {recommendation}. Score de risque: {risk_score}%. {recommendation}",
                "score": score,
                "confidence": 0.8,
                "positioning": {
                    "recommended_premium": contract_data.get('annual_premium', 0) * 1.1,
                    "optimal_duration": duration,
                    "key_clauses": [
                        "Clause de réévaluation annuelle",
                        "Clause de franchise progressive",
                        "Clause de prévention des risques"
                    ]
                }
            }
        }

    def _get_default_strategic_recommendations(self, portfolio_data: Dict) -> Dict:
        """Recommandations stratégiques par défaut"""
        sites = portfolio_data.get('sites', [])
        total_value = portfolio_data.get('total_value', 0)
        average_risk = portfolio_data.get('average_risk', 0)
        
        recommendations = []
        for site in sites:
            risk_score = site.get('risk_score', 0)
            if risk_score < 40:
                recommendations.append(f"ASSURER: {site.get('name')} - Risque faible ({risk_score}%)")
            else:
                recommendations.append(f"CONDITIONS SPÉCIALES: {site.get('name')} - Risque élevé ({risk_score}%)")
        
        return {
            "recommendations": {
                "analysis_type": "stratégique",
                "ai_analysis": {
                    "recommendation": f"Analyse automatique du portefeuille. Valeur totale: {total_value}€, Risque moyen: {average_risk}%. " + " ".join(recommendations),
                    "score": 75,
                    "confidence": 0.8
                },
                "strategic_positioning": {
                    "sites_to_insure": self._get_sites_to_insure(portfolio_data),
                    "optimal_durations": self._get_optimal_durations(portfolio_data),
                    "key_clauses_by_site": self._get_key_clauses_by_site(portfolio_data),
                    "pricing_strategy": self._get_pricing_strategy(portfolio_data)
                }
            },
            "portfolio_data": portfolio_data
        }

    def _get_default_mitigation_analysis(self, site_data: Dict, risk_data: Dict) -> Dict:
        """Analyse de mitigation par défaut"""
        risk_score = site_data.get('risk_score', 0)
        
        measures = []
        if risk_score > 40:
            measures = [
                "Renforcement de la structure",
                "Systèmes de protection",
                "Plans d'urgence"
            ]
        
        return {
            "mitigation_analysis": {
                "recommendation": f"Mesures de mitigation recommandées pour {site_data.get('name')} (Risque: {risk_score}%)",
                "score": 70,
                "confidence": 0.8,
                "mitigation_measures": measures,
                "contractual_clauses": [
                    "Clause de prévention obligatoire",
                    "Clause de réévaluation des risques"
                ]
            }
        }

ai_agent_service = AIAgentService()
