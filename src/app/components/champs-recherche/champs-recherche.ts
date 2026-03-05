import { Component, computed, inject } from '@angular/core'; // Ajoutez inject
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RechercheService } from '../../services/recherche.service';

@Component({
  selector: 'app-champs-recherche',
  standalone: true, // Assurez-vous d'être en standalone si nécessaire
  imports: [CommonModule, FormsModule],
  templateUrl: './champs-recherche.html',
  styleUrl: './champs-recherche.scss',
})
export class ChampsRecherche {
  // Utilisation de inject() pour une initialisation immédiate
  private rechercheService = inject(RechercheService);

  // Maintenant, ceci est parfaitement valide
  protected readonly champs = this.rechercheService.champsRecherche;
  
  protected readonly nombreChamps = computed(() => this.champs().length);

  // Le constructeur n'est plus nécessaire pour l'injection
  constructor() {}

  mettreAJourChamp(id: string, event: Event): void {
    const input = event.target as HTMLInputElement;
    this.rechercheService.mettreAJourChamp(id, input.value);
  }

  supprimerChamp(id: string): void {
    this.rechercheService.supprimerChamp(id);
  }
}