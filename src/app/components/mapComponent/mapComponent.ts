import { Component, AfterViewInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-mapComponent',
  templateUrl: './mapComponent.html',
  styleUrls: ['./mapComponent.scss']
})
export class MapComponent implements AfterViewInit {

  private map: any;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  async ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      const L = await import('leaflet');
      this.initMap(L);
    }
  }

  private initMap(L: any) {
    this.map = L.map('map')//.setView([48.8566, 2.3522], 13);

    fetch('https://nominatim.openstreetmap.org/search?format=json&q=Le+Mans,France')
    .then(res => res.json())
    .then(data => {
      const lat = parseFloat(data[0].lat);
      const lon = parseFloat(data[0].lon);
      console.log(lat, lon);
      this.map.setView([lat, lon], 13);
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(this.map);

    const icon = L.divIcon({
      className: 'custom-marker',
      html: '📍',
      iconSize: [24, 24],
      iconAnchor: [12, 24],
    });

    L.marker([48.8566, 2.3522], { icon }).addTo(this.map);
  }
}