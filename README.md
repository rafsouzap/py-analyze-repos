# GitLab Stats Analyzer

## Overview

The GitLab Stats Analyzer is a Python-based tool that analyzes GitLab projects and user statistics. It fetches data from the GitLab API, processes it, and provides insights into merge requests, commits, and changes made by users and projects. The tool can also export the analyzed data to CSV files for further analysis.

## Features

- Analyze GitLab projects and user statistics
- Fetch merge requests and commit details
- Export data to CSV files
- Configurable via a YAML configuration file
- Supports multi-threaded processing for faster analysis

## Project Structure
```
.
├── api_utils.py 
├── config.py 
├── exporters.py 
├── gitlab-stats.py 
├── models.py 
├── project.py 
├── requirements.txt 
├── transformers.py 
├── user.py
```

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/gitlab-stats-analyzer.git
    cd gitlab-stats-analyzer
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the script:**

    ```sh
    python gitlab-stats.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD [options]
    ```

    **Options:**

    - `--start-date`: Start date in `YYYY-MM-DD` format
    - `--end-date`: End date in `YYYY-MM-DD` format
    - `--token`: Set GitLab access token
    - `--host`: Set GitLab host
    - `--add-project`: Add a project by URL
    - `--add-user`: Add a user by Username
    - `--mode`: Result analysis mode (projects or users)
    - `--export-csv`: Export data to CSV
    - `--verbose`: Enable verbose logging

2. **Examples:**

    - Add a project:

        ```sh
        python gitlab-stats.py --add-project https://gitlab.com/yourusername/yourproject
        ```

    - Add a user:

        ```sh
        python gitlab-stats.py --add-user yourusername
        ```

    - Analyze projects:

        ```sh
        python gitlab-stats.py --start-date 2023-01-01 --end-date 2023-01-31 --mode projects
        ```

    - Analyze users and export data to CSV:

        ```sh
        python gitlab-stats.py --start-date 2023-01-01 --end-date 2023-01-31 --mode users --export-csv
        ```

## Configuration File

When you start configuring your environment, define the access token, host and other settings, the `config.yaml` file will be created in the project path with the following format:

```yaml
gitlab:
    token: YOUR_GITLAB_ACCESS_TOKEN
    host: https://gitlab.com
    users:
    - user_id: 123
    user_name: john.due
    projects:
    - project_id: 123
    project_name: project-sample
```

- `token`: Your GitLab access token
- `host`: The GitLab host URL
- `users`: List of users to analyze
- `projects`: List of projects to analyze

## Dependencies

The project dependencies are listed in the [`requirements.txt`]("requirements.txt") file:

- [`argparse`](https://pypi.org/project/argparse/")
- [`logging`]("https://pypi.org/project/logging/")
- [`requests`]("https://pypi.org/project/requests/")
- [`tabulate`]("https://pypi.org/project/tabulate/")
- [`tqdm`]("https://pypi.org/project/tqdm/")
- [`PyYAML`]("https://pypi.org/project/PyYAML/")

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
