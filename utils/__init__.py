import os

from dotenv import load_dotenv


def get_env_var(var_name:str) -> str:
    """
    Load environment variables from a .env file.

    Args:
        env_file (str, optional): Path to the environment variables file.
                                  Defaults to '.env'.
    """
    if not os.getenv("ENV_LOADED"):
        os.environ["ENV_LOADED"] = "1"
        load_dotenv()

    return os.getenv(var_name)


def get_project_root():
    """
    Returns the absolute path to the project root directory.

    Returns:
        str: Absolute path of the project root directory.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))