import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface Project {
  title: string;
  teaser: string;
  description: string;
  cost: string;
  startDate: string;
  endDate: string;
  allContributors: string[];
}

@Component({
  selector: 'app-project-list',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.scss']
})
export class ProjectListComponent implements OnInit {

  projects: Project[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Remplace par ton API
    this.http.get<Project[]>('http://localhost:4200/cordis/listOfProject?nomOrga=GUATECS')
      .subscribe(data => this.projects = data);
  }

}