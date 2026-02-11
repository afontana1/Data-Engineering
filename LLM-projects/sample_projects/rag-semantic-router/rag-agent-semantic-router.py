import os
from typing import Dict, Any
from datetime import datetime, timedelta
import pytz
import requests

from openai import OpenAI

import chromadb
from chromadb.utils import embedding_functions

from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder
from semantic_router.llms.openai import get_schemas_openai
from semantic_router.llms import OpenAILLM

# Constants
AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi"
export AEROAPI_KEY="your_flightaware_api_key"
COLLECTION_NAME = "baggage_policy"

# Initialize clients
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-3-small"
)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_flight_context(flight_id: str) -> str:
    def _get_flight_data() -> Dict[str, Any]:
        session = requests.Session()
        session.headers.update({"x-apikey": AEROAPI_KEY})
        start_date = datetime.now().date().strftime('%Y-%m-%d')
        end_date = (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        api_resource = f"/flights/{flight_id}?start={start_date}&end={end_date}"
        response = session.get(f"{AEROAPI_BASE_URL}{api_resource}")
        response.raise_for_status()
        flights = response.json().get('flights', [])
        if not flights:
            raise ValueError(f"No flight data found for flight ID {flight_id}.")
        return flights[0]

    def _utc_to_local(utc_date_str: str, local_timezone_str: str) -> str:
        utc_datetime = datetime.strptime(utc_date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        local_timezone = pytz.timezone(local_timezone_str)
        local_datetime = utc_datetime.astimezone(local_timezone)
        return local_datetime.strftime('%Y-%m-%d %H:%M:%S')

    flight_data = _get_flight_data()
    dep_key = 'estimated_out' if flight_data.get('estimated_out') else 'scheduled_out'
    arr_key = 'estimated_in' if flight_data.get('estimated_in') else 'scheduled_in'

    flight_details = {
        'source': flight_data['origin']['city'],
        'destination': flight_data['destination']['city'],
        'depart_time': _utc_to_local(flight_data[dep_key], flight_data['origin']['timezone']),
        'arrival_time': _utc_to_local(flight_data[arr_key], flight_data['destination']['timezone']),
        'status': flight_data['status']
    }
    
    return (
        f"The current status of flight {flight_id} from {flight_details['source']} to {flight_details['destination']} "
        f"is {flight_details['status']} with departure time at {flight_details['depart_time']} and arrival time at "
        f"{flight_details['arrival_time']}."
    )

def get_baggage_context(query: str) -> str:
    collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_function)
    results = collection.query(query_texts=[query], n_results=3)
    if results and results['documents']:
        return " ".join(results['documents'][0])
    return "No relevant baggage information found."

def get_llm_response(query: str, context: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful airline assistant. Answer the user query based on the context provided."},
            {"role": "user", "content": f"Query: {query}\nContext: {context}"},
        ],
    )
    return response.choices[0].message.content

def index_baggage_policy():
    baggage_rules = [
        "Emirates Airlines offers a generous baggage policy that varies based on route, fare type, and cabin class.",
        "For carry-on luggage, Economy passengers are allowed one piece weighing up to 7 kg with dimensions not exceeding 55 x 38 x 20 cm.",
        # ... (rest of the rules)
    ]

    if COLLECTION_NAME not in [col.name for col in chroma_client.list_collections()]:
        collection = chroma_client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        for idx, rule in enumerate(baggage_rules):
            collection.add(documents=[rule], ids=[f"baggage_rule_{idx}"])
        print(f"Stored {len(baggage_rules)} baggage rules in ChromaDB.")
    else:
        collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_function)

    return collection

def setup_router():
    encoder = OpenAIEncoder()
    schemas = get_schemas_openai([get_flight_context, get_baggage_context])

    flight_info = Route(
        name="flight_info", 
        utterances=["What's the status of my flight?", "When does my flight depart?", "Is my flight on time?", "What's the status of flight EK524?"],
        function_schemas=schemas                    
    )

    baggage_policy = Route(
        name="baggage_policy",
        utterances=["What's the baggage allowance?", "How many bags can I bring?", "What are the luggage restrictions?"],
        function_schemas=schemas    
    )

    chitchat = Route(
        name="chat",
        utterances=["Write a poem about a cat.", "Tell me a joke about a rat.", "Why did the chicken cross the road?", "Give me a fun fact."]
    )

    llm = OpenAILLM()
    return RouteLayer(encoder, routes=[flight_info, baggage_policy, chitchat], llm=llm)

def process_query(query: str, router_layer: RouteLayer):
    response = router_layer(query)
    context = "No relevant context found."
    if response.function_call:
        for call in response.function_call:
            if call["function_name"] == "get_flight_context":
                context = get_flight_context(**call["arguments"])
            elif call["function_name"] == "get_baggage_context":
                context = get_baggage_context(**call["arguments"])
    
    llm_response = get_llm_response(query, context)
    print(f"Query: {query}")
    print(f'Function call: {response.function_call}')    
    print(f"Context: {context}")
    print(f"LLM Response: {llm_response}\n")

def main():
    index_baggage_policy()
    router_layer = setup_router()

    queries = [
        "What's the status of flight EK524?",
        "What's the size limit for cabin baggage?",
        "Write a poem about a cat."
    ]

    for query in queries:
        print(f"\nProcessing query: {query}")
        process_query(query, router_layer)


if __name__ == "__main__":
    main()