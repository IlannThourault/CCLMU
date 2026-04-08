/**
 * Service de communication pour les actions de la carte
 * 
 * Ce service coordonne les événements entre la carte et les autres composants,
 * en particulier le slider de dates et les filtres de recherche.
 * 
 * Utilise le pattern Observable/Subject pour la communication réactive
 * 
 * @injectable
 * @providedIn 'root' - Service singleton disponible globalement
 */

import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

/**
 * Structure des données d'action de la carte
 * @property firstDate - Date de début pour le filtrage
 * @property lastDate - Date de fin pour le filtrage
 * @property keywords - Mots-clés de filtrage (séparés par des virgules)
 */
interface MapAction {
  firstDate: Date;
  lastDate: Date;
  keywords: string;
}

@Injectable({
  providedIn: 'root',
})
export class MapService {
  /**
   * Subject privé émettant les actions de la carte
   * @private
   */
  private actionSource = new Subject<MapAction>();

  /**
   * Observable publique s'abonnant aux actions de la carte
   * Les composants écoutent ici pour réagir aux changements de plage de dates
   * ou de mots-clés sur la carte
   */
  action$ = this.actionSource.asObservable();

  /**
   * Déclenche une action de filtrage sur la carte
   * Notifie tous les observateurs abonnés
   * 
   * @param firstDate - Date de début du filtrage
   * @param lastDate - Date de fin du filtrage
   * @param keywords - Mots-clés pour le filtrage
   * 
   * @emits action$ avec l'objet MapAction complet
   */
  triggerAction(firstDate: Date, lastDate: Date, keywords: string) {
    this.actionSource.next({ firstDate, lastDate, keywords });
  }
}
