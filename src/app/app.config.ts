/**
 * Configuration globale de l'application Angular
 * 
 * Ce fichier centralise tous les providers et configurations globales
 * qui sont appliqués au démarrage de l'application.
 * 
 * Il inclut :
 * - Le routage
 * - Les communications HTTP
 * - La gestion des erreurs globales
 * - L'hydratation client (SSR support)
 */

import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';

/**
 * Configuration principale de l'application
 * Fournit tous les services et configurations nécessaires
 * 
 * Providers inclus :
 * - Gestion des erreurs globales du navigateur
 * - Routeur avec la configuration des routes
 * - Hydratation client avec relecture des événements (pour SSR)
 * - Client HTTP pour les requêtes API
 */
export const appConfig: ApplicationConfig = {
  providers: [
    // Listeners pour capturer les erreurs non gérées globalement
    provideBrowserGlobalErrorListeners(),
    
    // Configuration du routeur Angular
    provideRouter(routes),
    
    // Support SSR avec hydratation client et replay des événements
    provideClientHydration(withEventReplay()),
    
    // Client HTTP pour les appels API
    provideHttpClient()
  ]
};
