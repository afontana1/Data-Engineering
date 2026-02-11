# ✈️🧳 AI Travel Agent - Powered by LangGraph: A Practical Use Case 🌍
Welcome to the AI Travel Agent repository! This project demonstrates how to leverage LangGraph for building a smart travel assistant that uses multiple language models (LLMs) to handle tasks such as finding flights, booking hotels, and sending personalized emails. The agent is designed to interact with users, invoke necessary tools, and provide a seamless travel planning experience.

## **Features**

- **Stateful Interactions**: The agent remembers user interactions and continues from where it left off, ensuring a smooth user experience.
- **Human-in-the-Loop**: Users have control over critical actions, like reviewing travel plans before emails are sent.
- **Dynamic LLM Usage**: The agent intelligently switches between different LLMs for various tasks, like tool invocation and email generation.
- **Email Automation**: Automatically generates and sends detailed travel plans to users via email.

## Getting Started
Clone the repository, set up the virtual environment, and install the required packages

1. git clone git@github.com:nirbar1985/ai-travel-agent.git

1. ( In case you have python version 3.11.9 installed in pyenv)
   ```shell script
   pyenv local 3.11.9
   ```

1. Install dependencies
    ```shell script
    poetry install --sync
    ```

1. Enter virtual env by:
    ```shell script
    poetry shell
    ```

## **Store Your API Keys**

1. Create a `.env` file in the root directory of the project.
2. Add your API keys and environment variables to the `.env` file:
    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    SERPAPI_API_KEY=your_serpapi_api_key
    SENDGRID_API_KEY=your_sendgrid_api_key

    # Observability variables
    LANGCHAIN_API_KEY=your_langchain_api_key
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_PROJECT=ai_travel_agent
    ```

Make sure to replace the placeholders (`your_openai_api_key`, `your_serpapi_api_key`, `your_langchain_api_key`, `your_sendgrid_api_key`) with your actual keys.
This version includes the necessary environment variables for OpenAI, SERPAPI, LangChain, and SendGrid and the LANGCHAIN_TRACING_V2 and LANGCHAIN_PROJECT configurations.

### How to Run the Chatbot
To start the chatbot, run the following command:
```
streamlit run app.py
```

### Using the Chatbot
Once launched, simply enter your travel request. For example:
> I want to travel to Amsterdam from Madrid from October 1st to 7th. Find me flights and 4-star hotels.


![photo1](https://github.com/user-attachments/assets/eb12d697-a445-4b13-b084-d2052f91d7bc)

The chatbot will generate results that include logos and links for easy navigation.

> **Note**: The data is fetched via Google Flights and Google Hotels APIs. There’s no affiliation or promotion of any particular brand.


#### Example Outputs

- Flight and hotel options with relevant logos and links for easy reference:

![photo2](https://github.com/user-attachments/assets/741e010c-22cf-4d31-a518-441b076ec58f)

![photo3](https://github.com/user-attachments/assets/a29173c7-852d-41ab-b3fe-94e6cca83c78)


#### Email Integration
The email integration is implemented using the **human-in-the-loop** feature, allowing you to stop the agent execution and return control back to the user, providing flexibility in managing the travel data before sending it via email.

![photo4](https://github.com/user-attachments/assets/53775c87-7881-40c3-9b23-2885ed020e46)

- Travel data formatted in HTML, delivered straight to your inbox:
![photo5](https://github.com/user-attachments/assets/02641ce1-b303-4020-9849-7d77f596a6ba)
![photo6](https://github.com/user-attachments/assets/1c3d8a35-148d-4144-829a-b1db6e3b3dde)

## Learn More
For a detailed explanation of the underlying technology, check out the full article on Medium:
[Building Production-Ready AI Agents with LangGraph: A Real-Life Use Case](https://medium.com/cyberark-engineering/building-production-ready-ai-agents-with-langgraph-a-real-life-use-case-7bda34c7f4e4))

## License
Distributed under the MIT License. See LICENSE.txt for more information.
