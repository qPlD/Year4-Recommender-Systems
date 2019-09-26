# Explaining Recommender Systems (Year 4)
## Project Introduction:
Recommendation Systems are the workhorse of most of the current web-based businesses. When buying something from Amazon, listening to music on Spotify, watching movies on Netflix, you're interacting with an intelligent recommendation systems. Developing efficient algorithms to recommend serendipitous items are one of the hot topics in this research field. The problem is that these algorithms are hard to understand, to explain how a recommendation was made.

The goal of this project is to develop a set of explanation techniques in order to better understand the outputs of recommendation systems, perhaps using visualisations. Using these techniques, we can understand the pros/cons of a specific algorithm in comparison to others.

## Tools:
* SpotLight:

  SpotLight is a tool for data validation (see https://pypi.org/project/spotlight/ for more info).
  
  **Run** *pip install spotlight*
  
  Python Version must be more recent then **3.6.0**.
---
* LightFM:

  LightFM is a Python implementation of a number of popular recommendation algorithms for both implicit and explicit feedback. It also makes it possible to incorporate both item and user metadata into the traditional matrix factorization algorithms. It represents each user and item as the sum of the latent representations of their features, thus allowing recommendations to generalise to new items (via item features) and to new users (via user features). The details of the approach are described in the LightFM paper, available on arXiv. (see https://github.com/lyst/lightfm for more info).
  
  **Run** *pip install lightfm*
---




*(All code is my own work unless otherwise stated)*
