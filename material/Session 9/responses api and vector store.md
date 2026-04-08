# OpenAI Responses API & Agents SDK - Complete Guide

## Table of Contents
1. [Responses API Basics](#responses-api-basics)
2. [Sending Messages with Text and Images](#sending-messages-with-text-and-images)
3. [Handling Local Images](#handling-local-images)
4. [OpenAI Agent SDK](#openai-agent-sdk)
5. [Vector Stores & File Search](#vector-stores--file-search)
6. [Chunking Strategies](#chunking-strategies)
7. [Custom Chunking Logic](#custom-chunking-logic)

---

## Responses API Basics

### Overview
The OpenAI Responses API is a cleaner alternative to Chat Completions API with simplified semantics. It separates instructions from input at the top level, making it ideal for straightforward text generation tasks while supporting advanced features like tools, streaming, and structured outputs.

### Basic Usage - Python
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID"),
)

# Simple text generation
response = client.responses.create(
    model="gpt-5",
    instructions="You are a helpful assistant.",
    input="Hello, how are you?"
)
print(response.output_text)
```

### Basic Usage - Requests Library
```python
import requests
import os

# Alternative using requests library
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

data = {
    "model": "gpt-5",
    "instructions": "You are a helpful assistant.",
    "input": "Hello!"
}

response = requests.post(
    "https://api.openai.com/v1/responses",
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
    print(result["output_text"])
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Structured Outputs with JSON Schema
```python
response = client.responses.create(
    model="gpt-5",
    input="Jane, 54 years old",
    text={
        "format": {
            "type": "json_schema",
            "name": "person",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1
                    },
                    "age": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 130
                    }
                },
                "required": ["name", "age"],
                "additionalProperties": False
            }
        }
    }
)

# Response contains structured JSON
import json
data = json.loads(response.text.value)
print(f"Name: {data['name']}, Age: {data['age']}")
```

### Multi-turn Conversations with Streaming
```python
import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID"),
)

# For multi-turn conversations with tools
messages = [
    {"role": "user", "content": [{"type": "input_text", "text": "What's the weather in Paris?"}]}
]

tools_state = {
    "webSearchEnabled": True,
    "fileSearchEnabled": False,
    "functionsEnabled": True,
    "codeInterpreterEnabled": False,
    "vectorStore": None,
    "webSearchConfig": {
        "user_location": {
            "type": "approximate",
            "country": "US"
        }
    }
}

# Stream the response
stream = client.responses.create(
    model="gpt-5",
    messages=messages,
    tools_state=tools_state,
    stream=True
)

for chunk in stream:
    if hasattr(chunk, 'event'):
        if chunk.event == "response.output_text.delta":
            print(chunk.data.get('delta', ''), end='')
        elif chunk.event == "response.completed":
            print("\nResponse completed!")
```

### Tool Integration Example
```python
# Define custom functions
def get_weather(location: str) -> str:
    """Get weather information for a location"""
    return f"Weather in {location}: sunny, 25°C"

def get_joke() -> str:
    """Get a random joke"""
    return "Why don't scientists trust atoms? Because they make up everything!"

# Map functions for tool calls
functions_map = {
    "get_weather": get_weather,
    "get_joke": get_joke
}

# Use with responses API
response = client.responses.create(
    model="gpt-5",
    instructions="You are a helpful assistant with access to weather and humor tools.",
    input="Tell me the weather in London and a joke",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather information for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_joke",
                "description": "Get a random joke"
            }
        }
    ]
)
```

### Key Advantages over Chat Completions API
1. **Cleaner semantics**: Separates instructions from input
2. **Structured outputs**: Better JSON schema support with `text.format`
3. **Tool integration**: Built-in support for web search, file search, code interpreter
4. **Streaming**: Native streaming support for real-time responses
5. **Multi-turn**: Simplified conversation state management

---

## Sending Messages with Text and Images

### Text-Only Messages
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID"),
)

response = client.responses.create(
    model="gpt-5",
    instructions="You are a helpful writing assistant.",
    input="Write a brief summary of climate change."
)
print(response.output_text)
```

### Multi-Modal Messages with Images
```python
# Using image URLs
response = client.responses.create(
    model="gpt-5-vision",
    instructions="You are an image analysis expert.",
    input=[
        {"type": "text", "text": "What do you see in this image?"},
        {
            "type": "image_url",
            "image_url": {
                "url": "https://example.com/path/to/image.jpg"
            }
        }
    ]
)
print(response.output_text)
```

### Multiple Images in One Request
```python
response = client.responses.create(
    model="gpt-5-vision",
    instructions="Compare these images and describe the differences.",
    input=[
        {"type": "text", "text": "Compare these two images:"},
        {
            "type": "image_url",
            "image_url": {"url": "https://example.com/image1.jpg"}
        },
        {
            "type": "image_url",
            "image_url": {"url": "https://example.com/image2.jpg"}
        }
    ]
)
print(response.output_text)
```

---

## Handling Local Images

### Base64 Encoding for Local Images
```python
import base64
import os
from openai import OpenAI

def encode_image(image_path):
    """Encode a local image file to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Load and encode local image
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID"),
)
base64_image = encode_image("./path/to/local/image.jpg")

response = client.responses.create(
    model="gpt-5-vision",
    instructions="You are an expert image analyzer.",
    input=[
        {"type": "text", "text": "Describe this image in detail:"},
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
    ]
)
print(response.output_text)
```

### Handling Different Image Formats
```python
import mimetypes

def encode_image_with_detection(image_path):
    """Encode image and detect MIME type"""
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith('image/'):
        raise ValueError(f"Invalid image file: {image_path}")

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    return f"data:{mime_type};base64,{base64_image}"

# Usage with auto-detection
image_data_url = encode_image_with_detection("./image.png")

response = client.responses.create(
    model="gpt-5-vision",
    instructions="Analyze this image for accessibility compliance.",
    input=[
        {"type": "text", "text": "Check this UI for accessibility issues:"},
        {"type": "image_url", "image_url": {"url": image_data_url}}
    ]
)
```

---

## OpenAI Agent SDK

### Basic Agent Setup with Conversation Management
```python
from openai import OpenAI
from typing import List, Dict
import os

class OpenAIAgent:
    def __init__(self, api_key: str = None, model: str = "gpt-5", instructions: str = ""):
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID"),
        )
        self.model = model
        self.instructions = instructions
        self.conversation_history = []
    
    def send(self, message: str) -> str:
        """Send a message and get response"""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input=message
        )
        
        # Add assistant response to history
        self.conversation_history.append({"role": "assistant", "content": response.output_text})
        
        return response.output_text

# Usage
agent = OpenAIAgent(
    model='gpt-5',
    instructions='You are a helpful customer service agent.'
)

response = agent.send('Hello, I need help with my order')
print(response)
```

### Agent with Persistent Memory
```python
class MemoryAgent(OpenAIAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory = {}  # Simple key-value memory store
    
    def remember(self, key: str, value: str):
        """Store information in memory"""
        self.memory[key] = value
    
    def recall(self, key: str) -> str:
        """Retrieve information from memory"""
        return self.memory.get(key, "No information found")
    
    def send_with_memory(self, message: str) -> str:
        """Send message with memory context"""
        # Include memory context in instructions
        memory_context = "\nMemory: " + str(self.memory) if self.memory else ""
        enhanced_instructions = self.instructions + memory_context
        
        response = self.client.responses.create(
            model=self.model,
            instructions=enhanced_instructions,
            input=message
        )
        
        # Extract and store any new information
        self._extract_memory(message, response.output_text)
        
        return response.output_text
    
    def _extract_memory(self, user_input: str, response: str):
        """Simple memory extraction (can be enhanced with NLP)"""
        if "my name is" in user_input.lower():
            name = user_input.lower().split("my name is")[1].strip().split()[0]
            self.remember("user_name", name)
        if "i like" in user_input.lower():
            preference = user_input.lower().split("i like")[1].strip()
            self.remember("user_preference", preference)

# Usage
memory_agent = MemoryAgent(
    instructions='Remember our conversation history and provide consistent responses.'
)

memory_agent.send_with_memory('My name is John and I like pizza')
response = memory_agent.send_with_memory('What do you know about me?')
print(response)  # Will remember John likes pizza
```

### Agent with Custom Tools
```python
import asyncio
from typing import Callable, Dict, Any

class ToolAgent(OpenAIAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tools = {}
    
    def add_tool(self, name: str, description: str, function: Callable):
        """Add a tool function to the agent"""
        self.tools[name] = {
            'description': description,
            'function': function
        }
    
    def web_search(self, query: str) -> str:
        """Mock web search function"""
        return f"Search results for '{query}': Found 10 relevant articles about {query}"
    
    def file_search(self, query: str, files: List[str] = None) -> str:
        """Mock file search function"""
        files = files or ["doc1.txt", "doc2.pdf"]
        return f"File search results for '{query}' in {len(files)} files: Found relevant content"
    
    def send_with_tools(self, message: str) -> str:
        """Send message with tool capabilities"""
        # Check if message requires tool usage
        tool_result = None
        
        if "search for" in message.lower() or "search the web" in message.lower():
            query = message.lower().replace("search for", "").replace("search the web for", "").strip()
            tool_result = self.web_search(query)
        elif "search files" in message.lower():
            query = message.lower().replace("search files for", "").strip()
            tool_result = self.file_search(query)
        
        # Include tool result in context if available
        enhanced_input = message
        if tool_result:
            enhanced_input = f"User query: {message}\nTool result: {tool_result}\nPlease provide a response based on this information."
        
        response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions + "\nYou have access to web search and file search tools.",
            input=enhanced_input
        )
        
        return response.output_text

# Usage
tool_agent = ToolAgent(
    instructions='You can search the web and analyze files to help users.'
)

response = tool_agent.send_with_tools('Search for the latest news on AI')
print(response)
---

## Vector Stores & File Search

### Creating a Vector Store
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID"),
)

# Create a vector store
vector_store = client.beta.vector_stores.create(
    name="company_knowledge_base"
)
print(f"Vector store created: {vector_store.id}")
```

### Adding Files to Vector Store
```python
# Upload files to vector store
file_paths = ["./docs/policy.pdf", "./docs/manual.txt"]

for file_path in file_paths:
    # Upload file
    with open(file_path, "rb") as file:
        uploaded_file = client.files.create(
            file=file,
            purpose="assistants"
        )

    # Add to vector store
    client.beta.vector_stores.files.create(
        vector_store_id=vector_store.id,
        file_id=uploaded_file.id
    )
    print(f"Added {file_path} to vector store")
```

### Using Vector Store with Responses API
```python
# Use vector store for file search
response = client.responses.create(
    model="gpt-5",
    instructions="Use the knowledge base to answer questions accurately.",
    input="What is our company's vacation policy?",
    tools_state={
        "fileSearchEnabled": True,
        "vectorStore": {
            "id": vector_store.id,
            "name": "company_knowledge_base"
        }
    }
)
print(response.output_text)
```

### Querying Vector Store Directly
```python
# Search within vector store
search_results = client.beta.vector_stores.files.list(
    vector_store_id=vector_store.id,
    query="vacation policy"
)

for result in search_results.data:
    print(f"Relevant file: {result.filename}")
    print(f"Relevance score: {result.score}")
```

---

## Chunking Strategies

### Default Chunking
```python
# OpenAI automatically chunks files when uploaded
# Default strategy: ~800 tokens per chunk with 400 token overlap

file_response = client.files.create(
    file=open("large_document.pdf", "rb"),
    purpose="assistants"
)
# File is automatically chunked for optimal retrieval
```

### Custom Chunking Configuration
```python
# Configure chunking parameters
vector_store = client.beta.vector_stores.create(
    name="custom_chunked_store",
    chunking_strategy={
        "type": "static",
        "static": {
            "max_chunk_size_tokens": 600,
            "chunk_overlap_tokens": 200
        }
    }
)
```

### Manual Text Chunking
```python
def chunk_text(text, chunk_size=800, overlap=200):
    """Manually chunk text with specified size and overlap"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Find natural breakpoint (sentence end)
        if end < len(text):
            last_period = chunk.rfind('.')
            if last_period > chunk_size * 0.7:  # At least 70% of chunk size
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks

# Example usage
long_text = "Your long document text here..."
chunks = chunk_text(long_text)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk[:100]}...")
```

---

## Custom Chunking Logic

### Semantic Chunking
```python
import re
from typing import List

class SemanticChunker:
    def __init__(self, max_chunk_size: int = 800):
        self.max_chunk_size = max_chunk_size

    def chunk_by_sections(self, text: str) -> List[str]:
        """Chunk text by natural sections (headers, paragraphs)"""
        # Split by headers (markdown style)
        sections = re.split(r'\n#{1,3}\s+', text)

        chunks = []
        current_chunk = ""

        for section in sections:
            # If section fits in current chunk
            if len(current_chunk + section) <= self.max_chunk_size:
                current_chunk += section
            else:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())

                # If section is too large, split by paragraphs
                if len(section) > self.max_chunk_size:
                    para_chunks = self._chunk_by_paragraphs(section)
                    chunks.extend(para_chunks)
                    current_chunk = ""
                else:
                    current_chunk = section

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _chunk_by_paragraphs(self, text: str) -> List[str]:
        """Split large sections by paragraphs"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk + para) <= self.max_chunk_size:
                current_chunk += para + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + '\n\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

# Usage
chunker = SemanticChunker(max_chunk_size=600)
semantic_chunks = chunker.chunk_by_sections(document_text)
```

### Code-Aware Chunking
```python
def chunk_code_file(file_content: str, language: str = "python") -> List[str]:
    """Chunk code files by functions/classes while preserving context"""

    if language == "python":
        # Split by function/class definitions
        pattern = r'\n(?=(?:def |class |@\w+\s*\n(?:def |class )))'
        sections = re.split(pattern, file_content)
    else:
        # Generic chunking for other languages
        return chunk_text(file_content)
    
    chunks = []
    imports_and_globals = ""
    
    # Extract imports and global declarations (Python-focused)
    first_section = sections[0] if sections else ""
    import_lines = []
    for line in first_section.split('\n'):
        if (line.strip().startswith(('import ', 'from ')) 
            and 'def ' not in line and 'class ' not in line):
    for section in sections[1:]:  # Skip first section (imports)
        # Include imports with each chunk for context
        chunk_with_context = imports_and_globals + '\n\n' + section
        chunks.append(chunk_with_context.strip())

    return chunks

# Usage for Python files
with open("example.py", "r") as f:
    code_content = f.read()

code_chunks = chunk_code_file(code_content, "python")
for i, chunk in enumerate(code_chunks):
    print(f"Code Chunk {i+1}:\n{chunk}\n---")
```
