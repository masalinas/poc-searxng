from langchain_community.utilities import SearxSearchWrapper

# 1. Initialize host (or export SEARX_HOST to your environment variables)
# If using a public instance, verify API access is enabled on that instance.
searx_host='http://localhost:8888'

search = SearxSearchWrapper(searx_host=searx_host)

# 2. Query for academic papers using the 'science' category filter
# We use .results() instead of .run() to get rich metadata (links, snippets, engines)
academic_results = search.results(
    query="Multimodal Human Activity Recognition sensor fusion",
    num_results=5,
    categories=["science"],  # Restricts search to academic/scientific engines
    time_range="year"        # Optional: 'day', 'week', 'month', 'year'
)

# 3. Print the formatted findings
for idx, result in enumerate(academic_results, 1):
    print(f"--- Result {idx} ---")
    print(f"Title: {result.get('title')}")
    print(f"Link:  {result.get('link')}")
    print(f"Engines Used: {result.get('engines')}")
    print(f"Snippet: {result.get('snippet')}\n")
