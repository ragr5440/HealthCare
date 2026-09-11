from src.crew.agents import create_agents


def test_create_three_agents():

    agents = create_agents()

    assert len(agents) == 3

    assert "retrieval_agent" in agents
    assert "lookup_agent" in agents
    assert "response_composer" in agents


def test_retrieval_agent_has_one_tool():

    agents = create_agents()

    retrieval_agent = agents[
        "retrieval_agent"
    ]

    assert len(retrieval_agent.tools) == 1
    assert (
        retrieval_agent.tools[0].name
        == "Clinic Policy Search"
    )


def test_lookup_agent_has_one_tool():

    agents = create_agents()

    lookup_agent = agents[
        "lookup_agent"
    ]

    assert len(lookup_agent.tools) == 1
    assert (
        lookup_agent.tools[0].name
        == "Appointment Record Lookup"
    )


def test_composer_has_no_tools():

    agents = create_agents()

    response_composer = agents[
        "response_composer"
    ]

    assert len(response_composer.tools) == 0