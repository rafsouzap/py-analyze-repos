from models import User, MergeRequest, Commit, Stats

def transform_merge_requests(user_id, user_name, merge_requests_payload, commits_payload):
    merge_requests = []
    
    for merge_request in merge_requests_payload:
        commit_data = next((commit for commit in commits_payload if commit['id'] == merge_request['merge_commit_sha']), None)
        
        if commit_data:
            stats = Stats(
                additions=commit_data['stats']['additions'],
                deletions=commit_data['stats']['deletions'],
                total=commit_data['stats']['total']
            )
            
            commit = Commit(
                id=commit_data['id'],
                title=commit_data['title'],
                stats=stats
            )
            
            merge_request_obj = MergeRequest(
                id=merge_request['id'],
                project_id=merge_request['project_id'],
                title=merge_request['title'],
                state=merge_request['state'],
                merge_commit_sha=merge_request['merge_commit_sha'],
                reference=merge_request['references']['full'],
                created_at=merge_request['created_at'],
                merged_at=merge_request['merged_at'],
                prepared_at=merge_request['prepared_at'],
                commit=commit
            )
            
            merge_requests.append(merge_request_obj)
    
    user = User(
        user_id=user_id,
        user_name=user_name,
        merge_request=merge_requests
    )
    
    return user