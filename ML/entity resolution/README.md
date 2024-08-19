# Entity Resolution

Problem: Quadratic runtime for naive comparisons. This will not scale. 

Objective: Find a scalable solution for real time entity resolution.

## Local Sensitivity Hashing

- [CS246: Mining Massive Data Sets](https://snap.stanford.edu/class/cs246-2022/)

### EXAMPLES

- https://github.com/Jmkernes/Locality-sensitive-hashing-tutorial
- https://github.com/arpitg91/FindingSimilarDocuments-LSH
- https://github.com/tonymngo/entity-resolution-challenge
- https://github.com/leihao1/MachineLearningAlgorithms
- https://github.com/mattilyra/LSH
- https://github.com/PiotrTa/Mining-Massive-Datasets
- https://github.com/hushon/BigDataEssentials
- https://towardsdatascience.com/locality-sensitive-hashing-how-to-find-similar-items-in-a-large-set-with-precision-d907c52b05fc
- https://towardsdatascience.com/locality-sensitive-hashing-for-music-search-f2f1940ace23
- https://towardsdatascience.com/understanding-locality-sensitive-hashing-49f6d1f6134
- https://nbviewer.org/github/mattilyra/LSH/blob/master/examples/Introduction.ipynb
- https://towardsdatascience.com/is-this-you-entity-matching-in-the-modern-data-stack-with-large-language-models-19a730373b26
- https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/
- https://towardsai.net/p/l/text-similarity-using-k-shingling-minhashing-and-lshlocality-sensitive-hashing
- https://spotintelligence.com/2023/01/16/local-sensitive-hashing/
- https://www.codemotion.com/magazine/backend/fast-document-similarity-in-python-minhashlsh/
- https://tylerneylon.com/a/lsh1/
- https://www.robots.ox.ac.uk/~vedaldi/assets/teach/2022/b16/notes/7-locality-sensitive-hashing.html
- https://randorithms.com/2019/09/19/Visual-LSH.html
- http://ethen8181.github.io/machine-learning/clustering_old/text_similarity/text_similarity.html


## Python Difflib
- https://docs.python.org/3/library/difflib.html

## Blocklib
- https://blocklib.readthedocs.io/en/stable/index.html
- https://arxiv.org/abs/1712.09691
- https://github.com/data61/blocklib

## Useful Resources

1. [SERF](http://infolab.stanford.edu/serf/)
2. [Identity Resolution](https://www.sciencedirect.com/topics/computer-science/identity-resolution)
3. [A framework of identity resolution: evaluating identity attributes and matching algorithms](https://security-informatics.springeropen.com/articles/10.1186/s13388-015-0021-0)
4. [Entity Resolution](https://paperswithcode.com/task/entity-resolution)
5. [Named_entity](https://en.wikipedia.org/wiki/Named_entity)
6. [Entity_linking](https://en.wikipedia.org/wiki/Entity_linking)
7. [Record_linkage](https://en.wikipedia.org/wiki/Record_linkage)
8. [Practical Entity Resolution on AWS to Reconcile Data in the Real World](https://aws.amazon.com/blogs/architecture/practical-entity-resolution-on-aws-to-reconcile-data-in-the-real-world/)
9. [basics-of-entity-resolution](https://www.districtdatalabs.com/basics-of-entity-resolution)
10. [Introduction to Entity Resolution](https://towardsdatascience.com/an-introduction-to-entity-resolution-needs-and-challenges-97fba052dde5)
11. [Local Sensitivity Hashing](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)
12. [Almost All of Entity Resolution](https://www.science.org/doi/10.1126/sciadv.abi8021?cookieSet=1)
13. [Locality Sensitive Hashing: How to Find Similar Items in a Large Set, with Precision](https://towardsdatascience.com/locality-sensitive-hashing-how-to-find-similar-items-in-a-large-set-with-precision-d907c52b05fc)
14. [Text Similarity LSH](http://ethen8181.github.io/machine-learning/clustering_old/text_similarity/text_similarity.html)
15. [Locality Sensitive Hashing (LSH): The Illustrated Guide](https://www.pinecone.io/learn/locality-sensitive-hashing/)
16. [Book](https://www.amazon.com/Data-Matching-Techniques-Data-Centric-Applications/dp/3642430015/ref=pd_lpo_1?pd_rd_w=P5NUt&content-id=amzn1.sym.116f529c-aa4d-4763-b2b6-4d614ec7dc00&pf_rd_p=116f529c-aa4d-4763-b2b6-4d614ec7dc00&pf_rd_r=XXDSTC7KBN0C2V0CA485&pd_rd_wg=gFyTZ&pd_rd_r=38d848b7-e44d-42f8-b00e-0b919d62848b&pd_rd_i=3642430015&psc=1)
17. [Simple MinHash implementation in Python](https://maciejkula.github.io/2015/06/01/simple-minhash-implementation-in-python/)
18. [Finding Duplicate Questions using DataSketch](https://medium.com/@bassimfaizal/finding-duplicate-questions-using-datasketch-2ae1f3d8bc5c)
19. [Minhash and locality-sensitive hashing](https://cran.r-project.org/web/packages/textreuse/vignettes/textreuse-minhash.html)
20. [Near-duplicates and shingling](https://nlp.stanford.edu/IR-book/html/htmledition/near-duplicates-and-shingling-1.html)
21. [Document deduplication using Locality Sensitive Hashing (LSH) with minhash](https://github.com/mattilyra/LSH/blob/master/examples/Introduction.ipynb)
22. [Document deduplication using Locality Sensitive Hashing (LSH) with minhash](https://notebook.community/mbatchkarov/LSH/lsh_minhash)
23. [An overview of end-to-end entity resolution for big data](https://blog.acolyer.org/2020/12/14/entity-resolution/)
24. [https://www.researchgate.net/publication/349363125_A_multiclass_classification_approach_for_incremental_entity_resolution_on_short_textual_data](https://www.researchgate.net/publication/349363125_A_multiclass_classification_approach_for_incremental_entity_resolution_on_short_textual_data)
25. [An Entity Resolution Primer](https://agkn.wordpress.com/2016/05/17/an-entity-resolution-primer/)
26. [Parallel Sorted Neighborhood Blocking with MapReduce](https://www.researchgate.net/publication/47436652_Parallel_Sorted_Neighborhood_Blocking_with_MapReduce)
27. [Cloud-Scale Entity Resolution: Current State and Open Challenges](https://www.semanticscholar.org/paper/Cloud-Scale-Entity-Resolution%3A-Current-State-and-Chen-Schallehn/4775e6973c478df50efad42dd96a5ae5d5bfe339)
28. [Entity Resolution Tutorial](https://linqs.org/assets/resources/getoor-asonam12-slides.pdf)
29. [Near-duplicates and shingling](https://nlp.stanford.edu/IR-book/html/htmledition/near-duplicates-and-shingling-1.html)
30. [(Almost) All of Entity Resolution](https://arxiv.org/abs/2008.04443)
31. [A Survey on Locality Sensitive Hashing Algorithms and their Applications](https://arxiv.org/abs/2102.0894)
32. [SetSimilaritySearch](https://github.com/ekzhu/SetSimilaritySearch)


### Videos
- https://www.youtube.com/watch?v=W7Xqt4guibc
- https://www.youtube.com/watch?v=2Drw9plALIM
- https://www.youtube.com/watch?v=Oky1n3vKuF0
- https://www.youtube.com/playlist?list=PLJphF6F8OTilgxHtjMzp8BXJ6ZKH4DZ8Q
- https://www.youtube.com/playlist?list=PLzERW_Obpmv86IN_pe_byYc3Z18v8MUif
- https://www.youtube.com/playlist?list=PLoOmvuyo5UAfY6jb46jCpMoqb-dbVewxg
- https://www.youtube.com/playlist?list=PLk3qn9pE_2w9WIuE2tWxHR4nwO_qVgT5C
- https://www.youtube.com/watch?v=F-Kf52yvTCU

### Github Examples for [data-matching-software](https://github.com/J535D165/data-matching-software) and [record-linkage-resources](https://github.com/ropeladder/record-linkage-resources)

- [datasketch](https://github.com/ekzhu/datasketch)

1. [dedupe](https://github.com/dedupeio/dedupe)
    - [EntityResolution](https://github.com/TeeanRonson/EntityResolution)
    - [csvdedupe](https://github.com/dedupeio/csvdedupe)
    - [examples](https://github.com/dedupeio/dedupe-examples)
2. [recordlinkage](https://github.com/J535D165/recordlinkage)
3. [splink](https://github.com/moj-analytical-services/splink)
4. [nlu](https://github.com/JohnSnowLabs/nlu)
5. [deduplipy](https://github.com/fritshermans/deduplipy)
6. [fuzzymatcher](https://github.com/RobinL/fuzzymatcher)
7. [nominally](https://github.com/vaneseltine/nominally)
8. [pyJedAI](https://github.com/AI-team-UoA/pyJedAI)
9. [entity-resolution](https://github.com/Orbifold/entity-resolution)
10. [py_entitymatching](https://github.com/anhaidgroup/py_entitymatching)
11. [entity resolution](https://github.com/DistrictDataLabs/entity-resolution)
12. [wrecord linkage toolkit](https://github.com/usc-isi-i2/rltk)
13. [massive-data-mining](https://github.com/Yuhan-Wg/massive-data-mining)
14. [Deduplicating archiver with compression](https://github.com/borgbackup/borg)
    - [borgmatic](https://github.com/borgmatic-collective/borgmatic)
15. [dupeguru](https://github.com/arsenetar/dupeguru)
16. [mail-deduplicate](https://github.com/kdeldycke/mail-deduplicate)
17. [LSH](https://github.com/mattilyra/LSH)
18. [Fly-LSH](https://github.com/dataplayer12/Fly-LSH)
19. [fingerprints](https://github.com/alephdata/fingerprints)
20. [lshashing](https://github.com/MNoorFawi/lshashing)
21. [semantic-sh](https://github.com/KeremZaman/semantic-sh)
22. [LSHash](https://github.com/kayzhu/LSHash)
23. [lshash](https://github.com/loretoparisi/lshash)
24. [dedup](https://github.com/zyocum/dedup)
25. [Panns -- Nearest Neighbors Search](https://github.com/ryanrhymes/panns)
26. [NearPy](https://github.com/pixelogik/NearPy)
27. [rpforest](https://github.com/lyst/rpforest)
28. [narrow-down](https://github.com/chr1st1ank/narrow-down)
29. [Locality-Sensitive-Hashing](https://github.com/RikilG/Locality-Sensitive-Hashing)
30. [LSH-semantic-similarity](https://github.com/avinash-mishra/LSH-semantic-similarity)
31. [locality-sensitive-hashing](https://github.com/KatsarosEf/locality-sensitive-hashing)
32. [MinHash-LSH-From-Scratch](https://github.com/santurini/MinHash-LSH-From-Scratch)
33. [text-shingles](https://github.com/steven-s/text-shingles)
34. [haystack](https://github.com/deepset-ai/haystack)
35. [sourmash](https://github.com/sourmash-bio/sourmash)
36. [Fingerprint and Similarity thresholding](https://github.com/stanford-futuredata/FAST)
37. [BigDataEssentials](https://github.com/hushon/BigDataEssentials)
38. [pyLSHash](https://github.com/guofei9987/pyLSHash)
39. [SparkER](https://github.com/Gaglia88/sparker)
40. [AWS Admartech Samples](https://github.com/aws-samples/aws-admartech-samples)
41. [Awesome-Entity Resolution](https://github.com/Senzing/awesome)
42. [Record Linkage Toolkit](https://github.com/usc-isi-i2/rltk)
43. [Soweego](https://github.com/Wikidata/soweego)
44. [Entity Linking Recent Trends](https://github.com/izuna385/Entity-Linking-Recent-Trends)
45. [Splinks](https://github.com/moj-analytical-services/splink)
46. [DbLink](https://github.com/cleanzr/dblink)
47. [Zingg](https://github.com/zinggAI/zingg)
48. [ditto](https://github.com/megagonlabs/ditto)
49. [redact-pii](https://github.com/solvvy/redact-pii)
50. [SDV](https://github.com/sdv-dev/SDV)
51. [CTGAN](https://github.com/sdv-dev/CTGAN)
52. [Copulas](https://github.com/sdv-dev/Copulas)
53. [DeepEcho](https://github.com/sdv-dev/DeepEcho)
54. [mockingbird](https://github.com/openraven/mockingbird)
55. [awesome-synthetic-data](https://github.com/gretelai/awesome-synthetic-data)
56. [awesome-synthetic-data](https://github.com/gretelai/awesome-synthetic-data)
57. [mimesis](https://github.com/lk-geimfari/mimesis)
58. [ydata-synthetic](https://github.com/ydataai/ydata-synthetic)
59. [thisrepositorydoesnotexist](https://github.com/paulbricman/thisrepositorydoesnotexist)
60. [Octopii](https://github.com/redhuntlabs/Octopii)
61. [faker-file](https://github.com/barseghyanartur/faker-file)
62. [SDGym](https://github.com/sdv-dev/SDGym)
63. [pydbgen](https://github.com/tirthajyoti/pydbgen)
64. [generatedata](https://github.com/benkeen/generatedata)
65. [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator)
66. [presidio](https://github.com/microsoft/presidio)
67. [DataProfiler](https://github.com/capitalone/DataProfiler)
68. [databunker](https://github.com/securitybunker/databunker)
69. [piicatcher](https://github.com/tokern/piicatcher)
70. [PII-Codex](https://github.com/EdyVision/pii-codex)
71. [PII-Leakage](https://github.com/microsoft/analysing_pii_leakage)