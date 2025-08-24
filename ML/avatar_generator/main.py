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
    

    """
        Saves processed profile image to storage
        
        Args:
            image_data: Processed image bytes
            user_id: User ID for filename
            
        Returns:
            File path or None if failed
    """
    async def save_profile_image(self, image_data: bytes, user_id: str) -> Optional[str]:

        try: 

            # Creating file path if doesn't already exist
            profile_dir = "backend/data/profile_images"
            os.makedirs(profile_dir, exist_ok=True)


            # Generate unique file name
            # %Y%m%d_%H%M%S is the format of the timestamp
            # % Y % m % d _ % H % M % S

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"profile_{user_id}_{timestamp}.png"
            filepath = os.path.join(profile_dir, filename)

            # Saving image
            # wb - write binary

            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(image_data)

            return f"Saved your image at {filepath}"
        
        except Exception as e:
            print(f"Error saving image {e}")
            return None
        


    """
        Generates image using Hugging Face Stable Diffusion API
        
        Args:
            prompt: Text description of desired image
            negative_prompt: What to avoid in the image
        
        Returns:
            Image data as bytes or None if failed
        """
    async def generate_image(self, prompt: str, negative_prompt: Optional[str] = None) -> Optional[bytes]:
        try:

            if not negative_prompt:
                negative_prompt = "blurry, low quality, distorted, ugly, bad anatomy, extra limbs"

            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": negative_prompt,
                    "num_inference_steps": 20,  # Lower for faster generation
                    "guidance_scale": 7.5,      # How closely to follow prompt
                    "width": 512,               # Generation size
                    "height": 512
                }
            }

            # Making API request
            response = requests.post(
                self.api_url, 
                headers=self.headers,
                json=payload,
                timeout=60 # 60 seconds
            )

            if response.status_code == 200:
                return response.content

            else:
                print(f"API Error: {response.status_code}, {response.text}")
                return None


        except Exception as e:
            print(f"Error generating image: {e}")
            return None
        


    """
        Processes generated image for use as profile picture:
        - Converts to square format
        - Resizes to profile dimensions
        - Optimizes file size
        
        Args:
            image_data: Raw image bytes from API
            
        Returns:
            Processed image bytes or None if failed
    """
    def process_image_for_profile(self, image_data:bytes) -> Optional[bytes]:

        try:
            
            # Open image from bytes
            image = Image.open(io.BytesIO(image_data))


            # If image is not in RGB format convert it
            if image.mode != 'RGB':
                image = image.convert('RGB')

            width, height = image.size()

            min_dimensions = min(width, height)


            # Calculating crop box that is centered on the image
            # If the image is wider than tall, then need to trim left and right side
            # If the image is taller though, then need to trim the top and bottom

            # Example: If image is 400×250
            # min_dimensions = min(400, 250) => 250
            # left = (400 - 250) // 2 = 75
            # top = (250 - 250) // 2 = 0
            # right = 75 + 250 = 325
            # bottom = 0 + 250 = 250
            # So it crops out a 250×250 square centered in the image
            
            left = (width - min_dimensions) // 2
            top = (height - min_dimensions) // 2
            
            right = (left + min_dimensions)
            bottom = (top + min_dimensions)

            image = image.crop((left, top, right, bottom))

            image = image.resize(self.profile_size, Image.Resampling.LANCZOS)


            # Optional border

            output_buffer = io.BytesIO()

            image.save(
                output_buffer,
                format='PNG',
                optimize=True,
                quality=85
            )

            return output_buffer.getvalue()
        


        except Exception as e:
            print(f"Error processing image: {e}")
            return None





         
    
    """
        Profile picture generation
        
        Args:
            user_description: What the user wants in their profile picture
            user_id: User ID for saving and database updates
            style: Art style preference
            
        Returns:
            Dictionary with generation results
        """
    async def generate_profile_picture(
            self,
            user_description:str,
            user_id:str,
            style:str = "cartoon",
            ) -> Dict[str, Any]:
        

        try:

            print(f"Start profile picture generation for {user_id}")


            # Step 1 prompting
            prompt = self.create_prompt(user_description=user_description, style=style)

            print(f"Generated Prompt: {prompt}")


            # Step 2 generate image
            print(f"Generating Image")
            raw_image_data = await self.generate_image(prompt)

            if not raw_image_data:
                return {
                    "success": False,
                    "error": "Failed to generate image",
                    "filepath": None
                }

            print(f"Process image data for profile picture")
            processed_image_data = self.process_image_for_profile(raw_image_data)


            if not processed_image_data:
                return {
                    "success": False,
                    "error": "Failed to process image",
                    "filepath": None
                }

            
            # Step 4 save image
            filepath = self.save_profile_image(processed_image_data, user_id=user_id)

            if not filepath: 
                return {
                    "success": False,
                    "error": "Failed to save image",
                    "filepath": None
                }
            
            print(f"Successfully generated profile picture: {filepath}")


            return {
                "success": True,
                "filepath": filepath,
                "prompt_used": prompt,
                "style": style,
                "generated_at": datetime.now().isoformat(),
                "file_size": len(processed_image_data)
            }
        

        except Exception as e:
            print(f"Error in profile picture generation: {e}")
            return {
                "success": False,
                "error": str(e),
                "filepath": None
            }

