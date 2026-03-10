# Vision Models Guide

Socrates Nexus supports vision models that can analyze and understand images. This guide shows you how to use vision capabilities with multiple LLM providers.

## Overview

Vision models allow your LLM to:
- Analyze images from URLs or local files
- Process base64-encoded image data
- Understand visual content and answer questions about images
- Compare multiple images
- Extract information from images

## Supported Providers

- **Anthropic Claude 3.5 Sonnet** - Advanced vision capabilities
- **OpenAI GPT-4 Vision** - Multi-modal understanding
- **Google Gemini Vision** - Multimodal analysis

## Basic Usage

### Analyzing an Image from URL

```python
from socrates_nexus import LLMClient

client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

response = client.chat(
    "What's in this image?",
    images=["https://example.com/image.jpg"]
)

print(response.content)
```

### Analyzing a Local Image

```python
client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

response = client.chat(
    "Describe this image",
    images=["./path/to/image.jpg"]
)

print(response.content)
```

### Processing Base64 Images

```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = client.chat(
    "What do you see?",
    images=[image_data]
)
```

## Advanced Features

### Multiple Images

Compare or analyze multiple images in one request:

```python
response = client.chat(
    "Compare these images. What are the differences?",
    images=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
)
```

### Image Detail Levels

Control analysis depth (provider-dependent):

```python
from socrates_nexus.models import ImageContent

image = ImageContent(
    source="https://example.com/image.jpg",
    detail="high"  # "low" for faster processing, "high" for detailed analysis
)
```

### Image Utilities

Socrates Nexus provides utilities for image handling:

```python
from socrates_nexus.utils.images import (
    encode_image_base64,
    detect_media_type,
    validate_image_format,
    load_image_from_url
)

# Encode local image to base64
base64_data = encode_image_base64("image.jpg")

# Detect image type
media_type = detect_media_type("image.png")  # Returns "image/png"

# Validate format
is_valid = validate_image_format("image.jpg")  # Returns True

# Download image from URL
image_bytes = load_image_from_url("https://example.com/image.jpg")
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)
- TIFF (.tiff)

## Provider-Specific Details

### Anthropic Claude

- Model: `claude-3-5-sonnet`, `claude-3-opus`
- Supports images via base64, URLs, or file paths
- Automatic format detection

### OpenAI GPT-4 Vision

- Model: `gpt-4-vision`, `gpt-4-turbo`
- Supports image URLs and base64
- Detail levels: "low" (fast), "high" (detailed)

### Google Gemini

- Model: `gemini-1.5-pro-vision`
- Supports multiple image formats
- Efficient multimodal processing

## Error Handling

```python
from socrates_nexus.exceptions import (
    InvalidRequestError,
    RateLimitError,
    ProviderError
)

try:
    response = client.chat(
        "Analyze this image",
        images=["invalid-image.jpg"]
    )
except FileNotFoundError:
    print("Image file not found")
except InvalidRequestError as e:
    print(f"Invalid image format: {e}")
except RateLimitError:
    print("Rate limited by provider")
except ProviderError as e:
    print(f"Provider error: {e}")
```

## Performance Tips

1. **Resize Large Images** - Reduce file size before sending
2. **Use Detail Level** - Use "low" detail for faster responses
3. **Batch Processing** - Process multiple images in separate calls to avoid timeouts
4. **Cache Results** - Enable caching for repeated image analysis

```python
client = LLMClient(
    provider="anthropic",
    model="claude-3-5-sonnet",
    cache_responses=True,
    cache_ttl=3600  # Cache for 1 hour
)
```

## Examples

See the full working examples in `examples/12_vision_models.py`

## API Reference

### ImageContent Model

```python
from socrates_nexus.models import ImageContent

image = ImageContent(
    source: Union[str, bytes]  # URL, file path, or base64
    media_type: Optional[str]  # "image/jpeg", "image/png", etc.
    detail: Optional[str]       # "low" or "high" (provider-dependent)
)
```

### Vision Parameters

```python
response = client.chat(
    message="Your prompt here",
    images=["url1", "url2"],  # List of image sources
    image_detail="high"        # Optional: vision detail level
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Image not found | Verify file path exists and is readable |
| Format not supported | Convert to JPEG, PNG, GIF, or WebP |
| Rate limited | Add delays between requests |
| Blurry/unclear response | Use higher detail level or better quality image |
| Base64 encoding error | Ensure file is read in binary mode |

## Support

For issues or questions, contact: Hermes_creative@proton.me
