from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from app.core.config import settings
from app.db.mysql_db import init_db
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini LLM
GEMINI_API_KEY = settings.GEMINI_API_KEY
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=GEMINI_API_KEY
)

# Initialize OpenAi LLM
# OPENAI_API_KEY = settings.OPENAI_API_KEY
# llm = ChatOpenAI(
#     model="gpt-4o",
#     temperature=0,
#     max_retries=1,
#     api_key=OPENAI_API_KEY
# )

# Initialize the SQL DB
db = init_db()

def query(user_id: str, query: str):
    system_message = f"""
    User ID: {user_id}

    You are an intelligent agent that interfaces with a MySQL logistics database. Your task is to interpret natural language questions and respond by generating accurate, secure, and syntactically correct SQL queries based on the database schema and user context.

    ### General Guidelines:
    1. Start by inspecting the schema using `get_table_info()` to understand relevant tables and columns.
    2. Never use `SELECT *`. Always select only the necessary columns.
    3. Use `LIMIT {{top_k}}` when retrieving multiple rows unless explicitly asked for more.
    4. Always use `WHERE` clauses to filter based on the provided `user_id`, where relevant.
    5. Use appropriate `JOIN`s to navigate relationships between tables.
    6. Never execute DML or DDL statements (e.g., INSERT, UPDATE, DELETE, DROP).
    7. Retry queries on error, and revise logic if necessary.
    8. Always double-check your SQL syntax before execution.

    ### Handling Contextual Queries (User-Type Aware):
    When the query is related to the user's depot, company, or account, apply the following logic based on schema relationships:

    - **If the user is a depot user (`user_type = 'D'`)**:
    - Retrieve `user_company_name` directly from the `user` table.
    - Join `user → depot → company → user` (with `user_type = 'C'`) to get the associated company name.
    - Join `user` with `depot` to get details such as `depot_contact`, `labour_charge`, or depot ID.
    - To list jobsheets, filter `jobsheet` records where `js_depot_id` matches the depot linked to this user.

    - **If the user is a company user (`user_type = 'C'`)**:
    - Access all depots and users under that company.
    - Retrieve financial or job-related records across all linked depots.

    - **If the query is general (e.g., about overall system statistics, job summaries, or entity counts)**:
    - Respond without filtering by user unless security or data scope requires it.

    Only return relevant and safe data to the user. If a query involves sensitive or admin-only access, return an appropriate denial or explain the limitation.

    Use best practices in SQL generation, and prioritize correctness, relevance, and efficiency.
    """.format(
        dialect="SQLite",
        top_k=5,
    )


    # Create toolkit and agent
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    agent_executor = create_react_agent(llm, tools, prompt=system_message)

    # Run the agent on the user query
    for step in agent_executor.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        # Extract last message from each step
        messages = step.get("messages", [])
        if messages:
            final_response = messages[-1].content

    return {
        "ai_response": final_response or "No response generated."
    }
