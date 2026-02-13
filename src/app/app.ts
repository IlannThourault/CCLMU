import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChampsRecherche } from './components/champs-recherche/champs-recherche';
import { BarreRecherche } from './components/barre-recherche/barre-recherche';



@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ChampsRecherche, BarreRecherche],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})

export class App {
  protected readonly title = signal('CCLMU');
}
