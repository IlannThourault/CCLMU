import { Injectable, signal } from '@angular/core';

export interface ChampRecherche {
  id: string;
  libelle: string;
  valeur: string;
  timestamp: number;
}

@Injectable({
  providedIn: 'root'
})
export class RechercheService {
  // Liste des champs de recherche
  private champs = signal<ChampRecherche[]>([]);
  
  // Exposer les champs en lecture seule
  readonly champsRecherche = this.champs.asReadonly();

  // Ajouter un nouveau champ
  ajouterChamp(libelle: string, valeur: string): void {
    const nouveauChamp: ChampRecherche = {
      id: this.genererIdUnique(),
      libelle,
      valeur,
      timestamp: Date.now()
    };
    
    this.champs.update(champs => [...champs, nouveauChamp]);
  }

  // Supprimer un champ
  supprimerChamp(id: string): void {
    this.champs.update(champs => champs.filter(c => c.id !== id));
  }

  // Mettre à jour un champ
  mettreAJourChamp(id: string, nouvelleValeur: string): void {
    this.champs.update(champs => 
      champs.map(c => c.id === id ? { ...c, valeur: nouvelleValeur } : c)
    );
  }

  // Vider tous les champs
  viderChamps(): void {
    this.champs.set([]);
  }

  // Obtenir tous les champs
  obtenirTousLesChamps(): ChampRecherche[] {
    return this.champs();
  }

  private genererIdUnique(): string {
    return `champ-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}