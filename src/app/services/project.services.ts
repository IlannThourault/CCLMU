/**
 * Service de gestion des projets et des interactions utilisateur
 * 
 * Ce service gère la communication entre les composants pour :
 * - Signaler quand l'utilisateur demande plus de détails sur un projet
 * - Émettre des événements observable pour les autres composants
 * 
 * Utile pour le passage de données et la synchronisation entre composants découplés
 * 
 * @injectable
 * @providedIn 'root' - Service disponible globalement
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { Project } from '../models/project';

@Injectable({ providedIn: 'root' })
export class ProjectService {
  /**
   * Subject pour émettre les demandes de "Voir plus" d'un projet
   * Utilisé pour signaler aux autres composants qu'un utilisateur veut des détails
   * @private
   */
  private voirPlusSource = new Subject<string>();

  /**
   * Observable publique émettant les noms des projets demandant plus de détails
   * Les composants s'abonnent ici pour recevoir les notifications
   */
  voirPlus$ = this.voirPlusSource.asObservable();

  /**
   * Émet un événement quand l'utilisateur demande plus de détails sur un projet
   * 
   * @param nom - Le nom/identifiant du projet
   * @emits voirPlus$ avec le nom du projet
   */
  emettreVoirPlus(nom: string) {
    this.voirPlusSource.next(nom);
  }
}