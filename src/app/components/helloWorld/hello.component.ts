import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';  // <-- important pour ngModel

@Component({
  selector: 'app-hello',
  standalone: true,
  templateUrl: './hello.component.html',
  imports: [CommonModule, FormsModule]  // <-- FormsModule ajouté ici
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