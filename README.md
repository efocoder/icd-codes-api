# ICD Codes API

This a simple API for recording and tracking ICD codes

### To get this application running, follow these steps;

1. Clone the git repository
   ```bash
    git clone https://github.com/efocoder/icd-codes-api.git
   ```
2. In order to run the application, you need to have Docker and Docker Compose installed on your system.

   ## Run application

2.1 Build first.

  ```docker-compose
    1. docker-compose build
    
    2. docker-compose up
   ```

2.2. Build and run at a goal

   ```docker-compose
    docker-compose up
```

### Test Logins
```
Email: clem.clem@gmail.com
Password: password
```

# Notes:

### A sample csv file with dummy data of 1000 can be found in utility folder

### A zip file of the OpenAPI specifications can be found in the utility folder.

### If you want to see where I designed the specifications document, here is the link:

#### Please note that not all the specifications was implemented

```Link
https://focadtechlab.stoplight.io/docs/icd-codes/c2NoOjM3Mzg1Njg4-icd-code-record
```

## Link to Postman collection documentation

```url
https://documenter.getpostman.com/view/4397935/UVeDs7Ey#f4d9fff7-2158-458d-bd73-5510534f1b2e
```

### Run test

```Docker
docker exec  -it icd-code-api sh
pytest
```
