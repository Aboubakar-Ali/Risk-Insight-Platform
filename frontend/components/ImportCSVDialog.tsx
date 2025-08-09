'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { FileText, Upload } from 'lucide-react'

interface ImportCSVDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSitesImported: () => void
}

export function ImportCSVDialog({ open, onOpenChange, onSitesImported }: ImportCSVDialogProps) {
  const [loading, setLoading] = useState(false)
  const [file, setFile] = useState<File | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/api/v1/sites/import-csv', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        setOpen(false)
        setFile(null)
        onSitesImported()
        alert('Sites importés avec succès !')
      } else {
        alert('Erreur lors de l\'import du CSV')
      }
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de l\'import du CSV')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Importer des sites via CSV</DialogTitle>
          <DialogDescription>
            Sélectionnez un fichier CSV contenant vos sites à importer.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="csv-file" className="text-sm font-medium">
              Fichier CSV
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <Upload className="h-8 w-8 mx-auto mb-2 text-gray-400" />
              <input
                id="csv-file"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
              />
              <label htmlFor="csv-file" className="cursor-pointer text-blue-600 hover:text-blue-800">
                {file ? file.name : 'Cliquez pour sélectionner un fichier CSV'}
              </label>
              {file && (
                <p className="text-sm text-gray-500 mt-2">
                  Fichier sélectionné: {file.name}
                </p>
              )}
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-medium mb-2">Format CSV attendu :</h4>
            <p className="text-sm text-gray-600">
              name,address,city,postal_code,latitude,longitude,building_type,building_value,surface_area,construction_year
            </p>
            <p className="text-sm text-gray-600 mt-1">
              Exemple: "Siège Paris","123 Rue de la Paix","Paris","75001",48.8566,2.3522,office,5000000,2000,2010
            </p>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Annuler
            </Button>
            <Button type="submit" disabled={loading || !file}>
              {loading ? 'Import...' : 'Importer'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
} 