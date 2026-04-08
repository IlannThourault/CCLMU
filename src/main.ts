/**
 * Point d'entrée de l'application Angular
 * 
 * Ce fichier initialise l'application en :
 * 1. Bootstrappant le composant racine App
 * 2. Appliquant la configuration globale appConfig
 * 3. Gérant les erreurs d'initialisation
 * 
 * C'est le premier fichier exécuté lors du démarrage de l'application
 */

import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

/**
 * Initialise l'application Angular
 * - Lance le composant racine App
 * - Applique la configuration globale
 * - Log les erreurs si l'initialisation échoue
 */
bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));
