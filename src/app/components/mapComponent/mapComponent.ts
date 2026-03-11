import { Component, AfterViewInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Marker } from 'leaflet';
import { MapService } from '../../map-service';
import { last } from 'rxjs';

function formatDate(date: Date): string {
  const y = date.getFullYear();
  const m = (date.getMonth() + 1).toString().padStart(2, '0'); // Mois de 0 à 11
  const d = date.getDate().toString().padStart(2, '0');
  return `${y}-${m}-${d}`;
}

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

  private map: any;
  private L :any;
  private markersGroup: any;

  constructor(@Inject(PLATFORM_ID) private platformId: Object,
    private mapService : MapService){}

  async ngOnInit(){
    this.mapService.action$.subscribe((data) => {
      this.addMarker(data.firstDate, data.lastDate);
    })
  }

  async ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.L = await import('leaflet');
      (window as any).L = this.L;

      await import('leaflet.markercluster');
      this.initMap(this.L);
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

    this.markersGroup = L.markerClusterGroup();

    this.map.addLayer(this.markersGroup);

    // Gestion des boutons dans le popup
    this.map.on('popupopen', (e: any) => {
      const button = e.popup._contentNode.querySelector('.marker-btn');
      if (button) {
        button.addEventListener('click', () => {
          alert(`Bouton cliqué ! Coordonnées: ${button.dataset.lat}, ${button.dataset.lng}`);
        });
      }
    });

    console.log(this.L, " : ", this.markersGroup);
  }

  private async fetchCoordsFromDates(firstDate: Date, lastDate: Date): Promise<{nom: string, coords: number[]}[]> {
    const urlCORDIS = `http://localhost:4200/cordis/getAllLocalizationsFromDates?deb=${formatDate(firstDate)}&fin=${formatDate(lastDate)}`;
    const urlHAL = `http://localhost:4200/hal/getDataFromFilters?anneeMin=${firstDate.getFullYear()}&anneeMax=${lastDate.getFullYear()}&moisMin=${firstDate.getMonth()}&moisMax=${lastDate.getMonth()}&keywords=`

    const responseCORDIS = await fetch(urlCORDIS);
    const responseHAL = await fetch(urlHAL);

    const listeCORDIS: string[] = await responseCORDIS.json();
    const listeHAL: string[] = await responseHAL.json();

    const liste: string[] = listeCORDIS.concat(listeHAL);

    const coords: {nom: string, coords: number[]}[] = liste.map(s => {
      const parts = s.split(",");
      if (Number.isNaN(parseFloat(parts[1]))){
        console.log(s);
      }
      return {nom: parts[0], coords: [parseFloat(parts[1]), parseFloat(parts[2])]};
    });

    return coords;
  }

  public async addMarker(firstDate : Date, lastDate : Date){
    if (!this.L || !this.markersGroup || !this.map) {
    console.warn("Map ou markersGroup pas encore initialisés. Attendre ngAfterViewInit");
    return;
  }

  const datas = await this.fetchCoordsFromDates(firstDate, lastDate);

  this.markersGroup.clearLayers();


  datas.forEach(data => {
    const popupContent = `
      <div>
        <h4>${data.nom}</h4>
        <div class="seeMore">Voir plus</div>
      </div>`;
    const defaultIcon = this.L.icon({
    iconUrl: 'media/marker-icon.png',
    iconRetinaUrl: 'media/marker-icon-2x.png',
    shadowUrl: 'media/marker-shadow.png',

    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
    const marker = this.L.marker([data.coords[0], data.coords[1]], {icon : defaultIcon}).bindPopup(popupContent, { autoClose: false});
    this.markersGroup.addLayer(marker);
  });
  }
}