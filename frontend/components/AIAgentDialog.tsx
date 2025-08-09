'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Loader2, Brain, TrendingUp, Shield, AlertTriangle } from 'lucide-react'

interface AIAnalysis {
  summary: string
  recommendation: string
  justification: string
  actions: string[]
  score: number
  confidence: number
}

interface ContractAnalysis {
  analysis_type: string
  ai_analysis: AIAnalysis
  raw_response: string
}

interface AIAgentDialogProps {
  siteId?: number
  contractId?: number
  onAnalysisComplete?: (analysis: ContractAnalysis) => void
}

export default function AIAgentDialog({ siteId, contractId, onAnalysisComplete }: AIAgentDialogProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [analysis, setAnalysis] = useState<ContractAnalysis | null>(null)
  const [error, setError] = useState<string | null>(null)

  const analyzeContract = async () => {
    if (!siteId || !contractId) {
      setError('Site et contrat requis pour l\'analyse')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/v1/ai-agent/analyze-contract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site_id: siteId,
          contract_id: contractId
        })
      })

      if (!response.ok) {
        throw new Error('Erreur lors de l\'analyse')
      }

      const data = await response.json()
      setAnalysis(data.analysis)
      onAnalysisComplete?.(data.analysis)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue')
    } finally {
      setIsLoading(false)
    }
  }

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation.toUpperCase()) {
      case 'ACCEPTER':
        return 'bg-green-100 text-green-800'
      case 'NÉGOCIER':
        return 'bg-yellow-100 text-yellow-800'
      case 'REFUSER':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2 bg-green-600 hover:bg-green-700 text-white">
          <Brain className="h-4 w-4" />
          Analyser Contrat IA
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            Agent IA - Analyse de Contrat
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {!analysis && !isLoading && (
            <div className="text-center py-8">
              <Brain className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <p className="text-gray-600 mb-4">
                L'agent IA analysera la rentabilité du contrat en tenant compte des risques identifiés.
              </p>
              <Button onClick={analyzeContract} disabled={!siteId || !contractId}>
                Lancer l'analyse IA
              </Button>
            </div>
          )}

          {isLoading && (
            <div className="text-center py-8">
              <Loader2 className="h-8 w-8 mx-auto animate-spin mb-4" />
              <p>L'agent IA analyse le contrat...</p>
            </div>
          )}

          {error && (
            <Card className="border-red-200 bg-red-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-red-800">
                  <AlertTriangle className="h-5 w-5" />
                  Erreur d'analyse
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-red-700">{error}</p>
              </CardContent>
            </Card>
          )}

          {analysis && (
            <div className="space-y-4">
              {/* Résumé de l'analyse */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    Analyse de Rentabilité
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Score de Rentabilité</p>
                      <p className={`text-2xl font-bold ${getScoreColor(analysis.ai_analysis.score)}`}>
                        {analysis.ai_analysis.score}/100
                      </p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Recommandation</p>
                      <Badge className={getRecommendationColor(analysis.ai_analysis.recommendation)}>
                        {analysis.ai_analysis.recommendation}
                      </Badge>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Confiance IA</p>
                      <p className="text-lg font-semibold text-blue-600">
                        {Math.round(analysis.ai_analysis.confidence * 100)}%
                      </p>
                    </div>
                  </div>
                  <p className="text-gray-700">{analysis.ai_analysis.summary}</p>
                </CardContent>
              </Card>

              {/* Justification */}
              <Card>
                <CardHeader>
                  <CardTitle>Justification</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700">{analysis.ai_analysis.justification}</p>
                </CardContent>
              </Card>

              {/* Actions recommandées */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="h-5 w-5" />
                    Actions Recommandées
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {analysis.ai_analysis.actions.map((action, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700">{action}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Réponse brute de l'IA */}
              <Card>
                <CardHeader>
                  <CardTitle>Analyse Détaillée IA</CardTitle>
                  <CardDescription>Réponse complète de l'agent IA</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                      {analysis.raw_response}
                    </pre>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
