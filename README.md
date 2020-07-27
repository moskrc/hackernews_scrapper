# Hacker News Scrapper
Grab the latest news from https://news.ycombinator.com/ and store the news in database. Support REST API for the news.

**Flask/Redis sample**

### Installation

```Bash
# dev
$ cp .env.dev.sample .env.dev
$ docker-compose up --build
# prod
$ cp .env.prod.sample .env.prod
$ docker-compose -f docker-compose.prod.yml up --build
$ docker exec -ti app ./manage.py recreate_db
```

## How to test
```Bash
$ docker exec -ti app hackernews/manage.py test
```

### How to manage

Recreate DB:

```Bash
$ docker exec -ti app hackernews/manage.py recreate_db
```

Start fetch news every minute
```Bash
$ docker exec -ti app hackernews/manage.py start_fetching
```

Stop fetch news
```Bash
$ docker exec -ti app hackernews/manage.py stop_fetching
```

Fetch fresh news immediatly
```Bash
$ docker exec -ti app hackernews/manage.py  fetch_fresh_data
```

### API URLs

Swagger info

```/api/v1/swagger.json```

Web UI

```/api/v1/```

Posts

```/api/v1/posts/```

**Example output**

```
...
{
    "id": "64",
    "title": "What the heroin industry can teach us about solar power",
    "url": "https://www.bbc.com/news/science-environment-53450688",
    "created": "2020-07-27T12:30:12.257726",
    "created_hn": "2020-07-27T11:30:12.205959"
},
...
```

### Limit, Offset, Order example

```/api/v1/posts/?limit=10&order=title&offset=3&dir=asc```

**ordering fields:**
id, title, url, created