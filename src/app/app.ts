/**
 * Composant racine de l'application CCLMU (Collaborations de le Mans Universités)
 * 
 * Ce composant est le point d'entrée principal de l'application Angular.
 * Il intègre tous les sous-composants et gère le routage principal.
 * 
 * Dependencies :
 * - Angular core components et signals
 * - Routeur Angular
 * - Tous les composants enfants (Map, Slider, Search, Results)
 * 
 * @component
 */

import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChampsRecherche } from './components/champs-recherche/champs-recherche';
import { BarreRecherche } from './components/barre-recherche/barre-recherche';



@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ChampsRecherche, BarreRecherche],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})

export class App {
  /**
   * Titre de l'application
   * Utilisé dans les templates et pour l'affichage générale
   * Signal immutable en lecture depuis l'extérieur
   */
  protected readonly title = signal('CCLMU');
}
