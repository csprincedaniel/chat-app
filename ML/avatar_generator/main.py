import requests
# Tool for handling data flow
import io

# Encodes/Decodes data
import base64

from PIL import Image, ImageOps

from typing import Optional, Dict, Any

import json

# For asynchronous task
import asyncio

# For async file operation
import aiofiles

import os 
from datetime import datetime

# For environment variables like keys
from dotenv import load_dotenv

load_dotenv("ML/constants.env")
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


class ProfilePictureGenerator:

    def __init__(self):

        # Hugging face API endpoint 
        self.api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

        # For API request will have the key for Hugging face in it
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', HF_API_KEY)}"
        }

        # Profile picture specifications 

        self.profile_size = (256, 256)

        self.supported_formats = ['PNG', 'JPEG']

        # Predefined style prompts 
        self.style_templates = {
            "cartoon": "cartoon style, animated, colorful, disney style, {prompt}",
            "realistic": "photorealistic, high quality, detailed, {prompt}",
            "anime": "anime style, manga art, japanese animation, {prompt}",
            "cyberpunk": "cyberpunk style, neon colors, futuristic, {prompt}",
            "fantasy": "fantasy art, magical, ethereal, digital painting, {prompt}",
            "minimalist": "minimalist art, simple, clean lines, {prompt}"
        }


    """
        Creates an optimized prompt for profile picture generation
        
        Args:
            user_description: What the user wants in their profile picture
            style: Art style from our predefined templates
        
        Returns:
            Formatted prompt string
    """
    def create_prompt(self, user_description: str, style: str = "cartoon") -> str:

        # This will try to get the style_template specificed by the user but if it doesn't exist then 
        # use the cartoon as a default one.
        style_template = self.style_templates.get(style, self.style_templates["cartoon"])


        # Add the user's specificed description of their desired profile picture into the
        # prompt that will be used to generate a profile picture.
        base_prompt = self.style_templates.format(prompt=user_description)

        
        # Adding specific wording to the prompt to emphasize that the image will be used for a profile picture.
        profile_modifiers = "profile picture, headshot, centered, clean background, high quality"

        full_prompt = f"{base_prompt}, {profile_modifiers}"

        return full_prompt