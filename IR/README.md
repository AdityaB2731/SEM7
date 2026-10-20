# Information Retrieval (IR) assignments

This folder contains five small Python programs demonstrating common
Information Retrieval and web-data-processing techniques. Each assignment is
self-contained and prints its result to the terminal.

## Folder structure

| Assignment | File | Main concept |
|---|---|---|
| 1 | `ASSIGN1/similarity.py` | Vector-space document similarity |
| 2 | `ASSIGN2/pagerank.py` | Link-based PageRank |
| 3 | `ASSIGN3/map_reduce_count.py` | MapReduce character counting |
| 4 | `ASSIGN4/web_crawler.py` | Domain-restricted web crawling |
| 5 | `ASSIGN5/topic_pagerank.py` | Topic-sensitive PageRank |

## Setup on Windows

Run from the `IR` folder:

```powershell
cd "D:\SEM7 MINI PROJECT\LP4\codes\IR"
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The external packages are:

- `requests`: sends HTTP requests for the crawler.
- `beautifulsoup4`: parses HTML and extracts page titles and links.

Assignments 1, 2, 3, and 5 use only Python's standard library.

## Assignment 1: document similarity

### Objective

Measure how similar two text documents are using the vector-space model.

### How the code works

1. Opens `sample1.txt` and `sample2.txt`.
2. Converts punctuation and uppercase letters into a normalized form.
3. Splits the text into words.
4. Counts the frequency of every word in each document.
5. Treats each frequency dictionary as a vector.
6. Computes the dot product of the two vectors.
7. Uses the cosine angle formula:

   `angle = acos(dot(A, B) / (|A| * |B|))`

The angle is measured in radians. A smaller angle means the documents are
more similar; an angle near zero means they have similar word distributions.

### Run

The script uses relative paths, so run it from `ASSIGN1`:

```powershell
Set-Location .\ASSIGN1
..\.venv\Scripts\python.exe .\similarity.py
```

### Output

The program prints the number of lines, words, distinct words, and the
distance between the two documents. The current sample run produced:

```text
The distance between the documents is: 0.582779 radians
```

## Assignment 2: PageRank

### Objective

Rank web pages according to the importance of the pages linking to them.

### How the code works

The graph is represented as a dictionary. For example, `A: ["B", "C"]`
means page A links to pages B and C.

1. Gives every page an equal initial rank.
2. Keeps a damping factor of `0.85`.
3. Distributes each page's rank across its outgoing links.
4. Adds a random-teleportation contribution of `(1 - damping) / number_of_pages`.
5. Distributes dangling-page rank equally to all pages.
6. Repeats the calculation for 100 iterations.

### Run

```powershell
Set-Location ..\ASSIGN2
..\.venv\Scripts\python.exe .\pagerank.py
```

### Output

The program prints the final score for pages A, B, C, and D. A higher score
means that the page is more important in the supplied link graph.

## Assignment 3: MapReduce character count

### Objective

Demonstrate the mapper and reducer stages used in distributed processing.

### How the code works

The input is a small text dataset.

**Mapper:** converts text to lowercase, ignores non-ASCII alphabetic
characters, and emits pairs such as `('e', 1)`.

**Reducer:** groups pairs by character and adds their values. For example:

```text
('e', 1), ('e', 1), ('e', 1) -> e: 3
```

### Run

```powershell
Set-Location ..\ASSIGN3
..\.venv\Scripts\python.exe .\map_reduce_count.py
```

### Output

The program displays the mapper output first and then the final alphabetical
character counts.

## Assignment 4: web crawler

### Objective

Visit pages on a website, extract their titles, and discover links on the same
domain.

### How the code works

1. Accepts a starting URL.
2. Adds it to a queue.
3. Removes one URL from the queue.
4. Skips URLs already visited or outside the starting domain.
5. Downloads the page using `requests`.
6. Parses HTML with BeautifulSoup.
7. Prints the URL and page title.
8. Adds same-domain links to the queue.
9. Stops after five pages or when no URLs remain.

### Run safely

Use a public test site or a site where crawling is explicitly permitted:

```powershell
Set-Location ..\ASSIGN4
"https://example.com" | ..\.venv\Scripts\python.exe .\web_crawler.py
```

The crawler does not submit forms or log in. It makes HTTP requests, so it
should still be used responsibly and at a low page limit.

## Assignment 5: topic-sensitive PageRank

### Objective

Rank pages while giving more importance to a selected topic.

### How the code works

1. Parses the embedded XML dataset.
2. Builds a page-to-page graph from `<link>` elements.
3. Stores each page's topic.
4. Selects pages matching the requested topic.
5. Gives the selected topic pages the personalization probability.
6. Runs the PageRank calculation using that personalized teleport probability.
7. Prints pages in descending score order.

If no page matches the requested topic, the program falls back to ordinary
uniform PageRank.

### Run

```powershell
Set-Location ..\ASSIGN5
"AI" | ..\.venv\Scripts\python.exe .\topic_pagerank.py
```

Use `"Sports"` instead of `"AI"` to rank the Sports topic.

## Verified results

All five programs were executed successfully. The crawler was tested with
`https://example.com` and found one page. All Python source files compiled
without syntax errors.
