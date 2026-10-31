# AI-Powered Social Media Content Generator using Iterative Workflow

An AI-powered social media content generation application built using **Python, LangChain, LangGraph, OpenAI, and Groq**. The project implements an iterative workflow in which content is generated, evaluated, and optimized using feedback from an LLM-based evaluator until the content is approved or the maximum iteration limit is reached.

## 1. Project Overview

Creating engaging and relevant social media content requires creativity, originality, and proper formatting. This project automates part of that process using Large Language Models (LLMs) and an iterative workflow architecture.

The application accepts a topic from the user and generates social media content based on predefined instructions. The generated content is then evaluated by another LLM based on parameters such as originality, humor, relevance, attractiveness, and character length.

If the generated content does not satisfy the evaluation criteria, the optimizer generates an improved version using the evaluator's feedback. This process continues until the content is approved or the predefined maximum number of iterations is reached.

## 2. Project Objectives

- Automate social media content generation using Large Language Models.
- Implement an iterative workflow using LangGraph.
- Evaluate generated content using structured LLM responses.
- Improve content quality through feedback-driven optimization.
- Integrate multiple LLM providers within a single workflow.
- Understand state management, conditional routing, and iterative execution in Agentic AI.

## 3. Key Features

- **Automated Content Generation:** Generates social media posts based on user-provided topics.
- **LLM-Based Evaluation:** Evaluates content based on originality, humor, relevance, attractiveness, and formatting.
- **Structured Output:** Uses Pydantic to obtain structured evaluation results.
- **Feedback-Driven Optimization:** Improves content based on feedback provided by the evaluator.
- **Iterative Execution:** Repeats the evaluation and optimization process until approval or the iteration limit is reached.
- **Conditional Routing:** Uses LangGraph conditional edges to determine the next workflow step.
- **Multi-LLM Integration:** Integrates OpenAI and Groq models for different workflow operations.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | LLM integration and interaction |
| LangGraph | Workflow orchestration and state management |
| OpenAI GPT-4o-mini | Initial content generation |
| Groq GPT-OSS-20B | Content evaluation |
| OpenAI GPT-4o | Content optimization |
| Pydantic | Structured evaluation output |
| python-dotenv | Secure environment variable management |

## 5. Workflow Architecture

The project consists of three primary nodes:

### 1. Generate Node

- Accepts the topic provided by the user.
- Uses OpenAI GPT-4o-mini to generate social media content.
- Follows predefined instructions regarding content style, humor, simplicity, and character length.
- Passes the generated content to the evaluation node.

### 2. Evaluation Node

- Evaluates the generated content using Groq GPT-OSS-20B.
- Checks originality, humor, attractiveness, relevance, and formatting.
- Uses a Pydantic model to return structured evaluation results.
- Produces one of two evaluation outcomes:
  - `approved`
  - `improvement`

### 3. Optimizer Node

- Receives the evaluator's feedback.
- Uses OpenAI GPT-4o to improve the previously generated content.
- Generates an updated version based on the topic and evaluation feedback.
- Sends the improved content back to the evaluation node.

### Workflow Execution

The workflow follows this execution sequence:

**START → Generate Node → Evaluation Node**

After evaluation:

- If the content is approved, the workflow terminates.
- If improvement is required, the optimizer node generates an improved version and sends it back to the evaluation node.
- The cycle continues until approval or the maximum iteration limit is reached.

## 6. Workflow Diagram

The following diagram illustrates the iterative workflow architecture implemented using LangGraph.

![Iterative Workflow Graph](screenshots/workflow_graph.png)

## 7. Project Execution Output

The following screenshot shows the execution output of the content generation workflow, including the generated content and its evaluation results.

![Project Execution Output](screenshots/output.png)

## 8. Project Structure

```text
AI-Powered-Social-Media-Content-Generator/
│
├── screenshots/
│   ├── workflow_graph.png
│   └── output.png
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

**Note:** The `.env` file contains API credentials and must not be uploaded to GitHub.

## 9. Installation and Setup

Follow these steps to run the project locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Powered-Social-Media-Content-Generator.git
```

### Step 2: Navigate to the Project Directory

```bash
cd AI-Powered-Social-Media-Content-Generator
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure API Keys

Create a `.env` file in the project root directory.

Add your API credentials:

```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder values with your actual API keys.

### Step 6: Run the Application

```bash
python main.py
```

## 10. Environment Configuration

The project uses `python-dotenv` to load API credentials from the `.env` file.

The API keys are accessed using:

```python
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

Ensure that `.env` is included in `.gitignore` to prevent accidental exposure of API credentials.

## 11. Dependencies

The following packages are required:

```text
langchain
langgraph
langchain-openai
langchain-groq
langchain-core
pydantic
python-dotenv
```

Install them using:

```bash
pip install -r requirements.txt
```

## 12. Learning Outcomes

Through this project, I explored and implemented the following concepts:

- Iterative Workflow in Agentic AI.
- LangGraph StateGraph architecture.
- State management using TypedDict.
- Node creation and edge configuration.
- Conditional routing using `add_conditional_edges()`.
- Structured LLM output using Pydantic.
- Integration of multiple LLM providers.
- Feedback-based content optimization.
- Environment variable management for API credentials.

## 13. Future Enhancements

- Support multiple content formats, including LinkedIn posts, Instagram captions, and blog introductions.
- Allow users to select different writing styles and tones.
- Add a user interface for submitting topics and viewing generated content.
- Introduce a more comprehensive content quality scoring mechanism.
- Store generated content and evaluation history.
- Add automated checks for character limits and repeated content.

## 14. Author

**Snehal Vhasure**

Master of Engineering in Information Technology
---

*This project was developed as part of my learning journey in Agentic AI, focusing on iterative workflows, LLM integration, structured evaluation, and feedback-driven optimization.*
