import logging
import api_utils
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate
from tqdm import tqdm
from config import Config

class ProjectNotFoundException(Exception):
    """Custom exception for when project is not found"""
    pass

class Project:
    def __init__(self, config: Config, logger: logging.Logger):
        self.__config = config
        self.__logger = logger
        self.__logger.info('Project instance created with provided config.')

    def __get_project_info(self, project_url) -> tuple[int, str]:
        headers = {'PRIVATE-TOKEN': self.__config.get_token()}
        params = {'search': project_url.split('/')[-1]}
        url = f'{self.__config.get_host()}/api/v4/projects'

        try:
            projects = api_utils.get_request(url, headers, params, self.__logger)
            if projects:
                for project in projects:
                    if project['web_url'] == project_url:
                        self.__logger.info(f"Project found: {project['name']} with ID: {project['id']}")
                        return project['id'], project['name']
            else:
                raise ProjectNotFoundException(f"Project not found for URL: {project_url}")
        except Exception as e:
            self.__logger.error(f'An unexpected error occurred: {e}')
            raise
        return None, None
    
    def __analyze_commits_by_project(self, project_id, start_date, end_date):
        headers = {'PRIVATE-TOKEN': self.__config.get_token()}
        params = {
            'since': start_date, 
            'until': end_date, 'with_stats': 'true'
        }
        changes = 0
        url = f'{self.__config.get_host()}/api/v4/projects/{project_id}/repository/commits'

        try:
            commits = api_utils.get_request(url, headers, params, self.__logger)
            for commit in commits:
                changes += commit['stats']['total']
        except Exception as e:
            self.__logger.error(f'Error analyzing commits: {e}')
        return changes
    
    def __process_project(self, project, start_date, end_date):
        project_id = project['project_id']
        project_name = project.get('project_name', 'Unknown')
        try:
            changes = self.__analyze_commits_by_project(project_id, start_date, end_date)
            return project_id, project_name, changes
        except Exception as e:
            print(f'Error processing project {project_id}: {e}')
            return project_id, project_name, 0
   
    def projects_stats(self, start_date: str, end_date: str):
        projects = self.__config.get_config(['gitlab', 'projects'])

        results = []
        total_changes = 0
        max_thread_workers = 10

        with ThreadPoolExecutor(max_workers=max_thread_workers) as executor:
            futures = {executor.submit(self.__process_project, project, start_date, end_date): project for project in projects}

            with tqdm(total=len(futures), desc='Analyzing projects') as pbar:
                for future in as_completed(futures):
                    project_id, project_name, changes = future.result()
                    results.append([project_id, project_name, changes])
                    total_changes += changes
                    pbar.update(1)

        results.append(['Total', '', total_changes])
        print(f'\n{tabulate(results, headers=["Project ID", "Project Name", "Changed Lines"], tablefmt="grid")}')

    def add_project(self, url: str):
        self.__logger.info(f'Adding repository for URL: {url}')
        try:
            project_id, project_name = self.__get_project_info(url)
            self.__config.append_to_list(['gitlab','projects'], {'project_id': project_id, 'project_name': project_name})
            self.__logger.info(f'Project added: {project_name} with ID: {project_id}')
        except ProjectNotFoundException:
            print(f'Project not found for URL: {url}')
        except Exception as e:
            self.__logger.error(f'Failed to add project for URL: {url} due to an error: {e}')