# Coderr Django Projekt
    Coderr_frontend_v1.1.0
    Guest Login wie in der config.js
    

## Einführung
Coderr ist eine Plattform, auf der du deine Skills als Freelancer anbieten oder passende Dienstleistungen buchen kannst. Egal, ob du Programmierer, Designer oder Texter bist – mit Coderr kannst du Aufträge verwalten, Bestellungen abwickeln und Bewertungen sammeln. 

Diese API bildet das technische Rückgrat von Coderr und stellt Funktionen zur Verfügung, mit denen sich Angebote, Bestellungen, Benutzerprofile und Bewertungen steuern lassen. Sie richtet sich an Anbieter und Kunden gleichermaßen und sorgt für eine einfache und effiziente Abwicklung von Dienstleistungen.

Dank Django REST Framework bietet die API moderne Features wie Benutzerregistrierung, Authentifizierung, Rollenverwaltung und vieles mehr. Mit flexiblen Filter- und Suchfunktionen, Paginierung und einem durchdachten Rollenmanagement ist Coderr eine zuverlässige Plattform für den digitalen Marktplatz.

### Funktionen
- **Benutzerregistrierung und Authentifizierung** mit Django Auth.
- **Profile:** Verwaltung von Geschäfts- und Kundenprofilen.
- **Angebote:** CRUD-Operationen für Angebote und deren Details.
- **Bestellungen:** Erstellung und Verwaltung von Bestellungen.
- **Bewertungen:** Angebote mit Bewertungen und Kommentaren bewerten.
- **Filterung:** Möglichkeit zur Filterung von Angeboten und Bewertungen.
- **Paginierung:** Paginierte Ergebnisse für große Datenmengen.
- **Benutzerrollen:** Unterscheidung zwischen Geschäftsnutzern, Kunden und Administratoren.

### Voraussetzungen
- **Django REST Framework**
- **Python Version 3.12.3**

## Installation
1. **Repository klonen**
   ```sh
   git clone <repository-url>
   cd <projektverzeichnis>
   ```
2. **Virtuelle Umgebung erstellen und aktivieren**
   ```sh
   python -m venv env
   source venv/bin/activate  # für macOS/Linux
   env\Scripts\activate    # für Windows
   ```
3. **Abhängigkeiten installieren**
   ```sh
   pip install -r requirements.txt
   ```
4. **Datenbankmigrationen durchführen**
   ```sh
   python manage.py migrate
   ```
5. **Superuser erstellen**
   ```sh
   python manage.py createsuperuser
   ```
6. **Server starten**
   ```sh
   python manage.py runserver
   ```

Die API unter `http://127.0.0.1:8000/api` erreichbar.



## API Endpoints

### Angebote (Offers)
- `GET /offers/` - Liste aller Angebote mit Filter- und Suchmöglichkeiten
- `POST /offers/` – Erstellen eines neuen Angebots inklusive zugehöriger Details
- `GET /offers/{id}/` - Abrufen der Details eines spezifischen Angebots
- `PATCH /offers/{id}/` - Aktualisieren eines spezifischen Angebots
- `DELETE /offers/{id}/` - Löschen eines spezifischen Angebots
- `GET /offerdetails/{id}/` - Abrufen der Details eines spezifischen Angebotsdetails

### Bestellungen (Orders)
- `GET /orders/` - Liste der Bestellungen des angemeldeten Benutzers
- `POST /orders/` - Erstellen einer neuen Bestellung basierend auf einem Angebot
- `GET /orders/{id}/` - Abrufen der Details einer spezifischen Bestellung
- `PATCH /orders/{id}/` - Aktualisieren des Status einer spezifischen Bestellung
- `DELETE /orders/{id}/` - Löschen einer Bestellung (nur durch Admins)
- `GET /order-count/{business_user_id}/` - Gibt die Anzahl der laufenden Bestellungen eines Geschäftsnutzers zurück
- `GET /completed-order-count/{business_user_id}/` - Gibt die Anzahl der abgeschlossenen Bestellungen eines Geschäftsnutzers zurück

### Basisinformationen (Base Info)
- `GET /base-info/` - Abrufen der allgemeinen Basisinformationen der Plattform

### Benutzerprofile (Profiles)
- `GET /profile/{pk}/` - Abrufen der Details eines spezifischen Nutzers
- `PATCH /profile/{pk}/` - Aktualisieren der Details eines spezifischen Nutzers
- `GET /profiles/business/` - Liste aller Geschäftsnutzer
- `GET /profiles/customer/` - Liste aller Kundenprofile

### Authentifizierung/Registrierung (Authentication/Registration)
- `POST /login/` - User-Login
- `POST /registration/` - User-Registrierung

### Bewertungen (Reviews)
- `GET /reviews/` - Liste aller Bewertungen
- `POST /reviews/` - Erstellen einer neuen Bewertung
- `GET /reviews/{id}/` - Abrufen der Details einer spezifischen Bewertung
- `PATCH /reviews/{id}/` - Aktualisieren einer spezifischen Bewertung
- `DELETE /reviews/{id}/` - Löschen einer spezifischen Bewertung