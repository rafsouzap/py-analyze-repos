import logging
import api_utils
import transformers
import exporters
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate
from tqdm import tqdm
from datetime import datetime
from config import Config

class UserNotFoundException(Exception):
    """Custom exception for when user is not found"""
    pass

class User:
    def __init__(self, config: Config, logger: logging.Logger):
        self.__config = config
        self.__logger = logger
        self.__logger.info('User instance created with provided config.')

    def __get_user_info(self, username) -> tuple[int, str]:
        headers = {'PRIVATE-TOKEN': self.__config.get_token()}
        params = {'username': username}
        url = f'{self.__config.get_host()}/api/v4/users'

        try:
            users = api_utils.get_request(url, headers, params, self.__logger)
            if users:
                self.__logger.info(f"User found: {users[0]['username']} with ID: {users[0]['id']}")
                return users[0]['id'], users[0]['username']
            else:
                raise UserNotFoundException(f"User not found for username: {username}")
        except Exception as e:
            self.__logger.error(e)
            raise
    
    def __get_merge_requests_by_user(self, user_id: int, start_date: str, end_date: str) -> list:
        headers = {'PRIVATE-TOKEN': self.__config.get_token()}
        params = {
            'author_id': user_id, 
            'created_after': start_date, 
            'created_before': end_date, 
            'scope': 'all', 
            'per_page': '30',
            'state': 'merged'
        }
        all_merges = []
        page = 1

        with tqdm(desc='Fetching Merge Requests', unit=' merge requests', leave=False) as merge_pbar:
            while True:
                params['page'] = page
                url = f'{self.__config.get_host()}/api/v4/merge_requests'
                try:
                    merges = api_utils.get_request(url, headers, params, self.__logger)
                    if not merges:
                        break
                    all_merges.extend(merges)
                    page += 1
                    merge_pbar.update(len(merges))
                except Exception as e:
                    self.__logger.error(f'Error analyzing commits: {e}')
                    break
            
        return all_merges

    def __get_merge_requests_commit_detail(self, merges: list) -> list:
        headers = {'PRIVATE-TOKEN': self.__config.get_token()}
        all_commits = []

        with tqdm(total=len(merges), desc='Processing Merge Requests', leave=False) as commit_pbar:
            for merge in merges:
                project_id = merge['project_id']
                merge_commit_sha = merge['merge_commit_sha']
                params = {'stats': 'true'}
                url = f'{self.__config.get_host()}/api/v4/projects/{project_id}/repository/commits/{merge_commit_sha}'

                try:
                    commit = api_utils.get_request(url, headers, params, self.__logger)
                    if not commit:
                        break
                    all_commits.append(commit)
                except Exception as e:
                    self.__logger.error(f'Error analyzing commits: {e}')
                    break

                commit_pbar.update(1)
        return all_commits
    
    def __process_user(self, user, start_date, end_date, export_csv=False, filename=''):
        user_id = user['user_id']
        user_name = user['user_name']
        merges = self.__get_merge_requests_by_user(user_id, start_date, end_date)
        changes = self.__get_merge_requests_commit_detail(merges)

        user_data = transformers.transform_merge_requests(user_id, user_name, merges, changes)

        exporters.user_data_to_csv(user_data, filename, export_csv)

        total_merge_requests = len(merges)
        total_changes = sum(merge_request.commit.stats.total for merge_request in user_data.merge_request)

        return user_id, user_name, total_merge_requests, total_changes
          
    def users_stats(self, start_date: str, end_date: str, export_csv: bool = False):
        users = self.__config.get_config(['gitlab', 'users'])

        results = []
        total_merges = 0
        total_changes = 0
        max_thread_workers = 10
        filename = ''

        if export_csv:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            filename = f"user_data_{timestamp}.csv"

        with ThreadPoolExecutor(max_workers=max_thread_workers) as executor:
            futures = {
                executor.submit(self.__process_user, user, start_date, end_date, export_csv, filename): 
                    user for user in users
            }

            with tqdm(total=len(futures), desc='Getting users stats', leave=False) as user_pbar:
                for future in as_completed(futures):
                    try:
                        user_id, user_name, merges, changes = future.result()
                        results.append([user_id, user_name, merges, changes])
                        total_merges += merges
                        total_changes += changes
                        user_pbar.update(1)
                    except Exception as e:
                        self.__logger.error(f'Error processing user: {e}')

        results.append(['Total', '', total_merges, total_changes])
        print(f'\n{tabulate(results, headers=["User ID", "User Name", "MRs", "Changed Lines"], tablefmt="grid")}')

    def add_user(self, username: str):
        self.__logger.info(f'Adding user for Username: {username}')

        try:
            user_id, user_name = self.__get_user_info(username)
            self.__config.append_to_list(['gitlab','users'], {'user_id': user_id, 'user_name': user_name})
            self.__logger.info(f'User added: {user_name} with ID: {user_id}')
        except UserNotFoundException:
            print(f'User not found for username: {username}')
        except Exception as e:
            self.__logger.error(f'Failed to add user for Username: {username} due to an error: {e}')