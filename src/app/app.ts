import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HelloComponent } from './components/helloWorld/hello.component';
import { SliderComponent } from './components/slider/slider';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HelloComponent, SliderComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})

export class App {
  protected readonly title = signal('CCLMU');
}
