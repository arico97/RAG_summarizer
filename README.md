Install requirements: 

``pip install --no-cache-dir -r requirements.txt``

Run backend:

``uvicorn src.app:api_router --reload`` 

or 

``.\run.sh``

Run frontend:

``streamlit run main.py`` 

Build docker frontend image:

Run docker frontend image:

Build docker backend image:

Run docker backend image:

Docker compose:
# RAG Summarizer

## Project Overview

The **RAG Summarizer** is a Retrieval-Augmented Generation (RAG) model designed to generate concise summaries from input documents. By leveraging both retrieval mechanisms and generative capabilities, it produces accurate and contextually relevant summaries.

## Features

- **Document Retrieval**: Fetches relevant information from a predefined dataset to enhance summary generation.
- **Text Summarization**: Generates concise summaries using advanced natural language processing techniques.
- **Streamlit Interface**: Provides an interactive web application for users to input text and receive summaries.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/arico97/RAG_summarizer.git
   cd RAG_summarizer
   ```
2. **Set Up a Virtual Environment (optional but recommended)**:
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```
## Usage
1. Run the Streamlit Application:

   ```bash
   streamlit run streamlit_app.py
   ```
2. Access the Application:

Open your web browser and navigate to http://localhost:8501 to interact with the RAG Summarizer.

## Project Structure
- ``src/``: Contains the core modules for document retrieval and summarization.
- ``streamlit_app.py``: Hosts the Streamlit web application interface.
- ``requirements.txt``: Lists all necessary Python dependencies.
- ``Dockerfile``: Defines the Docker image setup for containerized deployment.
- ``rag-summarizer-deployment.yaml``: Kubernetes deployment configuration for the application.

## Deployment
### Docker
1. Build the Docker Image:

   ```bash
   docker build -t rag-summarizer:latest .
   ```
2. Run the Docker Container:

   ```bash
   docker run -p 8501:8501 rag-summarizer:latest
   ```
### Kubernetes
1. Apply the Deployment Configuration:

   ```bash
   kubectl apply -f rag-summarizer-deployment.yaml
   ```
2. Expose the Service:
Ensure the service is accessible by configuring the appropriate Kubernetes service resources.

## Testing
Execute the test suite to verify the functionality of the summarizer:

   ```bash
python test.py
   ```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your enhancements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Special thanks to the open-source community and the developers of the libraries utilized in this project.

