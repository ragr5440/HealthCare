import os

# These must be set before importing CrewAI.
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Crew, Process, Task

from src.crew.agents import create_agents


def main():

    agents = create_agents()

    retrieval_agent = agents[
        "retrieval_agent"
    ]

    retrieval_task = Task(
        description=(
            "Answer this clinic policy question: "
            "'How do I cancel my appointment?' "
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
        verbose=True,
    )

    result = crew.kickoff()

    print("\nFINAL RESULT")
    print("=" * 60)
    print(result)

if __name__ == "__main__":
    main()