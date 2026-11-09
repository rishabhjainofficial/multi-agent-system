from agents import build_search_agent, build_scraper_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str) -> dict:
    search_agent = build_search_agent()
    scraper_agent = build_scraper_agent()

    state= {}
    print("\n"+" ="*50)
    print("Step 1: search agent is working ...")
    print("="*50)
    search_output = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_output"] = search_output["messages"][-1].content

    print("\n search result", state["search_output"])

    print("\n" + "="*50)
    print("Step 2: scraper agent is working ...")
    print("="*50)
    scraper_output = scraper_agent.invoke({
        "messages": [("user", 
            f"Based on the following search results about: '{topic}', "
            f"pick the most relevant url and scrape it for deeper content.\n\n"
            f"Search results:\n{state['search_output'][:800]}"
        )]
    })
    state["scraper_output"] = scraper_output["messages"][-1].content

    print("\n scraper result", state["scraper_output"])

    print("\n" + "="*50)
    print("Step 3: writer agent is working ...")
    print("="*50)

    research_combined = (
        f"Search results: \n {state["search_output"]}"
        f"Detailed Scraped Content: \n {state['scraper_output']}"
    )
    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("\n Final report", state["report"])

    print("\n" + "="*50)
    print("Step 4: critic agent is working ...")
    print("="*50)
    state["feedback"] = critic_chain.invoke({
        "topic":topic,
        "report":state["report"]
    })

    print("\n Critic Feedback", state["feedback"])

    return state

if __name__ == "__main__":
    topic = input("\n Enter the research topic: ")
    run_research_pipeline(topic)