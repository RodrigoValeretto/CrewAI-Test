"""Utility module for loading prompt templates from YAML files."""

import os
from pathlib import Path
import yaml


def load_yaml_file(yaml_path):
    """
    Load content from a YAML file.

    Args:
        yaml_path: Relative path to the YAML file from the prompts directory

    Returns:
        The parsed YAML content as a dictionary
    """
    base_dir = Path(__file__).parent
    file_path = base_dir / "prompts" / yaml_path

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {file_path}: {e}")


def load_agent_prompt_yaml(agent_name):
    """Load agent configuration (role, goal, backstory) from YAML file."""
    content = load_yaml_file(f"agents/{agent_name}.yaml")

    return {
        "Role": content.get("role", ""),
        "Goal": content.get("goal", ""),
        "Backstory": content.get("backstory", ""),
    }


def load_task_prompt_yaml(task_name, assessment_data_str=None):
    """
    Load task description from YAML file.

    Args:
        task_name: Name of the task file (without .yaml extension)
        assessment_data_str: Optional assessment data to insert into the prompt

    Returns:
        Dictionary with 'description' and 'expected_output' keys
    """
    content = load_yaml_file(f"tasks/{task_name}.yaml")

    description = content.get("description", "")
    if assessment_data_str and "{ASSESSMENT_DATA}" in description:
        description = description.replace("{ASSESSMENT_DATA}", assessment_data_str)

    return {
        "description": description,
        "expected_output": content.get("expected_output", ""),
    }



