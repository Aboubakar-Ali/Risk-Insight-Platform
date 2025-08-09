'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Building2 } from 'lucide-react'

interface AddSiteDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSiteAdded: () => void
}

export function AddSiteDialog({ open, onOpenChange, onSiteAdded }: AddSiteDialogProps) {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    city: '',
    postal_code: '',
    country: 'France',
    latitude: '',
    longitude: '',
    building_type: '',
    building_value: '',
    surface_area: '',
    construction_year: '',
    notes: ''
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/v1/sites', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          latitude: parseFloat(formData.latitude),
          longitude: parseFloat(formData.longitude),
          building_value: parseFloat(formData.building_value),
          surface_area: formData.surface_area ? parseFloat(formData.surface_area) : null,
          construction_year: formData.construction_year ? parseInt(formData.construction_year) : null,
        }),
      })

      if (response.ok) {
        setOpen(false)
        setFormData({
          name: '',
          address: '',
          city: '',
          postal_code: '',
          country: 'France',
          latitude: '',
          longitude: '',
          building_type: '',
          building_value: '',
          surface_area: '',
          construction_year: '',
          notes: ''
        })
        onSiteAdded()
      } else {
        alert('Erreur lors de la création du site')
      }
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de la création du site')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Ajouter un nouveau site</DialogTitle>
          <DialogDescription>
            Remplissez les informations du site à assurer.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Nom du site *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="building_type">Type de bâtiment *</Label>
              <Select value={formData.building_type} onValueChange={(value) => handleInputChange('building_type', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="office">Bureau</SelectItem>
                  <SelectItem value="warehouse">Entrepôt</SelectItem>
                  <SelectItem value="factory">Usine</SelectItem>
                  <SelectItem value="retail">Commerce</SelectItem>
                  <SelectItem value="residential">Résidentiel</SelectItem>
                  <SelectItem value="hospital">Hôpital</SelectItem>
                  <SelectItem value="school">École</SelectItem>
                  <SelectItem value="other">Autre</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="address">Adresse complète *</Label>
            <Input
              id="address"
              value={formData.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
              required
            />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="city">Ville *</Label>
              <Input
                id="city"
                value={formData.city}
                onChange={(e) => handleInputChange('city', e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="postal_code">Code postal *</Label>
              <Input
                id="postal_code"
                value={formData.postal_code}
                onChange={(e) => handleInputChange('postal_code', e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="country">Pays</Label>
              <Input
                id="country"
                value={formData.country}
                onChange={(e) => handleInputChange('country', e.target.value)}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="latitude">Latitude *</Label>
              <Input
                id="latitude"
                type="number"
                step="any"
                value={formData.latitude}
                onChange={(e) => handleInputChange('latitude', e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="longitude">Longitude *</Label>
              <Input
                id="longitude"
                type="number"
                step="any"
                value={formData.longitude}
                onChange={(e) => handleInputChange('longitude', e.target.value)}
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="building_value">Valeur du bâtiment (€) *</Label>
              <Input
                id="building_value"
                type="number"
                value={formData.building_value}
                onChange={(e) => handleInputChange('building_value', e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="surface_area">Surface (m²)</Label>
              <Input
                id="surface_area"
                type="number"
                value={formData.surface_area}
                onChange={(e) => handleInputChange('surface_area', e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="construction_year">Année de construction</Label>
            <Input
              id="construction_year"
              type="number"
              value={formData.construction_year}
              onChange={(e) => handleInputChange('construction_year', e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
            <Input
              id="notes"
              value={formData.notes}
              onChange={(e) => handleInputChange('notes', e.target.value)}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Annuler
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Création...' : 'Créer le site'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
} 