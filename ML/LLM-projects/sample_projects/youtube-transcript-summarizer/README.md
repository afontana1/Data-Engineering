## Project Overview
YouTube Transcript Summarizer is a tool designed to efficiently summarize the transcripts of YouTube videos. It utilizes advanced natural language processing techniques to generate concise summaries of video content, making it easier for users to grasp the key points without having to watch the entire video.

## Problem and Solution Statement
With the constant influx of video content on platforms like YouTube, it's becoming increasingly challenging to sift through lengthy videos for pertinent information. Spending valuable time on videos that might not yield relevant content can be frustrating. Summarizing video transcripts offers a solution by condensing the information into key points, making it easier to identify important patterns without having to watch the entire video. This not only saves time but also streamlines the process of extracting valuable insights from vast amounts of video content.

## Implementation Strategy
The proposed solution entails developing a Chrome extension with a feature that allows users to copy the URL of a selected video. Upon pasting the URL, the extension will utilize the YouTube transcript API to access the transcript of the audio. Subsequently, this transcript will undergo summarization via a machine learning model, yielding a condensed version of the content. Finally, users will have the option to download the summarized text for their convenience.


## Features

- Multiple Langauage Support (Hindi,English,Gujarati,Braille)
- Runtime Text to Speech Conversion (English language Only)
- Get Transcripts of videos of any length.
- Get Summarization of video of any language.
- Downloadable Transcripts.

## Contribution
We welcome pull requests for any improvements you'd like to contribute. If you're planning significant changes, we recommend opening an issue first to discuss your ideas. Additionally, please ensure that any updates include appropriate test coverage.


## Installation

1. Clone the repository in your local machine.
```
git clone https://github.com/ivipinyadav14/youtube-transcript-summarizer.git
```

2. To run the API, you need to set up a **Virtual Environment**. Go into *youtube-transcript-summarizer-api* folder, open command prompt and paste the following command.
```
python -m venv venv
```

3. Now that you got a Virtual Environment created, it's time to install all the **dependencies**. Use the following command.   
```
pip install -r requirements.txt
```
4. Now it's time to run the **API**.
```
python app.py
```
5. Now the API is set up to provide the response. Its time to start with **frontend**.
```
cd ..
cd youtube-transcript-summarizer-frontend
```
6. Install all the required **node modules**.
```
npm install
```
7. You are all set to run the frontend.
```
npm start
```

