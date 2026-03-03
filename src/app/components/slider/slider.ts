import {
  Component,
  ElementRef,
  HostListener,
  ViewChild
} from '@angular/core';

import { CommonModule, DatePipe } from '@angular/common';

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

  @ViewChild('slider', { static: true }) slider!: ElementRef;

  minDate = new Date(2014, 5, 1);
  maxDate = new Date(2030, 2, 28);

  startDate = new Date(2014, 5, 1);
  endDate = new Date(2030, 2, 28);

  startPos = this.dateToPosition(this.startDate);
  endPos = this.dateToPosition(this.endDate);

  dragging: 'start' | 'end' | null = null;

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

  @HostListener('document:mouseup')
  stopDrag() {
    this.dragging = null;
  }
}