# Blog
#### created, 127/05/2020
#### By [E Naika](https://github.com/ENAIKA)
## Description
* This is a web based app that help users read blog content from writers. Users are able to react on the various blog posts by commenting and writers are able t login and create the blogs.
## Setup/Installation Requirements
* To run the website need a browser (for IE browsers version 9 and above is recommended.)

#### To Contribute
* Before starting the steps below: make sure Python3.6 is installed or have compartible version, have Flask framework and download all the necessary extensions from [requirements.txt] (https://github.com/ENAIKA/Blog/blob/master/requirements.txt) file.
Follow this steps:
* Fork the repo
* Create your branch 
* Make the appropriate changes in the files
* Add changes to reflect the changes made 
* Commit your changes 
* Push to the branch 
* Create a Pull Request.

# Behaviour Driven Design
* The app should display random quotes at the landing page
* The app should should allow users to read blogs written by writers.
* The app should allow writers to create blog posts.
* THe app should allow users to comment on blogs posted by writers.

### Specifications
| Behaviour                | Input example           | Output Example                   |
| ---------------------------|:-----------------------:| --------------------------------:|
| click     | click home icon/Refresh the homepage| True/A random quote displayed|
|submit     | submit blogForm| True/the form is submitted and db updated|
| click               |click subscribe button| True/redirected to subscription page to fill the form|
| click              |click comment| True/redirected to commentForm template to comment|
| click              |click blogs | True/all blogs rendered starting from the most recent blog|
| OA             |sign in and out | True/redirected to appropriate templates|

* create user interface.
* create heroku app and deploy

## Technologies Used
* Python-programming language
* VS Code-IDE
* Flask-Python framework


### License
* MIT License

* Copyright © [E NAIKA](https://github.com/ENAIKA)[2020]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.