
import xml.etree.ElementTree as ET

# Sample XML dataset
xml_data = """
<web>
    <page id="A" topic="AI">
        <link to="B"/>
        <link to="C"/>
    </page>
    <page id="B" topic="AI">
        <link to="C"/>
    </page>
    <page id="C" topic="Sports">
        <link to="A"/>
    </page>
    <page id="D" topic="AI">
        <link to="B"/>
    </page>
</web>
"""

def parse_xml(xml_text):
    root = ET.fromstring(xml_text)
    graph = {}
    topics = {}

    for page in root.findall("page"):
        page_id = page.get("id")
        topics[page_id] = page.get("topic", "")
        graph[page_id] = [
            link.get("to")
            for link in page.findall("link")
            if link.get("to")
        ]

    # Keep only links to pages defined in the XML
    pages = set(graph)
    for page in graph:
        graph[page] = [
            target for target in graph[page]
            if target in pages
        ]

    return graph, topics


def topic_pagerank(graph, topics, topic,
                   damping=0.85, iterations=100):
    pages = list(graph.keys())
    n = len(pages)

    if n == 0:
        return {}

    # Personalized teleport probability
    relevant = [
        page for page in pages
        if topics[page].lower() == topic.lower()
    ]

    if relevant:
        personalization = {
            page: (1 / len(relevant) if page in relevant else 0)
            for page in pages
        }
    else:
        # Fall back to ordinary uniform PageRank
        personalization = {page: 1 / n for page in pages}

    rank = personalization.copy()

    for _ in range(iterations):
        new_rank = {
            page: (1 - damping) * personalization[page]
            for page in pages
        }

        for page in pages:
            links = graph[page]

            if links:
                share = damping * rank[page] / len(links)
                for target in links:
                    new_rank[target] += share
            else:
                # Distribute dangling rank using topic weights
                for target in pages:
                    new_rank[target] += (
                        damping * rank[page]
                        * personalization[target]
                    )

        rank = new_rank

    return rank


graph, topics = parse_xml(xml_data)

print("Generated Web Graph:")
for page, links in graph.items():
    print(page, "->", links)

topic = input("\nEnter topic (AI/Sports): ").strip()
scores = topic_pagerank(graph, topics, topic)

print("\nTopic-Specific PageRank:")
for page, score in sorted(
    scores.items(), key=lambda item: item[1], reverse=True
):
    print(f"Page {page} ({topics[page]}): {score:.4f}")
