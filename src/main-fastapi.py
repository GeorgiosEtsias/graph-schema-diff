"""

Script launches a fast-api app, that enables the user
to test the changes between 2 versions fo a GraphQL schema.

"""
# import packages
from fastapi import FastAPI, HTTPException, Query
from starlette.responses import JSONResponse
import logging

# import custom method
from schema_diff_report import graphql_diff_report

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the title of the FastAPI application
app = FastAPI(title="graph-schema-difference-Georgios-Etsias")

@app.get("/compare-schemas/")
def compare_schemas_endpoint(
    schema1: str,
    schema2: str,
    summarization_technique: str = Query("algorithmic", enum=["algorithmic", "GPT3.5"])
):
    try:
        # Log the received schemas for debugging
        logger.info("Received schemas for comparison:")
        logger.debug(f"Schema 1: {schema1}")
        logger.debug(f"Schema 2: {schema2}")
        logger.debug(f"Summarization Technique: {summarization_technique}")

        # Pass the summarization technique to the graphql_diff_report
        result = graphql_diff_report(schema1, schema2, summarization_technique)

        # Return the comparison result
        return JSONResponse(content=result)

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error comparing schemas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing schemas: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    logging.info(f"Test the app in: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
