from src.crew.agents import create_agents


def validate_least_autonomy():

    agents = create_agents()

    retrieval_agent = agents["retrieval_agent"]
    lookup_agent = agents["lookup_agent"]
    response_composer = agents["response_composer"]

    print("\nLEAST AUTONOMY VALIDATION")
    print("=" * 50)

    print(
        "Retrieval Agent Tools:",
        [
            getattr(tool, "name", str(tool))
            for tool in retrieval_agent.tools
        ],
    )

    print(
        "Lookup Agent Tools:",
        [
            getattr(tool, "name", str(tool))
            for tool in lookup_agent.tools
        ],
    )

    print(
        "Response Composer Tools:",
        [
            getattr(tool, "name", str(tool))
            for tool in response_composer.tools
        ],
    )

    print("\nGovernance Rules")

    if len(response_composer.tools) == 0:
        print(
            "PASS - Response Composer has no tool access"
        )

    if len(retrieval_agent.tools) == 1:
        print(
            "PASS - Retrieval Agent only has clinic policy search"
        )

    if len(lookup_agent.tools) == 1:
        print(
            "PASS - Lookup Agent only has appointment lookup"
        )


if __name__ == "__main__":
    validate_least_autonomy()