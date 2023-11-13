# Movie Recommendation System (MRS)

This repository contains all the project files and necessary details about applications required to run the project on your local machine as well as host it as a Django Application on your Server/Domain.

| Title                                    | Description                                                                                                         | Link                                                                                                                       |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Demo :movie_camera:                      | Sample Demo of MRS Hosted on free cloud PaaS                                                                        | [:point_down: Refer](https://github.com/inboxpraveen/movie-recommendation-system#1-demo-movie_camera)                      |
| Requirements :heavy_check_mark:          | Requirements and essential links to get started with the project locally                                            | [:point_down: Refer](https://github.com/inboxpraveen/movie-recommendation-system#2-requirements-heavy_check_mark)          |
| Model Training :small_red_triangle_down: | How the MRS was trained for Demo as well as on Large Movie Dataset from Kaggle                                      | [:point_down: Refer](https://github.com/inboxpraveen/movie-recommendation-system#3-model-training-small_red_triangle_down) |
| Project Versatility :page_with_curl:     | Reference documentation of how to plug in any general recommendation model into this project and host it on servers | [:point_down:Refer](https://github.com/inboxpraveen/movie-recommendation-system#4-project-guide)                           |
| Troubleshooting Issues :muscle:          | Guide to resolve errors faced during reproducibility                                                                | To be Updated                                                                                                              |

Do you like it? :heart: Follow me on [Twitter](https://twitter.com/InboxPraveen), [GitHub](https://github.com/inboxpraveen), & [LinkedIn](https://www.linkedin.com/in/praveen-kumar-inbox/) to say Hi :wave:

<hr>

## 1. Demo :movie_camera:

In this section, we try to understand through video demo to play around the project and what all can be achieved through it.

1. [Movie Recommendation System Hosted Application Demo](https://movie-recommendation-8g56.onrender.com/)

2. Running MRS on local System - To be Updated

3. Sample Screenshots

   1. Home Screen

      <img src="static/images/ss1.png" alt="Home Screen" />

   2. Navigation Screen

      <img src="static/images/ss2.png" alt="Navigation Screen" />

   3. Search with Auto Suggestion

      <img src="static/images/ss3.png" alt="Search Functionality" />

   4. Recommended Movies

      <img src="static/images/ss4.png" alt="Movie Recommended Results" />


____

***Please be slightly patient while I create and upload the demo video. Follow and star this project to get latest notifications and update. :raised_hands:***

<hr>

## 2. Requirements :heavy_check_mark:

To build this project without any errors/issues, the following requirements needs to be satisfied

1. Create a Virtual Environment using python>=3.8 (Tested on 3.9.16)

2. Install the dependencies from the requirements text file from the repository.

<hr>

## 3. Model Training :small_red_triangle_down:

### 3.1 Training & Inference

For complete guide to training your model and inference using the trained model, refer to "[Movie Recommendation System Python Notebook](https://github.com/inboxpraveen/movie-recommendation-system/blob/master/Movie_Recommendation_System_Complete_Guide.ipynb)".

#### 3.2 Django Web Application Integration

I'm writing a blog soon...

Please be slightly patient while I create and upload the demo video. Follow and star this project to get latest notifications and update. :raised_hands:

<hr>

## 4. Project Guide

#### 4.1 Running it OnRender Free Cloud

I'm writing a blog soon...

Please be slightly patient while I create and upload the demo video. Follow and star this project to get latest notifications and update. :raised_hands:

#### 4.2 Running in Local

I am assuming you have completed [section 2](https://github.com/inboxpraveen/movie-recommendation-system#2-requirements-heavy_check_mark) in the above reference for creating your environment. Let's start by activating it.

```shell
/path/to/env/bin/activate
```

Once done, you should go to project root directory and run the following command

```she
python manage.py runserver
```

It will take a moment and then show the following output on the terminal.

<img title="" src="./readme_images/runserver_demo.png" alt="">

You can now open your browser and hit the server IP `http://localhost:8000` provided to run the demo on your local system. 

By default, this project will run on Demo model. If you wish to change model, you can train and download the model of your choice using the python notebook to get better or faster recommendations. Once trained, you can integrate by modifying these 2 lines of code inside `recommender/views.py`

```python
Line 5 : movies_data = pd.read_parquet("static/<dataset_name>.parquet")
Line 73: model = pa.parquet.read_table('static/<model_name>.parquet').to_pandas()
```

Note that you have to place dataset and model into the `static` directory.


This code implements a movie recommendation system based on user input. The system provides a simple web interface built on HTML, CSS, and JavaScript libraries. 

Inputs: The user can search for movies by providing a partial or complete movie name. 

Outputs: The system provides movie recommendations based on user input. 

Dependencies: 

* `static/recommender/` -- contains the following CSS files: `cursor.css`, `page.css`, and `navbar.css`
* `static/logo.png` -- the logo of the application
* `static/production ID_4779866.mp4` -- a background video for the web page
* `@tabler/icons@latest/iconfont/tabler-icons.min.css`
* `normalize/5.0.0/normalize.min.css`
* `jquery-ui.css`
* `font-awesome.min.css`
* `bootstrap.min.css`
* `jquery.min.js`
* `jquery-ui.js`

Usage:

1. Open the HTML file in a web browser.
2. Type the name of a movie in the search bar, and the system will provide the movie recommendation. 

Note: Only the top 2.5K movies based on IMBD are present in this system's database.