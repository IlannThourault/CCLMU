import { Component, AfterViewInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Marker } from 'leaflet';
import { MapService } from '../../map-service';

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

  constructor(@Inject(PLATFORM_ID) private platformId: Object,
    private mapService : MapService){}

  async ngOnInit(){
    this.mapService.action$.subscribe((data) => {
      this.addMarker(data.firstDate, data.lastDate);
    })
  }

  async ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      const L = await import('leaflet');
      (window as any).L = L;
      await import('leaflet.markercluster'); // <-- ici seulement, dans le browser
      this.initMap(L);
    }
  }

  private initMap(L: any) {
    this.map = L.map('map')

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

  private async fetchCoordsFromDates(firstDate: Date, lastDate: Date): Promise<number[][]> {
    // URL de ton API
    const url = `http://localhost:4200/cordis/${firstDate.toISOString()}/${lastDate.toISOString()}`;

    // Fetch
    const response = await fetch(url);

    // Récupérer le JSON
    const L: string[] = await response.json();

    // Transformer en nombre
    const coords: number[][] = L.map(s => {
      const parts = s.split(",");          // supposer format "lat,lng"
      return [parseFloat(parts[0]), parseFloat(parts[1])];
    });

    return coords;
  }

  public async addMarker(firstDate : Date, lastDate : Date){
    const coords = await this.fetchCoordsFromDates(firstDate, lastDate);
    console.log(coords);
  }
}