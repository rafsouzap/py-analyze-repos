import argparse
import logging
from tabulate import tabulate
from config import Config
from project import Project
from user import User

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.CRITICAL + 1
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger

def main():
    parser = argparse.ArgumentParser(description='Script to analyze GitLab projects commits.')
    parser.add_argument('--start-date', type=str, help='start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str, help='snd date in YYYY-MM-DD format')
    parser.add_argument('--token', type=str, help='set GitLab access token')
    parser.add_argument('--host', type=str, help='set GitLab host')
    parser.add_argument('--add-project', dest='project', type=str, help='add a project by URL')
    parser.add_argument('--add-user', dest='user', type=str, help='add a user by Username')
    parser.add_argument('--mode', choices=['projects', 'users'], default='projects', help='result analysis mode')
    parser.add_argument('--export-csv', action='store_true', help='export data to CSV')
    parser.add_argument('--verbose', action='store_true', help='enable verbose logging.')

    args = parser.parse_args()
    config = Config(file_path='config.yaml')
    logger = setup_logging(args.verbose)

    project = Project(config=config, logger=logger)
    user = User(config=config, logger=logger)

    if args.token:
        config.set_token(args.token)
    elif args.host:
        config.set_host(args.host)
    elif args.project:
        project.add_project(url=args.project)
    elif args.user:
        user.add_user(username=args.user)
    else:
        if not args.start_date or not args.end_date:
            print('Please provide the start and end dates')
            exit(1)
        
        start_date = f"{args.start_date}T00:00:00Z"
        end_date = f"{args.end_date}T23:59:59Z"

        if args.mode == 'projects':
            project.projects_stats(start_date=start_date, end_date=end_date)
        elif args.mode == 'users':
            user.users_stats(start_date=start_date, end_date=end_date, export_csv=args.export_csv)
        
if __name__ == '__main__':
    main()