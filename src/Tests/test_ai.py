import pytest
from unittest.mock import patch, AsyncMock

from src.conf.config import settings
from src.services.ai import setup_gemini, generate_summary
from google.generativeai.generative_models import GenerativeModel


@pytest.mark.asyncio
async def test_model_response():
    model = setup_gemini()
    prompt = "Write a brief summary about the importance of programming."

    response = await model.generate_content_async(prompt)
    print(response.text)
    assert response.text is not None
    assert len(response.text) > 0


@pytest.mark.asyncio
async def test_setup_gemini():

    with patch("src.services.ai.genai.configure") as mock_configure:
        model = setup_gemini()
        mock_configure.assert_called_once_with(
            api_key=settings.google_api_key
        )
        assert model is not None
        assert isinstance(model, GenerativeModel)


@pytest.mark.asyncio
async def test_generate_summary_success():
    mock_model = AsyncMock()
    mock_response = AsyncMock()
    mock_response.text = "This is a summary."
    mock_model.generate_content_async.return_value = mock_response

    with patch("src.services.ai.setup_gemini", return_value=mock_model):
        summary = await generate_summary(
            "This is the content to summarize.", model=mock_model
        )

        assert summary == "This is a summary."
        mock_model.generate_content_async.assert_called_once()


