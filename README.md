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

1. [Movie Recommendation System Hosted Application Demo](https://movie-recommender-29hr.onrender.com/)

2. Running MRS on local System - To be Updated

____

***Please be slightly patient while I create and upload the demo video. Follow and star this project to get latest notifications and update. :raised_hands:***

<hr>

## 2. Requirements :heavy_check_mark:

To build this project without any errors/issues, the following requirements needs to be satisfied

1. Windows Operating System (Win 10 is preferred)

2. Google Chrome Browser (v80 or Higher)

3. WAMP Web Server (v3.0 or higher)

4. Code Editor (Visual Studio Code - Preferred)

If you are not aware if you have the right versions or you need to install them, fret not. Continue to the installation section at next.

<hr>

## 3. Model Training :small_red_triangle_down:

### 3.1 Chrome Installation

- To download latest google chrome web browser on Windows OS and install in your system, just go the following link - [Download Google Chrome Web Browser](https://www.google.com/intl/en_in/chrome/). Once you visit, it will have option for you to download chrome and then install it as usual. 

- If you are on Linux OS, then you can follow - [Install Chrome on Linux Mint - Easy Step-By-Step Guide | Digital Ocean](https://www.digitalocean.com/community/tutorials/install-chrome-on-linux-mint).

- If you are on Mac OS, then you can follow - [How To Install Google Chrome On Mac Quickly](https://setapp.com/how-to/install-google-chrome-for-mac-quickly). 

:spiral_notepad:***NOTE: Google chrome is preferred browser to run everything smoothly, but you can use any other browser of your choice as well. It is not a hard requirement, but can help you ease your UI & UX experience.***

### 3.2 Code Editor

- To download Visual Studio Code - Just follow the official website which contains a build for all 3 platforms. Visit - [Download Visual Studio Code - Mac, Linux, Windows](https://code.visualstudio.com/download)
- You can download your OS based build and install it will all the default instructions.
- Visual Studio Code is preferred editor but there are other good options as well. You can choose to work with whatever you are comfortable or use to.

### 3.3 WAMP Web Server

Installing WAMP Web Server and running a local server on your machine is crucial for replicating and reproducing all the results for this project. 

1. Downloading WAMP Server - Go and grab the WAMP installer application from [here](https://sourceforge.net/projects/wampserver/). The size varies based on which version you download. I have v3.3.0 on my system whose download size was 644 MB.

2. Once you have downloaded, Install the with the following settings.

<img title="Wamp Installlation Step 1" src="./readme_attachments/wamp_installation_1.png" alt="Step 1">

<img title="Wamp Installlation Step 2" src="./readme_attachments/wamp_installation_2.png" alt="Step 2">

After this, it will take some time and then install it. After some time, it will ask for a prompt on choosing the default browser on which your local server will be hosted. It initially shows me Edge, but I wish to change it to Google Chrome. 

<img title="Wamp Installlation Step 3" src="./readme_attachments/wamp_installation_3.png" alt="Step 3">

For changing it to Google Chrome, Just select Yes here, and then find where you have installed Google Chrome on your system. In my case, It's at the following directory.

<img title="Wamp Installlation Step 4" src="./readme_attachments/wamp_installation_4.png" alt="Step 4">

Once we have chosen browser, It will ask for Code editor in a similar fashion. 

<img title="" src="./readme_attachments/wamp_installation_5.png" alt="">

By default it will set Notepad Windows Application, but as we prefer and have already setup Visual Studio Code Editor, we will go ahead and select it from the installed directory.

<img title="" src="./readme_attachments/wamp_installation_6.png" alt="">

This will complete the installation of WAMP Server in our system.

To verify WAMP is successfully installed and the Server is running on your system, search for WAMP in your start menu applications and then run it as "administrator"

<img title="" src="./readme_attachments/running_wamp_1.png" alt="">

Once you run it, after few seconds, a green color wamp icon **should** appear on your tray icon.

<img title="" src="./readme_attachments/running_wamp_2.png" alt="">

If the color is anything but green, it looks like there is some issue while running the server.

<hr>

## 4. Project Guide

### 4.1 Building Database & Schema in WAMP

1. Start the WAMP server and wait for it while the server runs successfully. 

2. Open Google Chrome (or any browser) and type "http://localhost/phpmyadmin" without quotes. You will be presented with the login screen.

3. By default, the Username is "root" & and empty password. If this is not the case for you, you will need to change your username & password.

<img title="" src="./readme_attachments/login_wamp.png" alt="">

4. Once we are logged in, we should create our database schema. To do so, select new from left panel, enter name of database as "fifa" and select encoding as "utf8mb4_unicode_ci" and then hit create button.

<img title="" src="./readme_attachments/building_db_1.png" alt="">

---