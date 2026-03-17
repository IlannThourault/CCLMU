import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { Project } from '../models/project';

@Injectable({ providedIn: 'root' })
export class ProjectService {
  private voirPlusSource = new Subject<string>();
  voirPlus$ = this.voirPlusSource.asObservable();

  emettreVoirPlus(nom: string) {
    this.voirPlusSource.next(nom);
  }
}