import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http'; 

export interface ChampRecherche {
  id: string;
  valeur: string;
  timestamp: number;
}

// Interface pour typer vos données HAL
export interface PointHal {
  y: number;
  m: number;
  n: string;
  kw: string[];
  gps: number[][];
}

@Injectable({
  providedIn: 'root'
})
export class RechercheService {
  private http = inject(HttpClient);
  
  public donneesHal: PointHal[] = [];

  champs = signal<ChampRecherche[]>([]);
  readonly champsRecherche = this.champs.asReadonly();

  constructor() {
    this.chargerDonnees();
  }

  // 2. Méthode pour charger le fichier JSON 
  private chargerDonnees() {
    this.http.get<PointHal[]>('coorHal.json').subscribe({
      next: (data) => {
        this.donneesHal = data;
        console.log(`${this.donneesHal.length} points de collaboration chargés.`);
      },
      error: (err) => console.error("Erreur lors du chargement du JSON :", err)
    });
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

  ajouterChamp(valeur: string): void {
    // Sécurité : Ne pas ajouter de doublons et respecter la limite de 7
    const dejaPresent = this.champs().some(c => c.valeur.toLowerCase() === valeur.toLowerCase());
    if (!dejaPresent && this.champs().length < 7) {
      const nouveauChamp: ChampRecherche = {
        id: this.genererIdUnique(),
        valeur,
        timestamp: Date.now()
      };
      this.champs.update(champs => [...champs, nouveauChamp]);
    }
  }


  filtrerDonneesCarte(anneeMin: number, anneeMax: number) {
    const filtresActifs = this.champs().map(c => c.valeur.toLowerCase());
  
    // On utilise maintenant this.donneesHal qui a été remplie par chargerDonnees()
    return this.donneesHal.filter(point => {
      const matchDate = point.y >= anneeMin && point.y <= anneeMax;
      if (!matchDate) return false;
  
      if (filtresActifs.length === 0) return true;
  
      // Vérification si au moins un mot-clé correspond
      return point.kw.some((k: string) => 
        filtresActifs.includes(k.toLowerCase())
      );
    });
  }

  private genererIdUnique(): string {
    return `champ-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
  }
}