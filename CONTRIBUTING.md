## Basic guidelines

All code should be submitted by pull-request and follow these simple guidelines:

- Fork the repository and clone your fork locally.
- Create a new branch for your work (e.g., `feature/awesome-feature`).
- Ensure your branch is up to date with the `main` branch.
- Provide a clear description of the changes you're proposing, along with any issues this PR resolves.
- Verify that all tests pass and that no linting errors are present.
- If adding new functionality, write new tests in the `tests/` directory to cover this code.
- Code standards are defined as linting and formatting rules.
- Submit your pull request for review.


# Developing

## Local Setup
1. Install runtime requirements:
    ```bash
    sudo apt-get update
    sudo apt-get install docker-compose
    sudo usermod -aG docker $USER
    newgrp docker
    ```

2. Clone the repository and navigate to project directory:
    ```bash
    git clone https://github.com/mhiland/SignalEye.git
    cd signaleye
    ```

3. Install required dependencies:
    ```bash
    sudo pip install -r requirements.txt
    pre-commit install
    ```

## Docker

### Docker Compose
Run the project using Docker Compose:

```bash
docker-compose up -d
```

If wanting to change the wireless interface use environment variable, wlan=1 == wlan1. default: 0

```bash
wlan=1 docker-compose up -d --build
```

### Docker Debug

To access the running Docker container for troubleshooting:

```bash
docker exec -it signal_eye_container /bin/bash
```



## Testing

To run tests using pytest:

```bash
pytest
```

## Code Linting

Use pylint for code linting:

```bash
pylint $(git ls-files '*.py')
```

## Autopep8 for Formatting

Use `autopep8` to fix trailing whitespace and PEP8 formatting issues:

```bash
autopep8 --in-place --aggressive --aggressive --recursive .
```

## Pre-Commit Validation

Run pre-commit checks across all files:

```bash
pre-commit run --all-files
```
