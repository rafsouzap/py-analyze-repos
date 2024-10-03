import csv
import os
from models import User

def user_data_to_csv(user_data: User, filename: str, export: bool):
    if not export:
        return
    
    file_exists = os.path.exists(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow([
                'user_id', 'user_name', 'merge_request_id', 'project_id', 'title', 'state', 
                'created_at', 'merged_at', 'prepared_at', 'merge_commit_sha', 'reference', 
                'commit_id', 'commit_title', 'additions', 'deletions', 'total'
            ])
        
        for merge_request in user_data.merge_request:
            writer.writerow([
                user_data.user_id,
                user_data.user_name,
                merge_request.id,
                merge_request.project_id,
                merge_request.title,
                merge_request.state,
                merge_request.created_at,
                merge_request.merged_at,
                merge_request.prepared_at,
                merge_request.merge_commit_sha,
                merge_request.reference,
                merge_request.commit.id,
                merge_request.commit.title,
                merge_request.commit.stats.additions,
                merge_request.commit.stats.deletions,
                merge_request.commit.stats.total
            ])
