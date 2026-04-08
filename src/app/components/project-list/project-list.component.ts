import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ProjectService } from '../../services/project.services';
import { forkJoin } from 'rxjs';

interface Project {
    title: string;
    teaser: string;
    description: string;
    date: string;
    cout: string;
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
    nomProjet: String | undefined;

    constructor(
        private http: HttpClient, 
        private projectService: ProjectService
    ) {}

    ngOnInit() {
        // subscribe au bouton voir plus pour afficher les bons résultats
        this.projectService.voirPlus$.subscribe((nomProjet) => {
            this.nomProjet = nomProjet;
            
            // Appel a l'api avec le bon projet
            const urlCordis = `http://localhost:4200/cordis/listOfProject?nomOrga=${encodeURIComponent(nomProjet)}`;
            const urlHal = `http://localhost:4200/hal/getProjectsFromCollab?nomOrga=${encodeURIComponent(nomProjet)}&limite=10`;

            const cordisRequest = this.http.get<Project[]>(urlCordis);
            const halRequest = this.http.get<Project[]>(urlHal);

            
            
            forkJoin([cordisRequest, halRequest]).subscribe({
                next: ([dataCordis, dataHal]) => {
                this.projects = [...dataCordis, ...dataHal];
                
                // Scroll vers la section des projets après chargement
                setTimeout(() => {
                    const element = document.getElementById('liste-projets-section');
                    if (element) {
                        element.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'start'     
                        });
                    }
                }, 100);
                },
            });
        });
    }  
}