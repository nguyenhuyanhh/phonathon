# phonathon

The system aims to provide a modern and free alternative to the current Campuscall system used in Phonathon.

## Overview

- The system would be implemented in Django 1.11, using Python 3.5+ on Linux
- A prototype would be hosted locally, using the Django development server with SQLite backend
- If possible, the prototype would be deployed on Google Cloud/ DigitalOcean, using PostgreSQL as the database backend

The current focus is on getting a minimum working example for presentation to stakeholders.

## Documentation

### Models

#### `Prospect`

This model holds information about a prospect. The fields are as follows:

| Field | Description | Type
| -- | -- | --
| `id` | Unique numerical id| `int`
| `nric` | NRIC/FIN/Passport number | `str(15)`
| `salutation` | Salutation (Mr./ Mrs./ etc.) | `str(10)`
| `name` | Full name | `str(50)`
| `email` | Email address | `str`
| `address_1` | Home address (line 1) | `str(35)`
| `address_2` | Home address (line 2) | `str(35)`
| `address_3` | Home address (line 3) | `str(35)`
| `address_postal` | Home address (postal code) | `str(6)`
| `phone_home` | Home phone number | `str(8)`
| `phone_mobile` | Mobile phone number | `str(8)`
| `education_school` | Education (school graduated from) | `str`
| `education_degree` | Education (degree obtained) | `str`
| `education_year` | Education (graduation year) | `datetime`