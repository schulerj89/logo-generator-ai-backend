"""OpenAI service to generate prompts and images using OpenAI's DALL-E and Chat models."""
import os
import json
import logging
from openai import OpenAI
from app.exceptions import InappropriatePromptException

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=openai_api_key)

logging.basicConfig(level=logging.INFO)

def generate_random_prompts():
    """Generate random prompts for the user to choose from."""
    completions = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at generating prompts for Dall-E in JSON. Create 3 different prompts for a user to choose from for a fantasy football mascot logo, ensure you leverage actual mascots from NFL, college or high school teams. Should just be a few words and put it in json format: ['prompt 1', 'prompt 2', 'prompt 3']"}
        ]
    )

    prompts_answer = completions.choices[0].message.content

    # Find the json in the response string and convert it to an array
    start_index = prompts_answer.find("[")
    end_index = prompts_answer.find("]") + 1
    prompts_json = prompts_answer[start_index:end_index]

    if len(prompts_json) < 10:
        return []

    prompts = json.loads(prompts_json)

    return prompts

def generate_image_prompt(user_prompt):
    """Generate a new image prompt based on user input."""
    appropriate_completion = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {"role": "system", "content": "You are an expert at making sure prompts use the appropriate language and fixing them for a fantasy football mascot prompt. If you received a prompt that is not appropriate, fix it into a fantasy football mascot prompt. If you are unable to please return with 'Error: Inappropriate Prompt' and the reason why."},
            {"role": "user", "content": user_prompt}
        ]
    )

    appropriate_answer = appropriate_completion.choices[0].message.content

    if "Error: Inappropriate Prompt" in appropriate_answer:
        logging.info("Error: Inappropriate Prompt: %s", appropriate_answer)
        raise InappropriatePromptException(f"Error: Inappropriate Prompt: {appropriate_answer}")

    prompt = user_prompt + ". Do not include any text. Football Mascot Type Logo. Strictly always use a white background."

    completion = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {"role": "system", "content": "You are an expert at creating prompts for Dall-E. Update the prompt you received so that it is more specific and detailed and used so a user can create a fantasy football logo. Make sure to always use a white background."},
            {"role": "user", "content": prompt}
        ]
    )

    first_prompt = completion.choices[0].message.content

    completion_checker = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {"role": "system", "content": "You are an expert at keeping prompts concise and just a few sentences. Update the prompt you received so that it's simple and to the point. Ensure white background is stricly enforced."},
            {"role": "user", "content": first_prompt}
        ]
    )

    new_prompt = completion_checker.choices[0].message.content

    # Generate image
    images = openai_client.images.generate(
        model="dall-e-3",
        prompt=new_prompt,
        n=1,
        size="1024x1024"
    )
    image_url = images.data[0].url

    return first_prompt, new_prompt, image_url
