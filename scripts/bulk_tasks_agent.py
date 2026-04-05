import os
import sys
import pyperclip
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from typing import Optional, Any, List
from docling.document_converter import DocumentConverter
from openai import OpenAI
from pydantic import BaseModel, Field
import datetime
# Environment variables
NOTES_DIR = os.getenv("NOTES_DIR")
AUTOMATION_DIR = os.getenv("AUTOMATION_DIR")
BLOG_DIR = os.getenv("BLOG_POSTS_PATH")


AGENT_PROMPT = f"""You are a helpful assistant that takes in one or multiple tasks that involve, searching the web,
                reading papers, writing files and reading files.
                When given a task that involves looking through the user's notes you should consider they are located here:
                {NOTES_DIR}.
                If given a task that involves reviewing or looking through your automations, your automations folder is located at:
                {AUTOMATION_DIR}.
                If a task requires reading MY OWN blog posts (not blog posts from web articles!) you should consider my blog posts are saved here:
                {BLOG_DIR}. 
                When a task involves necessarily retrieving or reading specific information from a pdf you will always 
                use first use the search_tool to find the correct paper and fetch its url, then, you will use the download_and_load_pdf tool to actually download and read the paper so that you can provide
                always a grounded response.
                For ANY task you are required to do you will write it to a file with a title with that reminds the task 
                using words separated by '-'. This file should be saved in the folder ./agent_outputs
                """
                
EXTRACTION_SYS_PROMPT = "You are an expert task list/actionables extractor."

PROMPT_EXTRACT_TASKS = """
    As you can see, I mentioned several items such as taking notes on this and taking notes on that. 
    Please create a bullet point list of all the "take notes" parts from this rough draft. 
    This will help me separate them create tasks to address those problems, review the information, 
    research further, and so on.
    """

class Actionables(BaseModel):
    tasks: List[str] = Field(
        description="List of extracted tasks",
        default_factory=list
    )

def extract_actionables(prompt: str) -> Actionables:
    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": EXTRACTION_SYS_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        response_format=Actionables
    )
    return response.choices[0].message.parsed

def human_filter_out_tasks(task_list: List) -> List:
    for i,t in enumerate(task_list):
        print(f"Task: {i} - {t}")
        print("****")
    
    filter_tasks = input("Select the tasks to remove as a comma separated list (e.g 1,3,6, etc...).")
    
    if filter_tasks.strip():
        indices_to_remove = [int(idx.strip()) for idx in filter_tasks.split(',')]
        filtered_list = [task for i, task in enumerate(task_list) if i not in indices_to_remove]
        return filtered_list
    
    return task_list

def download_and_load_pdf(pdf_path_or_url: str) -> str:
    """
    Downloads and converts a PDF file to markdown format.
    
    Args:
        pdf_path_or_url (str): Path to local PDF file or URL to download PDF from
        
    Returns:
        str: The PDF content converted to markdown format
        
    Note:
        Uses DocumentConverter to handle both local files and URLs
    """
    converter = DocumentConverter()
    result = converter.convert(pdf_path_or_url)
    return result.document.export_to_markdown()

def search_tool(query: str) -> Optional[dict[str, Any]]:
    """
    Performs a web search using Tavily Search API.
    
    Args:
        query (str): Search query string
        
    Returns:
        Optional[dict[str, Any]]: Search results dictionary containing up to 10 results,
        or None if search fails
        
    Note:
        Uses general topic search with max 10 results
    """
    search = TavilySearch(max_results=10, topic="general")
    return search.invoke(query)

def write_file(contents: str, file_path: str) -> str:
    """
    Writes content to a file with a timestamped filename.
    
    Args:
        contents (str): Content to write to file
        file_path (str): Base path for the file
        
    Returns:
        str: Success message with timestamped filename or error message
        
    Note:
        Automatically adds timestamp to filename in format YYYYMMDD_HHMMSS
    """
    try:
        # Add timestamp to filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Split path into directory, filename and extension
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        base_name, ext = os.path.splitext(filename)
        
        # Construct new path with timestamp
        timestamped_path = os.path.join(directory, f"{base_name}_{timestamp}{ext}")
        
        with open(timestamped_path, 'w', encoding='utf-8') as f:
            f.write(contents)
        return f"Successfully wrote to {timestamped_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

def read_file(file_path: str) -> str:
    """
    Reads and returns the contents of a file.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: File contents or error message if read fails
        
    Note:
        Uses UTF-8 encoding for reading
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def list_files(folder_path: str) -> str:
    """
    Lists all files in a directory.
    
    Args:
        folder_path (str): Path to the directory to list files from
        
    Returns:
        str: Newline-separated list of filenames or error message if listing fails
    """
    try:
        files = os.listdir(folder_path)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"

def create_agent():
    return create_react_agent(
        model="gpt-4.1",
        tools=[search_tool, download_and_load_pdf, write_file, read_file, list_files],
        prompt=AGENT_PROMPT,
    )

def main():
    transcription = sys.stdin.read()

    actionables_list = extract_actionables(transcription + "\n\n" + PROMPT_EXTRACT_TASKS)
    # filtered_tasks = human_filter_out_tasks(actionables_list.tasks)
    # print(f"Filtered tasks\n\n: {filtered_tasks}")
    # Create agent and process tasks
    agent = create_agent()
    for task in actionables_list.tasks:
        print(f"\nProcessing task: {task}")
        response = agent.invoke({"messages": [task]})
        print(f"Response: {response['messages'][-1]}")

if __name__ == "__main__":
    main()
