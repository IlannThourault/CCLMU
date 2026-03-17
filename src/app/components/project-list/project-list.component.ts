import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ProjectService } from '../../services/project.services';

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

    constructor(
        private http: HttpClient, 
        private projectService: ProjectService
    ) {}

    ngOnInit() {
        // subscribe au bouton voir plus pour afficher les bons résultats
        this.projectService.voirPlus$.subscribe((nomProjet) => {
        console.log("Nom reçu depuis la carte :", nomProjet);
        
        // Appel a l'api avec le bon projet
        const url = `http://localhost:4200/cordis/listOfProject?nomOrga=${encodeURIComponent(nomProjet)}`;
        
        this.http.get<Project[]>(url).subscribe({
            next: (data) => {
            this.projects = data;
            console.log("Projets récupérés :", this.projects);
            },
            error: (err) => {
            console.error("Erreur lors de la récupération des projets", err);
            }
        });
        });
    }
}