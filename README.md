# Overview

---

## Setup 
### For local development environment build 
```bash
~$ cd ${project}
~$ docker-compose -f docker-compose-Local.yml up
```
### For web production environment build 
```bash
~$ cd ${project}
~$ docker-compose -f docker-compose-Production.yml up
```

#### Todos
- Implement Kubernetes environment setting
- Improve CI/CD
- Implement requirements.txt
- Implement setup.py

#### Requirements
Apache Airflow is tested with:

|              | Master version (dev)      | 
| ------------ | ------------------------- |
| Python       | 3.6, 3.7, 3.8             | 
| MySQL        | 5.7                    | 
| Redis        | 6.0-alpine                    | 
| Mongo        |4.4.2                | 

