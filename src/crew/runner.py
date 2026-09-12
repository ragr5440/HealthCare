import os

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Crew, Task, Process

from src.crew.agents import create_agents

def run_policy_query(
    query: str,
):

    agents = create_agents()

    retrieval_agent = agents[
        "retrieval_agent"
    ]

    retrieval_task = Task(
        description=(
            f"Answer this clinic policy question: "
            f"'{query}' "
            "You must use the Clinic Policy Search tool. "
            "Do not answer from your own knowledge."
        ),
        expected_output=(
            "A short answer based only on the clinic "
            "policy search result."
        ),
        agent=retrieval_agent,
    )

    crew = Crew(
        agents=[retrieval_agent],
        tasks=[retrieval_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)


def run_lookup_query(
    query: str,
):

    agents = create_agents()

    lookup_agent = agents[
        "lookup_agent"
    ]

    lookup_task = Task(
        description=(
            f"Find the appointment record for this query: "
            f"'{query}' "
            "You must use the Appointment Lookup tool. "
            "Do not answer from your own knowledge."
        ),
        expected_output=(
            "A short answer based only on the "
            "appointment record lookup result."
        ),
        agent=lookup_agent,
    )

    crew = Crew(
        agents=[lookup_agent],
        tasks=[lookup_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)