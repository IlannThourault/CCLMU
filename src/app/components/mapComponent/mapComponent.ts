import { Component, AfterViewInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

interface MarkerItem {
  lat: number;
  lng: number;
  title: string;
  description: string;
}

@Component({
  selector: 'app-mapComponent',
  templateUrl: './mapComponent.html',
  styleUrls: ['./mapComponent.scss']
})
export class MapComponent implements AfterViewInit {

  markers: MarkerItem[] = [
    { lat: 48.0061, lng: 0.1996, title: 'Le Mans', description: 'Ville célèbre pour les 24h !' },
    { lat: 48.008, lng: 0.202, title: 'Point B', description: 'Autre marker avec info.' },
  ];

  private map: any;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  async ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      const L = await import('leaflet');
      (window as any).L = L;
      await import('leaflet.markercluster'); // <-- ici seulement, dans le browser
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

    const markersGroup = L.markerClusterGroup();


    /*
    const icon = L.divIcon({
      className: 'custom-marker',
      html: '📍',
      iconSize: [24, 24],
      iconAnchor: [12, 24],
    });*/
    /*
    L.marker([48.8566, 2.3522], { icon }).addTo(this.map);
    const marker = L.marker([48.0061, 0.1996]).addTo(this.map);
    marker.bindPopup('Voici Le Mans ! 🏎️');*/

    this.markers.forEach((item) => {
      // Contenu du popup avec boutons
      const popupContent = `
        <div>
          <h4>${item.title}</h4>
          <p>${item.description}</p>
          <button class="marker-btn" data-lat="${item.lat}" data-lng="${item.lng}">Cliquer ici</button>
        </div>
      `;

      const marker = L.marker([item.lat, item.lng])
        .bindPopup(popupContent);

      markersGroup.addLayer(marker);
    });

    this.map.addLayer(markersGroup);

    // Gestion des boutons dans le popup
    this.map.on('popupopen', (e: any) => {
      const button = e.popup._contentNode.querySelector('.marker-btn');
      if (button) {
        button.addEventListener('click', () => {
          alert(`Bouton cliqué ! Coordonnées: ${button.dataset.lat}, ${button.dataset.lng}`);
        });
      }
    });
  }
}