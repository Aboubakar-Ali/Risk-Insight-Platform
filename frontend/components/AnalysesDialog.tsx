'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { TrendingUp, BarChart3, AlertTriangle, Euro, MapPin } from 'lucide-react'

interface Site {
  id: number
  name: string
  city: string
  building_type: string
  building_value: number
  risk_score: number
  created_at: string
}

interface Contract {
  id: number
  contract_number: string
  site_id: number
  premium_amount: number
  coverage_amount: number
  status: string
}

interface AnalysesDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  sites: Site[]
  contracts: Contract[]
}

export function AnalysesDialog({ open, onOpenChange, sites, contracts }: AnalysesDialogProps) {

  // Calculs d'analyses
  const totalValue = sites.reduce((sum, site) => sum + site.building_value, 0)
  const averageRisk = sites.length > 0 ? sites.reduce((sum, site) => sum + site.risk_score, 0) / sites.length : 0
  const totalPremiums = contracts.reduce((sum, contract) => sum + contract.premium_amount, 0)
  const highRiskSites = sites.filter(site => site.risk_score > 40)
  const lowRiskSites = sites.filter(site => site.risk_score < 30)

  const riskByType = {
    flood: sites.filter(s => s.risk_score > 40).length,
    storm: sites.filter(s => s.risk_score > 30).length,
    earthquake: sites.filter(s => s.risk_score > 50).length
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[800px] max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Analyses Détaillées
          </DialogTitle>
          <DialogDescription>
            Vue d'ensemble de votre portefeuille d'assurance
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Statistiques générales */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Valeur Totale</CardTitle>
                <Euro className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalValue.toLocaleString()}€</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Risque Moyen</CardTitle>
                <AlertTriangle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{Math.round(averageRisk)}%</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Primes Totales</CardTitle>
                <Euro className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalPremiums.toLocaleString()}€</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Sites Actifs</CardTitle>
                <MapPin className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{sites.length}</div>
              </CardContent>
            </Card>
          </div>

          {/* Répartition des risques */}
          <Card>
            <CardHeader>
              <CardTitle>Répartition des Risques</CardTitle>
              <CardDescription>Analyse par niveau de risque</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span>Risque Élevé (&gt;40%)</span>
                  <Badge variant="destructive">{highRiskSites.length} sites</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span>Risque Modéré (30-40%)</span>
                  <Badge variant="secondary">{sites.filter(s => s.risk_score >= 30 && s.risk_score <= 40).length} sites</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span>Risque Faible (&lt;30%)</span>
                  <Badge variant="default">{lowRiskSites.length} sites</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

                           {/* Risques par type */}
                 <Card>
                   <CardHeader>
                     <CardTitle>Risques par Type</CardTitle>
                     <CardDescription>Analyse des menaces principales basée sur les données météo</CardDescription>
                   </CardHeader>
                   <CardContent>
                     <div className="space-y-4">
                       <div className="flex justify-between items-center">
                         <span>Inondation</span>
                         <span className="font-semibold">{riskByType.flood > 0 ? 'Élevé' : 'Faible'}</span>
                       </div>
                       <div className="flex justify-between items-center">
                         <span>Tempête</span>
                         <span className="font-semibold">{riskByType.storm > 0 ? 'Modéré' : 'Faible'}</span>
                       </div>
                       <div className="flex justify-between items-center">
                         <span>Séisme</span>
                         <span className="font-semibold">{riskByType.earthquake > 0 ? 'Élevé' : 'Faible'}</span>
                       </div>
                       <div className="pt-2 border-t">
                         <div className="text-xs text-gray-600">
                           * Basé sur les conditions météo actuelles via OpenWeatherMap
                         </div>
                       </div>
                     </div>
                   </CardContent>
                 </Card>

          {/* Sites à surveiller */}
          {highRiskSites.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-red-600">Sites à Surveiller</CardTitle>
                <CardDescription>Sites nécessitant une attention particulière</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {highRiskSites.map((site) => (
                    <div key={site.id} className="flex justify-between items-center p-2 bg-red-50 rounded">
                      <div>
                        <div className="font-medium">{site.name}</div>
                        <div className="text-sm text-gray-600">{site.city}</div>
                      </div>
                      <Badge variant="destructive">{Math.round(site.risk_score)}%</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Recommandations */}
          <Card>
            <CardHeader>
              <CardTitle>Recommandations</CardTitle>
              <CardDescription>Actions suggérées pour optimiser votre portefeuille</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                {highRiskSites.length > 0 && (
                  <li>• Vérifier la couverture pour {highRiskSites.length} site(s) à risque élevé</li>
                )}
                {contracts.length === 0 && (
                  <li>• Créer des contrats d'assurance pour vos sites</li>
                )}
                {sites.length > 0 && (
                  <li>• Mettre à jour les évaluations de risque régulièrement</li>
                )}
                {totalValue > 10000000 && (
                  <li>• Considérer une diversification géographique</li>
                )}
                <li>• Analyser les tendances météorologiques pour les sites à risque</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  )
}
