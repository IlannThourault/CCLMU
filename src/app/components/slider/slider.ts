import {
  Component,
  ElementRef,
  HostListener,
  ViewChild
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { DatePipe } from '@angular/common';

import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-slider',
  standalone: true,
  imports: [
    CommonModule,
    DatePipe,
    MatDatepickerModule,
    MatNativeDateModule,
    MatInputModule
  ],
  templateUrl: './slider.html',
  styleUrls: ['./slider.scss']
})
export class SliderComponent {

  @ViewChild('slider', { static: true }) slider!: ElementRef;

  minDate = new Date(2010, 0, 1);
  maxDate = new Date(2025, 11, 31);

  startDate = new Date(2012, 6, 1);
  endDate = new Date(2023, 2, 1);

  startPos = this.dateToPosition(this.startDate);
  endPos = this.dateToPosition(this.endDate);

  dragging: 'start' | 'end' | null = null;
  activeThumb: 'start' | 'end' | null = null;

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

  @HostListener('document:mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
    if (!this.dragging) return;

    const rect = this.slider.nativeElement.getBoundingClientRect();
    let percent = (event.clientY - rect.top) / rect.height;
    percent = Math.max(0, Math.min(1, percent));

    if (this.dragging === 'start' && percent < this.endPos) {
      this.startPos = percent;
      this.startDate = this.positionToDate(percent);
    }

    if (this.dragging === 'end' && percent > this.startPos) {
      this.endPos = percent;
      this.endDate = this.positionToDate(percent);
    }
  }

  @HostListener('document:mouseup')
  stopDrag() {
    this.dragging = null;
  }

  openCalendar(type: 'start' | 'end', picker: any) {
    this.activeThumb = type;
    picker.open();
  }

  onDateSelected(date: Date) {
    if (!date || !this.activeThumb) return;

    const pos = this.dateToPosition(date);

    if (this.activeThumb === 'start' && pos < this.endPos) {
      this.startDate = date;
      this.startPos = pos;
    }

    if (this.activeThumb === 'end' && pos > this.startPos) {
      this.endDate = date;
      this.endPos = pos;
    }

    this.activeThumb = null;
  }
}