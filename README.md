# FastAPI ddd chat boilerplate

### Fastapi chat:


## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)
- [POETRY](https://python-poetry.org/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/pelkoa-glitch/fastapi-chat.git
2. Install all required packages in `Requirements` section.

3. Rename and fill the file `.env.example` with your dependencies

4. Run command
    ```bash
        cd fastapi-chat -  go to project folder
        poetry install  -  install dependencies
        poetry shell    -  activate python venv
        make app        -  run app container

5. Api docs on http://localhost:8000/api/docs

### Implemented Commands

* `make app` - up app container
* `make app-logs` - follow the logs in app container
* `make app-down` - down app container
* `make app-console` - open app container console
* `make test` - run tests in app container
