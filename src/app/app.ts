import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MapComponent } from './components/mapComponent/mapComponent';
import { SliderComponent } from './components/slider/slider';
import { ChampsRecherche } from './components/champs-recherche/champs-recherche';
import { BarreRecherche } from './components/barre-recherche/barre-recherche';
import { ProjectListComponent } from './components/project-list/project-list.component';
import {Menu} from "./components/menu/menu";


@Component({
  selector: 'app-root',
  imports: [RouterOutlet, MapComponent, SliderComponent, ChampsRecherche, BarreRecherche, ProjectListComponent, Menu],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})

export class App {
  protected readonly title = signal('CCLMU');
}
