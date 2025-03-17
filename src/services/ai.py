from typing import Optional
import google.generativeai as genai
from google.generativeai.types import (
    AsyncGenerateContentResponse,
    GenerationConfig,
)
from google.generativeai.generative_models import GenerativeModel
from src.conf.config import settings


def setup_gemini():
    api_key = settings.google_api_key
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    genai.configure(api_key=api_key)

    generation_config = GenerationConfig(
        temperature=0.7,
        top_p=0.8,
        top_k=40,
        max_output_tokens=1024,
    )

    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    return model


async def generate_summary(content: str, model: Optional[GenerativeModel] = None) -> Optional[str]:
    try:
        if not model:
            model = setup_gemini()
            
        prompt = f"""Please provide a summary of the following text.
                Focus on the main points and key ideas.
                Keep the summary concise yet informative.

        Text for processing:
        {content}

        Summary:"""
        
        response: AsyncGenerateContentResponse = await model.generate_content_async(
            prompt,
            stream=False
        )
        
        if response.text:
            return response.text.strip()
        return None
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None
