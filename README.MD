# GitLab Stats Analyzer

## Overview

The GitLab Stats Analyzer is a Python-based tool designed to analyze GitLab projects and user statistics. It fetches data from the GitLab API, processes it, and provides insights into merge requests, commits, and changes made by users and projects. The tool can also export the analyzed data to CSV files for further analysis.

## Features

- Analyze GitLab projects and user statistics.
- Fetch merge requests and commit details.
- Export data to CSV files.
- Configurable via a YAML configuration file.
- Supports multi-threaded processing for faster analysis.

## Project Structure
. ├── pycache/ ├── .gitignore ├── api_utils.py ├── config.py ├── config.yaml ├── exporters.py ├── gitlab-stats.py ├── models.py ├── project.py ├── requirements.txt ├── transformers.py ├── user_data_*.csv ├── user.py
