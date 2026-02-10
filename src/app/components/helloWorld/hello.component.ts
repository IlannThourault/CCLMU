import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-hello',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './hello.component.html',
  styleUrl: './hello.component.scss'
})
export class HelloComponent {
  query1: string = '';
  query2: string = '';

  search1() {
    console.log('Recherche 1 :', this.query1);
  }

  search2() {
    console.log('Recherche 2 :', this.query2);
  }
}
