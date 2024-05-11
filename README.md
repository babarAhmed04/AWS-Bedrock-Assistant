# Amazon Bedrock Help Bot

This project integrates Amazon Bedrock language models, including specialized models such as Llama2, Llama3, and Titan, 
to provide a conversational AI experience. The application is built using Streamlit, allowing users to interact with the AI directly through a web interface.

## Features

- Integration with Amazon Bedrock AI models.
- Real-time conversational interface using Streamlit.
- Support for multiple models: Llama2, Llama3, and Titan.
- Performance metrics tracking and display (response time, user feedback).
- Extensible design for easy addition of new models.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- AWS Account and AWS CLI configured with access to Amazon Bedrock services
- Streamlit

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/amazon-bedrock-help-bot.git
cd amazon-bedrock-help-bot

Install the necessary Python packages:
pip install -r requirements.txt

To run the application:
streamlit run main.py

Navigate to localhost:8501 in your web browser to interact with the application.

Configuration
The application can be configured via the config.py file, where you can specify data directories and other settings.
Ensure your AWS credentials are correctly configured to access the Amazon Bedrock service.

Contributing
Contributions to this project are welcome! To contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature/YourFeature).
- Make your changes.
- Commit your changes (git commit -am 'Add some feature').
- Push to the branch (git push origin feature/YourFeature).
- Create a new Pull Request.

