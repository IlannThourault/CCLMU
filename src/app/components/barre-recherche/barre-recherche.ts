import { Component, inject } from '@angular/core'; 
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RechercheService } from '../../services/recherche.service';
import { HalKeywords } from '../../../../backend/ressources/keywordsHal'; 

@Component({
  selector: 'app-barre-recherche',
  standalone: true, 
  imports: [FormsModule, CommonModule],
  templateUrl: './barre-recherche.html',
  styleUrl: './barre-recherche.scss',
})
export class BarreRecherche {
  public rechercheService = inject(RechercheService);

  recherche: string = '';

  motsCordis = ['Imagination', 'Adsorption', 'light-matter interactions', 'CCAM', 'Edible Soft Matter', 'Emulsions', 'multilateral exchange', 'microcontrollers', 'Self-assembly', 'scenography', 'nature-based solution', 'intersectoriality', 'Surface acoustic waves', 'geophysics', 'Engineering of digitalisation solutions', 'Energy-aware computing', 'non volatile memory', 'CMC manufacturing', 'Renewable Energy', 'pilot lines', 'Model order reduction', 'Microcontrollers', 'Interactive', 'Atomic Cluster', 'quantum technologies', 'Smart system integration', 'France', 'Food sciences', 'Edge computing', 'Event', 'photobioreactors', 'core noise', 'Texture', 'Atmosphere', 'proximity', 'Researchers', 'diatoms', 'Renewable Hydrogen', 'biorefinery', 'Entertainment', 'Entertainement', 'isoprenoids', 'Metamaterials', 'gender+', 'UHBR engine', 'Updates', 'Ideas', 'ecosystem services', 'picosecond laser ultrasonics', 'Caramelization', 'sustainable material concepts', 'Sensory', 'mobility', 'Hydrogen storage', 'Creativity', 'Stories', 'FDSOI', 'Automotive Autonomous driving', 'rewilding', 'LES', 'night', 'environmental performance', 'Computational chemistry', 'scenario', 'Green synthesis', 'marginal land', 'vibration damping', 'remote-sensing', 'H2 valley', 'aquaculture', 'Hydrogen Valley', 'Plants', 'fractures network', 'Anthropology', 'Natural History', 'Rheology', 'neural networks', 'numerical modelling', 'antimicrobial compounds', 'Future', 'intimate', 'Metal Organic Frameworks', 'Microalgae', 'dialogue', 'vibration and acoustics', 'mechanical discontinuities', 'public understanding of research', 'aircraft', 'soft sediment', 'mysterious', 'machine learning', 'Sharing economy', 'low resources', 'evaluation', 'equipment and materials', 'biomass', 'lightweight', 'Noise pollution', 'Maillard reaction', 'Machine Learning', 'acoustic liner', 'experimental methods', 'numerical', 'cropping systems', 'optoacoustic and acousto-optic transducers', 'digital twin', 'Safety', 'Bioengineering', 'twinning', 'explainability', 'human assisted learning', 'intersectionality', 'Intertidal seascapes', 'lable-free', 'Museums', 'European', 'Voyage', 'permeability of rocks', 'green', 'SDV', 'Upgrades', 'Experience', 'Foams', 'Archives', 'Together', 'natural blue pigments', 'Meetings', 'Decarbonation', 'Inclusiveness', 'Investigations', 'stakeholder', 'Multidisciplinary', 'boundary element method', 'sea defence', 'superlattice', 'smart systems', 'Gender Equality Plan', 'Plant-based proteins', 'Synchrotron', 'Acoustic performance', 'standardization', 'Collections', 'Responsability', 'modelling', 'low noise solutions', 'single frequency lasers', 'biodiversity', 'spectroscopy', 'CAA', 'energy consumption', 'Haslea', 'quantum computers', 'ECDL', 'finite element method', 'rock mechanics', 'Security', 'Doctoral Training', 'Encounter', 'natural language processing', 'turbine noise', 'institutional change', 'research excellence', 'Hydrogen', 'low ILUC feedstock', 'SERS', 'Foaming', 'Experiment', 'Health', 'Noise and Vibration', 'Dialogue', 'provincial science', 'fluid overpressure', 'Semiconductor process', 'CO2 storage', 'Smart mobility', 'lipids', 'Solution Combustion Synthesis', 'Speech processing', 'C sequestration', 'national', 'Social determinants', 'DNA origami', 'circulation of knowledge', 'phase change memory', 'sound aborption', 'optimization', 'history of science', 'blue biotechnology', 'Porous Materials', 'Design technology', 'Social sciences', 'Sound transmission loss', 'engine acoustic test', 'embedded flash technology', 'training', 'Publics', 'Ultra low power and secured & safety System on Chip (SoC)', 'Tribology', 'biobased products', 'governance', 'industrial crops', 'Public', 'Participatory', 'Acoustic Black Hole', 'omics', 'Food structure', 'Absorption', 'Researchers Publics Meetings Dialogue Experiment Experience Entertainment France Event European Loyalty Participatory Together Atmosphere', 'Aeroacoustics', 'Widening Countries', 'fats and polysaccharides', 'Biosensing', 'Impossible?']
  motsHal = HalKeywords;

  tousLesMots = [...this.motsCordis, ...this.motsHal].map(mot => mot.trim().toLowerCase());



  // Les listes filtrées à afficher
  suggestionsFiltrees: string[] = [];

  filtrerSuggestions(event: any) {
    const valeur = event.target.value.toLowerCase();
    // 4. On vérifie aussi la limite de 2 ici pour ne pas suggérer inutilement
    if (valeur.length > 1 && this.rechercheService.champs().length < 2) { 
      this.suggestionsFiltrees = this.tousLesMots
        .filter(mot => mot && mot.toLowerCase().includes(valeur))
        .slice(0, 15); 
    } else {
      this.suggestionsFiltrees = [];
    }
  }

  selectionnerSuggestion(mot: string) {
    if (this.rechercheService.champs().length < 2) {
      this.rechercheService.ajouterChamp(mot);
    }
    this.recherche = '';             
    this.suggestionsFiltrees = []; 
  }

  rechercher() {
    if (this.recherche.trim()) {
      this.rechercheService.ajouterChamp(this.recherche);
      this.recherche = '';
    }
  }

  viderTout() {
    this.rechercheService.viderChamps();
    this.recherche = '';
  }
}