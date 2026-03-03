import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MapComponent } from './components/mapComponent/mapComponent';
import { SliderComponent } from './components/slider/slider';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, MapComponent, SliderComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})

export class App {
  protected readonly title = signal('CCLMU');
}
