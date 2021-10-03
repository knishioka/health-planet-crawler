# Health Planet Crawler

## Set Up Environment
```bash
cp .env.sample .env
vi .env
```

You need to set following env variables.

- HEALTH_PLANET_ID: login id.
- HEALTH_PLANET_PASSWORD: login password.

## Run
```bash
export $(cat .env | xargs) && python health_planet.py  --start-date 2021-09-01 --end-date 2021-09-30
```
