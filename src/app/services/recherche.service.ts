/**
 * Service de gestion de la recherche et des champs de filtrage
 * 
 * Ce service centralise :
 * - La gestion des champs de recherche (mots-clés utilisateur)
 * - Le chargement des données HAL depuis le JSON public
 * - L'émission des événements de recherche
 * - Le filtrage des données par date et mots-clés
 * - La construction des requêtes de recherche
 * 
 * Utilise Angular Signals pour la réactivité
 * 
 * @injectable
 * @providedIn 'root' - Service singleton disponible globalement
 */

import { Injectable, signal, inject, computed} from '@angular/core';
import { HttpClient } from '@angular/common/http'; 
import { Subject } from 'rxjs';

/**
 * Interface représentant un champ de recherche
 * 
 * @property valeur - Le mot-clé saisi par l'utilisateur
 * @property timestamp - L'heure d'ajout du champ (en millisecondes)
 */
export interface ChampRecherche {
  valeur: string;
  timestamp: number;
}

/**
 * Interface représentant un point de données HAL
 * Correspond à une publication scientifique avec ses métadonnées
 * 
 * @property y - L'année de publication
 * @property m - Le mois de publication (1-12)
 * @property n - Le nom de l'organisation/auteur
 * @property kw - Les mots-clés associés
 * @property gps - Les coordonnées géographiques [[lat, long], ...]
 */
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
  /**
   * Injection du HttpClient pour les requêtes HTTP
   * @private
   */
  private http = inject(HttpClient);

  /**
   * Stockage des données HAL chargées depuis le JSON public
   * Accessible pour le filtrage et la recherche
   */
  public donneesHal: PointHal[] = [];

  /**
   * Signal contenant la liste des champs de recherche actuels
   * Chaque champ représente un mot-clé entré par l'utilisateur
   * Maximum 2 champs (limite imposée par ajouterChamp)
   */
  champs = signal<ChampRecherche[]>([]);

  /**
   * Version read-only du signal champs
   * Pour que les composants y accèdent sans pouvoir le modifier directement
   */
  readonly champsRecherche = this.champs.asReadonly();

  /**
   * Subject qui émet quand l'utilisateur déclenche une recherche
   * (généralement via le bouton loupe ou Entrée)
   * @private
   */
  private rechercheDeclencheeSource = new Subject<void>();

  /**
   * Observable publique s'abonnant aux déclenchements de recherche
   * Les composants écoutent cet observable pour réagir aux recherches
   */
  rechercheDeclenchee$ = this.rechercheDeclencheeSource.asObservable();

  /**
   * Signal computed qui retourne les mots-clés joints par des virgules
   * Exemple : "Paris, Recherche, Technologie"
   * Utile pour les requêtes API
   */
  public motsClesTexte = computed(() => 
    this.champs().map(c => c.valeur).join(',')
  );

  /**
   * Constructeur
   * Initialise le chargement des données HAL au démarrage du service
   */
  constructor() {
    this.chargerDonnees();
  }

  /**
   * Déclenche manuellement une recherche
   * Utile pour les appels programmatiques de recherche
   * 
   * @emits rechercheDeclenchee$
   */
  lancerRechercheForcee() {
    this.rechercheDeclencheeSource.next();
  }

  /**
   * Charge les données HAL depuis le fichier JSON public
   * S'exécute une seule fois au démarrage du service
   * @private
   */
  private chargerDonnees() {
    this.http.get<PointHal[]>('coorHal.json').subscribe({
      next: (data) => this.donneesHal = data,
      error: (err) => console.error("Erreur chargement JSON :", err)
    });
  }

  /**
   * Supprime un champ de recherche par sa valeur (pas son index)
   * Utile pour les boutons de suppression dans l'UI
   * 
   * @param valeur - Le mot-clé à supprimer
   */
  supprimerChamp(valeur: string): void {
    this.champs.update(champs => champs.filter(c => c.valeur !== valeur));
  }

  /**
   * Met à jour la valeur d'un champ de recherche existant
   * Utilisé quand l'utilisateur modifie un mot-clé
   * 
   * @param ancienneValeur - La valeur actuelle
   * @param nouvelleValeur - La nouvelle valeur
   */
  mettreAJourChamp(ancienneValeur: string, nouvelleValeur: string): void {
    this.champs.update(champs => 
      champs.map(c => c.valeur === ancienneValeur ? { ...c, valeur: nouvelleValeur } : c)
    );
  }

  /**
   * Supprime tous les champs de recherche
   * Utile pour un bouton "Effacer les filtres"
   */
  viderChamps(): void {
    this.champs.set([]);
  }

  /**
   * Ajoute un nouveau champ de recherche
   * Limite à 2 champs maximum pour éviter de surcharger l'UI
   * Déduplique automatiquement (pas de doublons)
   * 
   * @param valeur - Le mot-clé à ajouter
   */
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

  /**
   * Filtre les données HAL par plage d'années et mots-clés actuels
   * Retourne seulement les points correspondant aux critères
   * 
   * @param anneeMin - Année minimale (inclusive)
   * @param anneeMax - Année maximale (inclusive)
   * 
   * @returns Les données filtrées prêtes pour l'affichage sur la carte
   */
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