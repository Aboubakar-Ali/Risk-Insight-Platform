'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Loader2, Brain, TrendingUp, Target, Lightbulb, AlertTriangle, Clock, FileText, DollarSign } from 'lucide-react'

interface StrategicRecommendationsResponse {
  recommendations: {
    analysis_type: string
    ai_analysis: {
      recommendation: string
      score: number
      confidence: number
    }
    strategic_positioning: {
      sites_to_insure: Array<{
        site_id: number
        site_name: string
        recommendation: string
        reasoning: string
        risk_score: number
        building_value: number
      }>
      optimal_durations: Array<{
        site_id: number
        site_name: string
        optimal_duration: string
        reasoning: string
        risk_score: number
      }>
      key_clauses_by_site: Array<{
        site_id: number
        site_name: string
        base_clauses: string[]
        specific_clauses: string[]
        risk_score: number
      }>
      pricing_strategy: {
        strategy: string
        reasoning: string
        average_risk: number
        total_value: number
      }
    }
  }
  portfolio_data: {
    total_sites: number
    total_value: number
    total_premiums: number
    average_risk: number
  }
}

export default function StrategicRecommendationsDialog() {
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [recommendations, setRecommendations] = useState<StrategicRecommendationsResponse | null>(null)

  const getStrategicRecommendations = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/v1/ai-agent/strategic-recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          include_risk_analysis: true,
          include_cost_optimization: true,
          include_growth_opportunities: true,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setRecommendations(data)
      } else {
        console.error('Erreur lors de la récupération des recommandations')
      }
    } catch (error) {
      console.error('Erreur:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskLevel = (riskScore: number) => {
    if (riskScore < 10) return { level: 'Faible', color: 'bg-green-100 text-green-800' }
    if (riskScore < 25) return { level: 'Modéré', color: 'bg-yellow-100 text-yellow-800' }
    return { level: 'Élevé', color: 'bg-red-100 text-red-800' }
  }

  const getRiskColor = (riskScore: number) => {
    return getRiskLevel(riskScore).color
  }

  const getRecommendationColor = (recommendation: string) => {
    if (recommendation.includes('ASSURER')) return 'bg-green-100 text-green-800'
    if (recommendation.includes('CONDITIONS')) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2 bg-blue-600 hover:bg-blue-700 text-white">
          <Brain className="h-4 w-4" />
          Recommandations Stratégiques IA
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            Recommandations Stratégiques IA
          </DialogTitle>
        </DialogHeader>

        {!recommendations && !loading && (
          <div className="text-center py-8">
            <Button onClick={getStrategicRecommendations} className="gap-2">
              <Brain className="h-4 w-4" />
              Analyser le Portefeuille
            </Button>
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin" />
            <span className="ml-2">Analyse en cours...</span>
          </div>
        )}

        {recommendations && (
          <div className="space-y-6">
            {/* Analyse IA */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5" />
                  Analyse IA
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <Badge variant="outline">
                      Score: {recommendations.recommendations?.ai_analysis?.score || 75}/100
                    </Badge>
                    <Badge variant="outline">
                      Confiance: {Math.round((recommendations.recommendations?.ai_analysis?.confidence || 0.8) * 100)}%
                    </Badge>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm whitespace-pre-line">
                      {recommendations.recommendations?.ai_analysis?.recommendation || "Analyse en cours..."}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Stratégie de Tarification */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <DollarSign className="h-5 w-5" />
                  Stratégie de Tarification
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Stratégie recommandée:</span>
                    <Badge className={getRecommendationColor(recommendations.recommendations?.strategic_positioning?.pricing_strategy?.strategy || "PRIX ÉQUILIBRÉ")}>
                      {recommendations.recommendations?.strategic_positioning?.pricing_strategy?.strategy || "PRIX ÉQUILIBRÉ"}
                    </Badge>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-sm">
                      {recommendations.recommendations?.strategic_positioning?.pricing_strategy?.reasoning || "Analyse en cours..."}
                    </p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="font-medium">Risque moyen:</span> {recommendations.recommendations?.strategic_positioning?.pricing_strategy?.average_risk || 0}%
                    </div>
                    <div>
                      <span className="font-medium">Valeur totale:</span> {(recommendations.recommendations?.strategic_positioning?.pricing_strategy?.total_value || 0).toLocaleString()}€
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Sites à Assurer */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  Recommandations par Site
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {(recommendations.recommendations?.strategic_positioning?.sites_to_insure || []).map((site) => (
                    <div key={site.site_id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium">{site.site_name}</h4>
                        <Badge className={getRecommendationColor(site.recommendation)}>
                          {site.recommendation}
                        </Badge>
                      </div>
                                             <div className="grid grid-cols-2 gap-4 text-sm">
                         <div>
                           <span className="font-medium">Risque:</span> 
                           <Badge className={getRiskColor(site.risk_score)}>
                             {getRiskLevel(site.risk_score).level}
                           </Badge>
                         </div>
                         <div>
                           <span className="font-medium">Valeur:</span> {site.building_value.toLocaleString()}€
                         </div>
                       </div>
                      <div className="mt-2 text-sm text-gray-600">
                        {site.reasoning}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Durées Optimales */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Durées de Contrats Optimales
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                                     {(recommendations.recommendations?.strategic_positioning?.optimal_durations || []).map((duration) => (
                    <div key={duration.site_id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium">{duration.site_name}</h4>
                        <Badge variant="outline">
                          {duration.optimal_duration}
                        </Badge>
                      </div>
                                             <div className="grid grid-cols-2 gap-4 text-sm">
                         <div>
                           <span className="font-medium">Risque:</span> 
                           <Badge className={getRiskColor(duration.risk_score)}>
                             {getRiskLevel(duration.risk_score).level}
                           </Badge>
                         </div>
                         <div>
                           <span className="font-medium">Justification:</span>
                         </div>
                       </div>
                      <div className="mt-2 text-sm text-gray-600">
                        {duration.reasoning}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Clauses Clés */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Clauses Clés par Site
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                                     {(recommendations.recommendations?.strategic_positioning?.key_clauses_by_site || []).map((clause) => (
                    <div key={clause.site_id} className="border rounded-lg p-4">
                                             <div className="flex items-center justify-between mb-3">
                         <h4 className="font-medium">{clause.site_name}</h4>
                         <Badge className={getRiskColor(clause.risk_score)}>
                           Risque: {getRiskLevel(clause.risk_score).level}
                         </Badge>
                       </div>
                      
                      <div className="space-y-3">
                        <div>
                          <h5 className="font-medium text-sm mb-2">Clauses de Base:</h5>
                          <ul className="text-sm space-y-1">
                            {clause.base_clauses.map((baseClause, index) => (
                              <li key={index} className="flex items-start gap-2">
                                <span className="text-blue-600">•</span>
                                {baseClause}
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <div>
                          <h5 className="font-medium text-sm mb-2">Clauses Spécifiques:</h5>
                          <ul className="text-sm space-y-1">
                            {clause.specific_clauses.map((specificClause, index) => (
                              <li key={index} className="flex items-start gap-2">
                                <span className="text-orange-600">•</span>
                                {specificClause}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Statistiques du Portefeuille */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Statistiques du Portefeuille
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold">{recommendations.portfolio_data.total_sites}</div>
                    <div className="text-sm text-gray-600">Sites</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold">{recommendations.portfolio_data.total_value.toLocaleString()}€</div>
                    <div className="text-sm text-gray-600">Valeur Totale</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold">{recommendations.portfolio_data.total_premiums.toLocaleString()}€</div>
                    <div className="text-sm text-gray-600">Primes</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold">{Math.round(recommendations.portfolio_data.average_risk)}%</div>
                    <div className="text-sm text-gray-600">Risque Moyen</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
