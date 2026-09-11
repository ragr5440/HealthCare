from crewai import Agent

from src.crew.mock_llm import MockLLM
from src.tools.crewai_tools import (
    appointment_record_lookup,
    clinic_policy_search,
)

def create_agents():
    """
    Create the three agents required.
    """
    mock_llm = MockLLM()

    retrieval_agent = Agent(
        role="Clinic Policy Retrieval Agent",
        goal=(
            "Find clinic policy information relevant "
            "to the user's question."
        ),
        backstory=(
            "You search the clinic policy knowledge base. "
            "You use only the Clinic Policy Search tool and "
            "do not invent policy details."
        ),
        llm=mock_llm,
        tools=[clinic_policy_search],
        allow_delegation=False,
        verbose=True,
        max_iter=3,
    )

    lookup_agent = Agent(
        role="Appointment Lookup Agent",
        goal=(
            "Retrieve the correct appointment record "
            "when an appointment ID is provided."
        ),
        backstory=(
            "You look up appointment records by ID. "
            "You use only the Appointment Record Lookup "
            "tool and do not invent appointment details."
        ),
        llm=mock_llm,
        tools=[appointment_record_lookup],
        allow_delegation=False,
        verbose=True,
        max_iter=3,
    )

    response_composer = Agent(
        role="Healthcare Support Response Composer",
        goal=(
            "Create a clear final response using only "
            "information returned by the other agents."
        ),
        backstory=(
            "You write simple and helpful responses for "
            "clinic users. You do not search records and "
            "you do not create unsupported claims."
        ),
        llm=mock_llm,
        tools=[],
        allow_delegation=False,
        verbose=True,
        max_iter=2,
    )

    return {
        "retrieval_agent": retrieval_agent,
        "lookup_agent": lookup_agent,
        "response_composer": response_composer,
    }