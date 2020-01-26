# Explaining Recommender Systems (Year 4)
## Project Introduction:
Recommendation Systems are the workhorse of most of the current web-based businesses. When buying something from Amazon, listening to music on Spotify, watching movies on Netflix, you're interacting with an intelligent recommendation systems. Developing efficient algorithms to recommend serendipitous items are one of the hot topics in this research field. The problem is that these algorithms are hard to understand, to explain how a recommendation was made.

The goal of this project is to develop a set of explanation techniques in order to better understand the outputs of recommendation systems, perhaps using visualisations. Using these techniques, we can understand the pros/cons of a specific algorithm in comparison to others.

---
---

## Tools:
* SpotLight:

  SpotLight is a tool for data validation.
  <br/>See https://pypi.org/project/spotlight/ & https://github.com/maciejkula/spotlight for more info.
  
---

* LightFM:

  LightFM is a Python implementation of a number of popular recommendation algorithms for both implicit and explicit feedback. It also makes it possible to incorporate both item and user metadata into the traditional matrix factorization algorithms. It represents each user and item as the sum of the latent representations of their features, thus allowing recommendations to generalise to new items (via item features) and to new users (via user features).
<br/>The details of the approach are described in the LightFM paper, available on arXiv.
<br/>See https://github.com/lyst/lightfm for more info.

---

* ImageMagick:

    This tool is used to convert .png files to a video (or GIF) format. Do so with the following command:
  <br/>*ffmpeg -i step%02d.png -filter:v "setpts=20\*PTS" AnimatedGraph.gif*
  <br/>This makes it easier to view the evolution of various visualisations as the model trains.
  <br/>See https://imagemagick.org/index.php.
  
---
---

## Data:

* Using the MovieLens dataset:
<br/>Once you have downloaded the dataset, use **csv_to_txt.py** to convert the dataset to a text file (which is the required input for the **basic_recom_SL.py** algorithm to run properly.

---

* OMBd is required to acquire movie metadata to provide more information on the recommended movies. Metadata includes the movie's poster, year, runtime, actors, director and plot. The data is extracted in **omdb.py**.
<br/>See http://omdbapi.com/ for more info.
<br/>Note: a key may be required to be able to access the metadata (request one for free).
---
---

## Getting Started:
* Dependencies:

  *Python Version must be more recent then **3.6.0**.*
  
  **Run**
  
  *pip3 install spotlight* (default)
  
  *conda install -c maciejkula -c pytorch spotlight* (prototyping recommender systems).
  <br/>Can also be downloaded from GitHub link provided directly. **Requires the following dependencies**
  
  *pip3 install torch==1.3.0+cpu torchvision==0.4.1+cpu -f https://download.pytorch.org/whl/torch_stable.html*
  
  *pip3 install -U scikit-learn scipy matplotlib*
  
  *pip3 install h5py*
  
  *pip3 install requests*
  
  *pip3 install PyQt5*
  
  (*pip3 install lightfm*)

---

