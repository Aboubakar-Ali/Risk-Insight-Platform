'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Building2, TrendingUp, AlertTriangle, MapPin, Euro, Calendar } from 'lucide-react'
import { AddSiteDialog } from '@/components/AddSiteDialog'
import { ImportCSVDialog } from '@/components/ImportCSVDialog'
import { AnalysesDialog } from '@/components/AnalysesDialog'
import { SiteDetailsDialog } from '@/components/SiteDetailsDialog'
import AIAgentDialog from '@/components/AIAgentDialog'
import StrategicRecommendationsDialog from '@/components/StrategicRecommendationsDialog'

interface Site {
  id: number
  name: string
  address: string
  city: string
  postal_code: string
  country: string
  latitude: number
  longitude: number
  building_type: string
  building_value: number
  surface_area: number
  construction_year: number
  notes: string
  risk_score: number
  last_risk_update: string
  created_at: string
  updated_at: string
  contracts: Contract[]
}

interface Contract {
  id: number
  annual_premium: number
  deductible: number
  coverage_type: string
  status: string
  start_date: string
  end_date: string
  site_id: number
}

export default function Home() {
  const [sites, setSites] = useState<Site[]>([])
  const [contracts, setContracts] = useState<Contract[]>([])
  const [selectedSite, setSelectedSite] = useState<Site | null>(null)
  const [isAddSiteOpen, setIsAddSiteOpen] = useState(false)
  const [isImportOpen, setIsImportOpen] = useState(false)
  const [isAnalysesOpen, setIsAnalysesOpen] = useState(false)
  const [isSiteDetailsOpen, setIsSiteDetailsOpen] = useState(false)

  useEffect(() => {
    fetchSites()
    fetchContracts()
  }, [])

  const fetchSites = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/sites')
      if (response.ok) {
        const data = await response.json()
        setSites(data)
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des sites:', error)
    }
  }

  const fetchContracts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/contracts')
      if (response.ok) {
        const data = await response.json()
        setContracts(data)
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des contrats:', error)
    }
  }

  const handleUpdateWeatherScores = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/weather/update-all-scores', {
        method: 'POST'
      })
      if (response.ok) {
        fetchSites() // Recharger les sites avec les nouveaux scores
      }
    } catch (error) {
      console.error('Erreur lors de la mise à jour des scores:', error)
    }
  }

  const getRiskColor = (score: number) => {
    if (score < 10) return 'bg-green-100 text-green-800'
    if (score < 25) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const getRiskLabel = (score: number) => {
    if (score < 10) return 'Faible'
    if (score < 25) return 'Modéré'
    return 'Élevé'
  }

  const getBuildingTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      'office': 'Bureau',
      'factory': 'Usine',
      'warehouse': 'Entrepôt',
      'retail': 'Commerce',
      'residential': 'Résidentiel',
      'hospital': 'Hôpital',
      'school': 'École'
    }
    return labels[type] || type
  }

  const totalValue = sites.reduce((sum: number, site: Site) => sum + site.building_value, 0)
  const averageRisk = sites.length > 0 ? sites.reduce((sum: number, site: Site) => sum + site.risk_score, 0) / sites.length : 0
  const totalPremiums = contracts.reduce((sum: number, contract: Contract) => sum + contract.annual_premium, 0)
  const activeSites = sites.filter(site => site.contracts && site.contracts.length > 0).length

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Risk Insight Platform
          </h1>
          <p className="text-gray-600">
            Plateforme d'aide à la décision pour les assurances corporate
          </p>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Sites Assurés</CardTitle>
              <Building2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{activeSites}</div>
              <p className="text-xs text-muted-foreground">
                sur {sites.length} sites
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Valeur Totale</CardTitle>
              <Euro className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalValue.toLocaleString()}€
              </div>
              <p className="text-xs text-muted-foreground">
                Valeur des biens
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Risque Moyen</CardTitle>
              <AlertTriangle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {averageRisk.toFixed(1)}%
              </div>
              <p className="text-xs text-muted-foreground">
                Score de risque global
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Primes Annuelles</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalPremiums.toLocaleString()}€
              </div>
              <p className="text-xs text-muted-foreground">
                Chiffre d'affaires
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Actions */}
        <div className="flex flex-wrap gap-4 mb-8">
          <Button onClick={() => setIsAddSiteOpen(true)}>
            Ajouter un Site
          </Button>
          <Button variant="outline" onClick={() => setIsImportOpen(true)}>
            Importer CSV
          </Button>
          <Button variant="outline" onClick={() => setIsAnalysesOpen(true)}>
            Analyses
          </Button>
          <Button variant="outline" onClick={handleUpdateWeatherScores}>
            Mettre à jour les scores
          </Button>
          <StrategicRecommendationsDialog />
        </div>

        {/* Sites */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sites.map((site) => (
            <Card key={site.id} className="cursor-pointer hover:shadow-lg transition-shadow"
                  onClick={() => {
                    setSelectedSite(site)
                    setIsSiteDetailsOpen(true)
                  }}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{site.name}</CardTitle>
                  <Badge className={getRiskColor(site.risk_score)}>
                    {getRiskLabel(site.risk_score)}
                  </Badge>
                </div>
                <CardDescription className="flex items-center gap-1">
                  <MapPin className="h-3 w-3" />
                  {site.city}, {site.postal_code}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Type:</span>
                    <span className="text-sm font-medium">
                      {getBuildingTypeLabel(site.building_type)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Valeur:</span>
                    <span className="text-sm font-medium">
                      {site.building_value.toLocaleString()}€
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Surface:</span>
                    <span className="text-sm font-medium">
                      {site.surface_area}m²
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Score de risque:</span>
                    <span className="text-sm font-medium">
                      {site.risk_score.toFixed(1)}%
                    </span>
                  </div>
                  {site.contracts && site.contracts.length > 0 && (
                    <div className="pt-2 border-t">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Contrats:</span>
                        <Badge variant="secondary">{site.contracts.length}</Badge>
                      </div>
                      {site.contracts.map((contract) => (
                        <div key={contract.id} className="mt-2">
                          <AIAgentDialog 
                            siteId={site.id} 
                            contractId={contract.id}
                            onAnalysisComplete={(analysis) => {
                              console.log('Analyse IA terminée:', analysis)
                            }}
                          />
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Dialogs */}
        <AddSiteDialog 
          open={isAddSiteOpen} 
          onOpenChange={setIsAddSiteOpen}
          onSiteAdded={fetchSites}
        />
        <ImportCSVDialog 
          open={isImportOpen} 
          onOpenChange={setIsImportOpen}
          onSitesImported={fetchSites}
        />
        <AnalysesDialog 
          open={isAnalysesOpen} 
          onOpenChange={setIsAnalysesOpen}
          sites={sites}
          contracts={contracts}
        />
        {selectedSite && (
          <SiteDetailsDialog 
            open={isSiteDetailsOpen} 
            onOpenChange={setIsSiteDetailsOpen}
            site={selectedSite}
          />
        )}
      </div>
    </div>
  )
} 