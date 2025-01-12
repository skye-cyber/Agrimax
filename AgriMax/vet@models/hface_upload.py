from huggingface_hub import HfApi

api = HfApi()
api.upload_file(
    path_or_fileobj="/path/to/your/large_file.ext",
    path_in_repo="large_file.ext",
    repo_id="username/my-model",
    repo_type="model"
)
