/**
 * Modèle de données représentant un projet de recherche
 * 
 * Cette interface est utilisée pour typer les projets retournés par l'API backend
 * (endpoints CORDIS et HAL).
 * 
 * Elle offre une abstraction uniforme pour les données de projets
 * provenant de différentes sources.
 */

export interface Project {
  /**
   * Titre complet du projet de recherche
   */
  title: string;

  /**
   * Courte description/accroche du projet (teaser)
   * Généralement 1-2 lignes pour un aperçu rapide
   */
  teaser: string;

  /**
   * Description détaillée du projet
   * Contient le résumé complet ou l'objectif du projet
   */
  description: string;

  /**
   * Le coût/budget du projet en euros
   * Format : "XXXXXX€" pour CORDIS, "pas d'informations (hal)" pour HAL
   */
  cost: string;

  /**
   * Date de démarrage du projet
   * Format attendu : 'YYYY-MM-DD' (ex: '2020-03-15')
   */
  startDate: string;

  /**
   * Date de fin du projet
   * Format attendu : 'YYYY-MM-DD' (ex: '2023-06-30')
   */
  endDate: string;

  /**
   * Liste de toutes les organisations/institutions ayant participé au projet
   * Inclut les universités, organismes de recherche, entreprises, etc.
   */
  allContributors: string[];
}