from src.schemas.response_schema import (
    CrewResponse
)

def validate_response(
    response_data,
):

    return CrewResponse(
        **response_data
    )