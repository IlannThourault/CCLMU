import { Component, inject } from '@angular/core'; // Importez inject
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RechercheService } from '../../services/recherche.service';

@Component({
  selector: 'app-barre-recherche',
  standalone: true, // Ajoutez standalone si nécessaire
  imports: [FormsModule, CommonModule],
  templateUrl: './barre-recherche.html',
  styleUrl: './barre-recherche.scss',
})
export class BarreRecherche {
  private rechercheService = inject(RechercheService); // Utilisation de inject()

  query1: string = '';
  query2: string = '';

  search1() {
    if (this.query1.trim()) {
      this.rechercheService.ajouterChamp('Recherche 1', this.query1);
    }
  }

  search2() {
    if (this.query2.trim()) {
      this.rechercheService.ajouterChamp('Recherche 2', this.query2);
    }
  }

  viderTout() {
    this.rechercheService.viderChamps();
    this.query1 = '';
    this.query2 = '';
  }
}