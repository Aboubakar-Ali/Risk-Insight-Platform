'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Cloud, Thermometer, Wind, Droplets, Snowflake, AlertTriangle } from 'lucide-react'

interface WeatherInfoProps {
  siteId: number
  siteName: string
}

interface WeatherData {
  site_id: number
  site_name: string
  location: string
  weather_risk: {
    risk_score: number
    risk_factors: {
      temperature: number
      humidity: number
      wind_speed: number
      conditions: string
    }
  }
}

export function WeatherInfo({ siteId, siteName }: WeatherInfoProps) {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchWeatherData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`http://localhost:8000/api/v1/weather/site/${siteId}`)
      if (response.ok) {
        const data = await response.json()
        setWeatherData(data)
      } else {
        setError('Erreur lors de la récupération des données météo')
      }
    } catch (err) {
      setError('Impossible de récupérer les données météo')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (siteId) {
      fetchWeatherData()
    }
  }, [siteId])

  const getRiskColor = (score: number) => {
    if (score >= 60) return 'destructive'
    if (score >= 40) return 'secondary'
    return 'default'
  }

  const getRiskLabel = (score: number) => {
    if (score >= 60) return 'Élevé'
    if (score >= 40) return 'Modéré'
    return 'Faible'
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Cloud className="h-5 w-5" />
            Météo en cours de chargement...
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-600">
            <AlertTriangle className="h-5 w-5" />
            Erreur météo
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-red-600">{error}</p>
          <button 
            onClick={fetchWeatherData}
            className="mt-2 text-sm text-blue-600 hover:text-blue-800 underline"
          >
            Réessayer
          </button>
        </CardContent>
      </Card>
    )
  }

  if (!weatherData) {
    return null
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Cloud className="h-5 w-5" />
          Conditions météo actuelles
        </CardTitle>
        <CardDescription>
          {weatherData.location}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Score de risque météo */}
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium">Risque météo</span>
          <Badge variant={getRiskColor(weatherData.weather_risk.risk_score)}>
            {Math.round(weatherData.weather_risk.risk_score)}% - {getRiskLabel(weatherData.weather_risk.risk_score)}
          </Badge>
        </div>

        {/* Conditions météo détaillées */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <Thermometer className="h-4 w-4 text-orange-500" />
            <div>
              <div className="text-sm font-medium">Température</div>
              <div className="text-xs text-gray-600">
                {weatherData.weather_risk.risk_factors.temperature}°C
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Droplets className="h-4 w-4 text-blue-500" />
            <div>
              <div className="text-sm font-medium">Humidité</div>
              <div className="text-xs text-gray-600">
                {weatherData.weather_risk.risk_factors.humidity}%
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Wind className="h-4 w-4 text-gray-500" />
            <div>
              <div className="text-sm font-medium">Vent</div>
              <div className="text-xs text-gray-600">
                {weatherData.weather_risk.risk_factors.wind_speed} m/s
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Cloud className="h-4 w-4 text-gray-400" />
            <div>
              <div className="text-sm font-medium">Conditions</div>
              <div className="text-xs text-gray-600">
                {weatherData.weather_risk.risk_factors.conditions}
              </div>
            </div>
          </div>
        </div>

        {/* Bouton de rafraîchissement */}
        <button 
          onClick={fetchWeatherData}
          className="w-full text-sm text-blue-600 hover:text-blue-800 underline"
        >
          Actualiser les données météo
        </button>
      </CardContent>
    </Card>
  )
} 