import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MapService {
  private actionSource = new Subject<{firstDate : Date, lastDate : Date, keywords: string}>();

  action$ = this.actionSource.asObservable();
  triggerAction(firstDate : Date, lastDate : Date, keywords: string){
    this.actionSource.next({firstDate, lastDate, keywords});
  }
}
