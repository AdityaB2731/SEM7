
def page_rank(graph, damping=0.85, iterations=100):
    pages = list(graph.keys())
    n = len(pages)

    if n == 0:
        return {}

    rank = {page: 1 / n for page in pages}

    for _ in range(iterations):
        new_rank = {
            page: (1 - damping) / n
            for page in pages
        }

        # Distribute rank through outgoing links
        for page in pages:
            links = graph[page]

            if links:
                share = damping * rank[page] / len(links)
                for linked_page in links:
                    new_rank[linked_page] += share
            else:
                # Distribute dangling-page rank equally
                share = damping * rank[page] / n
                for target in pages:
                    new_rank[target] += share

        rank = new_rank

    return rank


# Web graph: page -> pages it links to
graph = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A"],
    "D": ["C"]
}

ranks = page_rank(graph)

print("PageRank Scores:")
for page, score in sorted(ranks.items()):
    print(f"Page {page}: {score:.4f}")
