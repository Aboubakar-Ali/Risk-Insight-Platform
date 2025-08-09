'use client'

import { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Building2, 
  MapPin, 
  Euro, 
  AlertTriangle, 
  Cloud, 
  Thermometer, 
  Wind, 
  Droplets,
  Calendar,
  FileText,
  RefreshCw,
  Zap,
  Shield,
  Globe,
  TrendingUp,
  Activity
} from 'lucide-react'

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
  surface_area?: number
  construction_year?: number
  risk_score: number
  notes?: string
  created_at: string
}

interface SiteDetailsDialogProps {
  site: Site
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function SiteDetailsDialog({ site, open, onOpenChange }: SiteDetailsDialogProps) {
  const [loading, setLoading] = useState(false)

  const getRiskColor = (score: number) => {
    if (score < 10) return 'default'
    if (score < 25) return 'secondary'
    return 'destructive'
  }

  const getRiskLabel = (score: number) => {
    if (score < 10) return 'Faible'
    if (score < 25) return 'Modéré'
    return 'Élevé'
  }

  const getZoneColor = (zone: string) => {
    if (zone === 'élevée') return 'destructive'
    if (zone === 'modérée') return 'secondary'
    return 'default'
  }

  const getRiskLevelFromPercentage = (percentage: number) => {
    if (percentage < 10) return { level: 'Faible', variant: 'default' }
    if (percentage < 25) return { level: 'Modéré', variant: 'secondary' }
    return { level: 'Élevé', variant: 'destructive' }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[900px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Building2 className="h-5 w-5" />
            {site.name}
          </DialogTitle>
          <DialogDescription>
            Détails complets du site et analyse des risques
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Informations générales */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                Informations Générales
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm font-medium text-gray-600">Adresse</div>
                  <div className="text-sm">{site.address}</div>
                  <div className="text-sm">{site.postal_code} {site.city}</div>
                  <div className="text-sm">{site.country}</div>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-600">Coordonnées</div>
                  <div className="text-sm">Lat: {site.latitude}</div>
                  <div className="text-sm">Lon: {site.longitude}</div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm font-medium text-gray-600">Type de bâtiment</div>
                  <div className="text-sm capitalize">{site.building_type}</div>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-600">Valeur</div>
                  <div className="text-sm font-semibold">{site.building_value.toLocaleString()}€</div>
                </div>
              </div>

              {(site.surface_area || site.construction_year) && (
                <div className="grid grid-cols-2 gap-4">
                  {site.surface_area && (
                    <div>
                      <div className="text-sm font-medium text-gray-600">Surface</div>
                      <div className="text-sm">{site.surface_area}m²</div>
                    </div>
                  )}
                  {site.construction_year && (
                    <div>
                      <div className="text-sm font-medium text-gray-600">Année de construction</div>
                      <div className="text-sm">{site.construction_year}</div>
                    </div>
                  )}
                </div>
              )}

              <div>
                <div className="text-sm font-medium text-gray-600">Date d'ajout</div>
                <div className="text-sm">{formatDate(site.created_at)}</div>
              </div>
            </CardContent>
          </Card>

          {/* Score de risque global */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4" />
                Score de Risque Global
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold">{Math.round(site.risk_score)}%</div>
                  <div className="text-sm text-gray-600">Risque {getRiskLabel(site.risk_score)}</div>
                </div>
                <Badge variant={getRiskColor(site.risk_score)} className="text-lg px-4 py-2">
                  {getRiskLabel(site.risk_score)}
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Données météo */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Cloud className="h-4 w-4" />
                Conditions Météo Actuelles
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <div className="text-sm font-medium">Risque météo</div>
                    <div className="text-xs text-gray-600">Basé sur les conditions actuelles</div>
                  </div>
                  <Badge variant={getRiskLevelFromPercentage(20).variant}>
                    {getRiskLevelFromPercentage(20).level}
                  </Badge>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center gap-2 p-3 bg-orange-50 rounded-lg">
                    <Thermometer className="h-4 w-4 text-orange-500" />
                    <div>
                      <div className="text-sm font-medium">Température</div>
                      <div className="text-xs text-gray-600">18.3°C</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 p-3 bg-blue-50 rounded-lg">
                    <Droplets className="h-4 w-4 text-blue-500" />
                    <div>
                      <div className="text-sm font-medium">Humidité</div>
                      <div className="text-xs text-gray-600">51%</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                    <Wind className="h-4 w-4 text-gray-500" />
                    <div>
                      <div className="text-sm font-medium">Vent</div>
                      <div className="text-xs text-gray-600">13.5 m/s</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                    <Cloud className="h-4 w-4 text-gray-400" />
                    <div>
                      <div className="text-sm font-medium">Conditions</div>
                      <div className="text-xs text-gray-600">brouillard</div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Risques de catastrophes naturelles */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Risques de Catastrophes Naturelles
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                  <div>
                    <div className="text-sm font-medium">Risque catastrophe</div>
                    <div className="text-xs text-gray-600">Basé sur l'historique</div>
                  </div>
                  <Badge variant={getRiskLevelFromPercentage(15).variant}>
                    {getRiskLevelFromPercentage(15).level}
                  </Badge>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="font-medium">Événements historiques</div>
                    <div className="text-lg font-bold">2</div>
                  </div>
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="font-medium">Fréquence</div>
                    <div className="text-lg font-bold capitalize">faible</div>
                  </div>
                </div>

                <div>
                  <div className="text-sm font-medium mb-2">Événements récents :</div>
                  <div className="space-y-2">
                    <div className="p-2 bg-gray-50 rounded text-xs">
                      <div className="flex justify-between">
                        <span className="font-medium capitalize">inondation</span>
                        <span>2022-03-15</span>
                      </div>
                      <div className="text-gray-600">Sévérité: modérée</div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Vulnérabilité géographique */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-4 w-4" />
                Vulnérabilité Géographique
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                  <div>
                    <div className="text-sm font-medium">Risque de vulnérabilité</div>
                    <div className="text-xs text-gray-600">Basé sur les zones géographiques</div>
                  </div>
                  <Badge variant={getRiskLevelFromPercentage(25).variant}>
                    {getRiskLevelFromPercentage(25).level}
                  </Badge>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-blue-50 rounded">
                    <div className="text-sm font-medium">Zone inondation</div>
                    <Badge variant="default" className="mt-1">
                      modérée
                    </Badge>
                  </div>
                  <div className="p-3 bg-orange-50 rounded">
                    <div className="text-sm font-medium">Zone séisme</div>
                    <Badge variant="default" className="mt-1">
                      faible
                    </Badge>
                  </div>
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="text-sm font-medium">Zone vent</div>
                    <Badge variant="default" className="mt-1">
                      modérée
                    </Badge>
                  </div>
                  <div className="p-3 bg-yellow-50 rounded">
                    <div className="text-sm font-medium">Zone affaissement</div>
                    <Badge variant="default" className="mt-1">
                      faible
                    </Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Notes */}
          {site.notes && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  Notes
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm">{site.notes}</p>
              </CardContent>
            </Card>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
} 