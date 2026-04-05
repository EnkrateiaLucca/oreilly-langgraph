import sys
import pyperclip
from openai import OpenAI
client = OpenAI()

MODEL_VIDEO_DESCR = "gpt-4.1"
MODEL_VIDEO_CHAPTERS = "gpt-4o"
SYS_MSG_CHAPTERS = """
You are a helpful content creator assistant that generates accurate chapter sections for youtube videos.
You will write a chapter section with timeline stamps for the major parts of the video. You should initiate 
the section with 
'''📚 Chapters:'''

and the format should be:
 <double:digit timestamp> - <brief description of this section>
"""
SYS_MSG_DESCR = """
You are a helpful content creator assistant that generates accurate youtube video descriptions 
containing witty insightful and proper content given a transcription of a video containing its timestamps.
You write a very small paragraph, to the point.
"""

def generate_video_description(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_VIDEO_DESCR,
        messages=[{"role": "system", "content": SYS_MSG_DESCR},
                  {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def generate_video_chapters(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_VIDEO_CHAPTERS,
        messages=[{"role": "system", "content": SYS_MSG_CHAPTERS},
                  {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def concatenate_final_video_description(youtube_video_description: str, youtube_chapter_section: str) -> str:
    full_video_description = f"""
        {youtube_video_description}.

        {youtube_chapter_section}

        🔗 Links:

        - Subscribe!: https://www.youtube.com/channel/UCu8WF59Scx9f3H1N_FgZUwQ
        - Tiktok: https://www.tiktok.com/@enkrateialucca?lang=en
        - Twitter: https://twitter.com/LucasEnkrateia
        - LinkedIn: https://www.linkedin.com/in/lucas-soares-969044167/
        - AI project tracker from Ben's Bites: https://bensbites.beehiiv.com/subscribe?ref=CoXhc4I0c0

        Support the Channel!

        - Buy me a cup of coffee: https://tr.ee/7tYsD-tUu2
        - Paypal: https://paypal.me/lucasenkrateia?country.x=PT&locale.x=pt_PT
        """
        
    return full_video_description

def write_video_description_to_file(video_description: str, filename: str = "youtube_description.txt") -> None:
    """
    Write the generated video description to a file.
    
    Args:
        video_description (str): The complete video description to write
        filename (str): The name of the file to write to (default: youtube_description.txt)
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(video_description)
        print(f"Video description saved to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

    

video_transcription=pyperclip.paste()

prompt1 = f"""
Given this video transcription: {video_transcription} you will write a Youtube 
description paragraph describing what is covered in the video in a nice and easy tone.
The output should ONLY BE THE description and nothing else.
Output video description:\n
"""

prompt2 = f"""
Given this youtube video transcription:
{video_transcription}
You will write a chapter section with timeline stamps for the major parts of the video. You should initiate 
the section with 
'''📚 Chapters:'''

and the format should be:
 <double:digit timestamp> - <brief description of this section>
"""

youtube_video_description = generate_video_description(prompt1)

youtube_chapter_section = generate_video_chapters(prompt2)

full_video_description = concatenate_final_video_description(youtube_video_description, youtube_chapter_section)

print(full_video_description)

write_video_description_to_file(full_video_description)

print("Copied to your clipboard")

pyperclip.copy(full_video_description)