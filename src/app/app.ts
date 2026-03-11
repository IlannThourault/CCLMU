import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MapComponent } from './components/mapComponent/mapComponent';
import { SliderComponent } from './components/slider/slider';
import { ChampsRecherche } from './components/champs-recherche/champs-recherche';
import { BarreRecherche } from './components/barre-recherche/barre-recherche';



@Component({
  selector: 'app-root',
  imports: [RouterOutlet, MapComponent, SliderComponent, ChampsRecherche, BarreRecherche],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})

export class App {
  protected readonly title = signal('CCLMU');
}
