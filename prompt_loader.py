"""Utility module for loading prompt templates from markdown files."""

import os
from pathlib import Path


def load_prompt(prompt_path):
    """
    Load a prompt from a markdown file.
    
    Args:
        prompt_path: Relative path to the prompt file from the prompts directory
        
    Returns:
        The content of the markdown file as a string
    """
    base_dir = Path(__file__).parent
    file_path = base_dir / "prompts" / prompt_path
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {file_path}")


def load_agent_prompt(agent_name):
    """Load agent configuration (role, goal, backstory) from markdown file."""
    content = load_prompt(f"agents/{agent_name}.md")
    
    # Parse markdown sections
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line.replace("## ", "").strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections


def load_task_prompt(task_name, assessment_data_str=None):
    """
    Load task description from markdown file.
    
    Args:
        task_name: Name of the task file (without .md extension)
        assessment_data_str: Optional assessment data to insert into the prompt
        
    Returns:
        Dictionary with 'description' and 'expected_output' keys
    """
    content = load_prompt(f"tasks/{task_name}.md")
    
    # Parse markdown sections
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line.replace("## ", "").strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()
    
    # Replace placeholder with assessment data if provided
    description = sections.get("Description", "")
    if assessment_data_str and "{ASSESSMENT_DATA}" in description:
        description = description.replace("{ASSESSMENT_DATA}", assessment_data_str)
    
    return {
        "description": description,
        "expected_output": sections.get("Expected Output", "")
    }


def load_output_format(task_name):
    """Load expected output format example for a task."""
    return load_prompt(f"output_formats/{task_name}_output.md")
