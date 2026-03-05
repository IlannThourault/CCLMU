import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MapComponent } from './components/mapComponent/mapComponent';
import { SliderComponent } from './components/slider/slider';

import { BarreRecherche } from './components/barre-recherche/barre-recherche';
import { ChampsRecherche } from './components/champs-recherche/champs-recherche';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, BarreRecherche, ChampsRecherche, MapComponent, SliderComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})

export class App {
  protected readonly title = signal('CCLMU');
}
