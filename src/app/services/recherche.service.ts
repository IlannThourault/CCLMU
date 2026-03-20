import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http'; 

export interface ChampRecherche {
  valeur: string;
  timestamp: number;
}

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

  private chargerDonnees() {
    this.http.get<PointHal[]>('coorHal.json').subscribe({
      next: (data) => this.donneesHal = data,
      error: (err) => console.error("Erreur chargement JSON :", err)
    });
  }

  // --- Suppression par VALEUR ---
  supprimerChamp(valeur: string): void {
    this.champs.update(champs => champs.filter(c => c.valeur !== valeur));
  }

  // --- Mise à jour par VALEUR ---
  mettreAJourChamp(ancienneValeur: string, nouvelleValeur: string): void {
    this.champs.update(champs => 
      champs.map(c => c.valeur === ancienneValeur ? { ...c, valeur: nouvelleValeur } : c)
    );
  }

  viderChamps(): void {
    this.champs.set([]);
  }

  ajouterChamp(valeur: string): void {
    const dejaPresent = this.champs().some(c => c.valeur.toLowerCase() === valeur.toLowerCase());
    if (!dejaPresent && this.champs().length < 2) {
      const nouveauChamp: ChampRecherche = {
        valeur,
        timestamp: Date.now()
      };
      this.champs.update(champs => [...champs, nouveauChamp]);
    }
  }

  filtrerDonneesCarte(anneeMin: number, anneeMax: number) {
    const filtresActifs = this.champs().map(c => c.valeur.toLowerCase());
  
    return this.donneesHal.filter(point => {
      const matchDate = point.y >= anneeMin && point.y <= anneeMax;
      if (!matchDate) return false;
  
      if (filtresActifs.length === 0) return true;
  
      return point.kw.some((k: string) => 
        filtresActifs.includes(k.toLowerCase())
      );
    });
  }
}