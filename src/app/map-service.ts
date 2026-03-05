import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MapService {
  private actionSource = new Subject<{firstDate : Date, lastDate : Date}>();

  action$ = this.actionSource.asObservable();
  triggerAction(firstDate : Date, lastDate : Date){
    this.actionSource.next({firstDate, lastDate});
  }
}
