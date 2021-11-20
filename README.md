# RegExum

RegExum is Python wrapper that simplifies text search for Terabyte and Petabyte-scale textual datasets stored in one of the following DBMS:

* [MongoDB](#mongodb) - modern (yet mature) distributed document DB with good performance in most workloads
* [ElasticSearch](#elasticsearch) - the go-to DBMS-complementary indexing software for texts and categorical data,
* [PostgreSQL](#postgresql) - most feature-rich open-source relational DB,
* [MySQL](#mysql) - the most commonly-used relational DB.

## Project Structure

* [regexum](regexum) - Python wrappers for search-able containers backed by persistent DBs.
* [benchmarks](benchmarks) - benchmarking tools and performance results.
* [assets](assets) - tiny datasets for testing purposes.

## Implementation Details & Included DBs

Some common databases have licences that prohibit sharing of benchmark results, so they were excluded from comparisons.

|     Name      |       Purpose       | Implementation Language | Lines of Code (in `/src/`) |
| :-----------: | :-----------------: | :---------------------: | :------------------------: |
|    MongoDB    |      Documents      |           C++           |         3'900'000          |
|    Postgre    |       Tables        |            C            |         1'300'000          |
| ElasticSearch |        Text         |          Java           |          730'000           |
|     Unum      | Graphs, Table, Text |           C++           |           80'000           |

### ElasticSearch

* Java-based document store built on top of Lucene text index.
* Widely considered high-performance solutions due to the lack of competition.
* Lucene was ported to multiple languages including projects like: [CLucene](http://clucene.sourceforge.net) and [LucenePlusPlus](https://github.com/luceneplusplus/LucenePlusPlus).
* Very popular open-source project backed by the `$ESTC` [publicly traded company](https://finance.yahoo.com/quote/ESTC).

### MongoDB

* A distributed ACID document store.
* Internally uses the `BSON` binary format.
* Very popular open-source project backed by the `$MDB` [publicly traded company](https://finance.yahoo.com/quote/MDB).
* Provides bindings for most programming languages (including [PyMongo](https://pymongo.readthedocs.io) for Python).

### Postgre, MySQL and other SQLs

* Most common open-source SQL databases.
* Work well in single-node environment, but scale poorly out of the box.
* Mostly store search indexes in a form of a [B-Tree](https://ieftimov.com/post/postgresql-indexes-btree/). They generally provide good read performance, but are slow to update.

## TODO

* [ ] New `re.pattern`-like object for queries and more `list`-like interface for DBs:
  * Finding the first match via `.index(re.pattern)`.
  * Streaming all matches via `.indexes(re.pattern)`.
  * Classical methods `.append(iterable)` and `.extend(iterable)` for index extension.
* [ ] Mixed Multithreaded Read/Write benchmarks.
