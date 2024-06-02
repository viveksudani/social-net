# Social Network - Backend

### Installation Steps:
1. Clone this repository
2. Create .env file by copying .env.example file. (Default values of variables are test ready.)
3. Run project:
```
docker compose up --build
```
4. Apply the migrations run following command in separate terminal
```
docker compose exec web python3 manage.py migrate
```
5. To create superuser run following command in separate terminal
```
docker compose exec web python3 manage.py createsuperuser
```
6. To stop project use CONTROL-C in main terminal

### Additional Information:
- Postman Collection (Published): https://documenter.getpostman.com/view/8563658/2sA3QwcACw
- Postman Collection (Json file): https://drive.google.com/file/d/1yimidn5AKqUD82SJ8QByX4h-JnIk7BvD/view?usp=sharing
- Life of an access token is set to an hour to make evaluation smooth.
