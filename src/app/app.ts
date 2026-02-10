import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HelloComponent } from './components/helloWorld/hello.component';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HelloComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})

export class App {
  protected readonly title = signal('CCLMU');
}
