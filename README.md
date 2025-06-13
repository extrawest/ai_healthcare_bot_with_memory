# 🏥 AI Healthcare Bot with Memory

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Maintainer](https://img.shields.io/static/v1?label=Yevhen%20Ruban&message=Maintainer&color=red)]()
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)]()
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub release](https://img.shields.io/badge/release-v1.0.0-blue)

An intelligent healthcare assistant with memory capabilities using Mem0, built using FastAPI, Chainlit, and mem0. This bot can remember patient information across conversations, providing personalized healthcare support.

## Demo



https://github.com/user-attachments/assets/ee2f519c-fdf6-4143-8fe3-8c03e0977462





## 🌟 Features

- 🧠 **Memory System**: Remembers patient information and conversation history using mem0
- 🔄 **Streaming Responses**: Real-time streaming of AI responses for a better user experience
- 🏥 **Healthcare Focus**: Specialized in healthcare-related conversations and information
- 🌐 **Dual Interface**: API backend with FastAPI and interactive UI with Chainlit
- 🔒 **Secure**: Designed with healthcare data privacy considerations
- 📱 **Responsive UI**: Modern, user-friendly interface for patient interactions

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/extrawest/ai_healthcare_bot_with_memory.git
cd ai_healthcare_bot_with_memory

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit the `.env` file with your own settings:
- Set your OpenAI API key
- Configure Qdrant settings for vector storage
- Adjust host/port settings if needed

### 3. Start the FastAPI Backend

First, start the FastAPI backend server:

```bash
python -m src.main
```

The API will be available at http://0.0.0.0:8000 by default.

### 4. Start the Chainlit UI

In a new terminal window (with the virtual environment activated), start the Chainlit UI:

```bash
python run_chainlit.py
```

The UI will be available at http://0.0.0.0:8001 by default.

### 5. Interact with the Bot

Open your browser and navigate to http://0.0.0.0:8001 to start interacting with the healthcare bot. The bot will remember your conversation history and provide personalized healthcare support.

## 💻 Usage

### API Endpoints

#### Chat Completions
```
POST /chat/completions
```
Request body:
```json
{
  "user_message": "I have a headache and would like to schedule an appointment",
  "user_id": "user_12345"
}
```

Response: A streaming response with AI-generated content.

### Memory System

The bot uses mem0 to store and retrieve relevant information from previous conversations. This allows it to:

- Remember patient symptoms and conditions
- Recall previous appointments and discussions
- Provide personalized healthcare advice based on patient history

## 📋 Requirements

- Python 3.9+
- OpenAI API key
- Qdrant instance (for vector storage)
- FastAPI
- Chainlit
- mem0
- langchain

## 🔧 Technical Implementation

### Memory Configuration

The system uses mem0 for memory storage with the following configuration:
- OpenAI embeddings (text-embedding-3-large)
- Qdrant vector store for efficient retrieval
- Custom prompt for healthcare entity extraction

### Streaming Implementation

The application implements streaming responses using:
- FastAPI's StreamingResponse
- Custom streaming service that converts regular responses to streams
- Chainlit's streaming capabilities for real-time UI updates

### Healthcare Support Agent

The AIHealthcareSupport agent:
- Retrieves relevant memories for each query
- Builds context from previous conversations
- Uses OpenAI's GPT-4o model for generating responses
- Stores new conversation data in memory

Developed by [extrawest](https://extrawest.com/). Software development company
