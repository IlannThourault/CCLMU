import {
  Component,
  ElementRef,
  HostListener,
  ViewChild
} from '@angular/core';

import { CommonModule, DatePipe } from '@angular/common';
import { map } from 'leaflet';
import { MapComponent } from '../mapComponent/mapComponent';
import { MapService } from '../../map-service';
import { RechercheService } from '../../services/recherche.service';

@Component({
  selector: 'app-slider',
  standalone: true,
  imports: [
    CommonModule,
    DatePipe
  ],
  templateUrl: './slider.html',
  styleUrls: ['./slider.scss']
})
export class SliderComponent {

    constructor(
        private mapService: MapService,
        private rechercheService: RechercheService
    ) {}

    @ViewChild('slider', { static: true }) slider!: ElementRef;

    minDate = new Date(0, 0, 0);
    maxDate = new Date(0, 0, 0);

    startDate = new Date();
    endDate = new Date();

    startPos = 0;
    endPos = 1;

    dragging: 'start' | 'end' | null = null;

    async ngOnInit() {
        const [
            firstYear, firstMonth, firstDay,
            lastYear, lastMonth, lastDay
        ] = await Promise.all([
            fetch("http://localhost:4200/cordis/firstDate/year"),
            fetch("http://localhost:4200/cordis/firstDate/month"),
            fetch("http://localhost:4200/cordis/firstDate/day"),
            fetch("http://localhost:4200/cordis/lastDate/year"),
            fetch("http://localhost:4200/cordis/lastDate/month"),
            fetch("http://localhost:4200/cordis/lastDate/day")
        ]);

        const firstYearRes = Number(await firstYear.text());
        const firstMonthRes = Number(await firstMonth.text());
        const firstDayRes = Number(await firstDay.text());

        const lastYearRes = Number(await lastYear.text());
        const lastMonthRes = Number(await lastMonth.text());
        const lastDayRes = Number(await lastDay.text());

        this.minDate = new Date(firstYearRes, firstMonthRes - 1, firstDayRes);
        this.maxDate = new Date(lastYearRes, lastMonthRes - 1, lastDayRes);

        this.startDate = this.minDate;
        this.endDate = this.maxDate;

        this.startPos = 0;
        this.endPos = 1;

        // click sur la loupe de la barre de recherche
        this.rechercheService.rechercheDeclenchee$.subscribe(() => {
        this.draggedFromHandle = true; // On simule un drag pour passer la sécurité de stopDrag
        this.stopDrag();
    });
    }

  dateToPosition(date: Date): number {
    const total = this.maxDate.getTime() - this.minDate.getTime();
    const delta = date.getTime() - this.minDate.getTime();
    return delta / total;
  }

  positionToDate(position: number): Date {
    const total = this.maxDate.getTime() - this.minDate.getTime();
    const timestamp = this.minDate.getTime() + total * position;
    return new Date(timestamp);
  }

  startDrag(type: 'start' | 'end', event: MouseEvent) {
    event.stopPropagation();
    this.dragging = type;
    this.draggedFromHandle = true;
  }

  minGapYears = 3;

  @HostListener('document:mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
  if (!this.dragging) return;

  const rect = this.slider.nativeElement.getBoundingClientRect();
  let percent = (event.clientY - rect.top) / rect.height;
  percent = Math.max(0, Math.min(1, percent));

  const newDate = this.positionToDate(percent);

  if (this.dragging === 'start') {
    const maxStartDate = new Date(this.endDate);
    maxStartDate.setFullYear(maxStartDate.getFullYear() - this.minGapYears);

    if (newDate <= maxStartDate) {
      this.startPos = percent;
      this.startDate = newDate;
    }
  }

  if (this.dragging === 'end') {
    const minEndDate = new Date(this.startDate);
    minEndDate.setFullYear(minEndDate.getFullYear() + this.minGapYears);

    if (newDate >= minEndDate) {
      this.endPos = percent;
      this.endDate = newDate;
    }
  }
}

  timeoutId: any;

    draggedFromHandle: boolean = false;

    @HostListener('document:mouseup')
    stopDrag() {
        if (this.draggedFromHandle) {
            const motsCles = this.rechercheService.motsClesTexte();

            // Action seulement si le drag a commencé sur un bouton
            if (this.timeoutId) {
                clearTimeout(this.timeoutId);
            }

            this.timeoutId = setTimeout(() => {
                this.mapService.triggerAction(this.startDate, this.endDate, motsCles);
                this.timeoutId = null;
            }, 1000);
        }

        // Réinitialisation des flags à chaque mouseup
        this.dragging = null;
        this.draggedFromHandle = false;
    }
}