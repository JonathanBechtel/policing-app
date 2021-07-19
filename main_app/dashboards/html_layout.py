# -*- coding: utf-8 -*-
"""
Page that contains HTML layout for dashboard
"""

html_layout = """

    <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-wEmeIV1mKuiNpC+IOBjI7aAzPcEZeedi5yW5f2yOq55WWLwNGmvvx4Um1vskeMj0" crossorigin="anonymous">
                <style>
                    .other {
                      vertical-align: center;
                      justify-content: center;
                      align-items: center;
                      display: flex;
                    }

                    .highlight {
                      background-color: #1d6b87;
                      font-size: 2em;
                      padding-left: 3em;
                      padding-right: 3em;
                    }

                    .highlight p {
                      color: #fcfcfc;
                    }
                </style>

                <!-- Global site tag (gtag.js) - Google Analytics -->
                <script async src="https://www.googletagmanager.com/gtag/js?id=G-WDWR3ZTMGT"></script>
                <script>
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());

                  gtag('config', 'G-WDWR3ZTMGT');
                </script>

            </head>
            <body>
              <nav class="navbar navbar-expand-lg navbar-light bg-light">
                      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                          <span class="navbar-toggler-icon"></span>
                      </button>
                <div class="container-fluid">
                  <div class="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul class="navbar-nav">
                      <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/home"">Home</a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="/about">About</a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="/faq">FAQ</a>
                      </li>
                      <li class="api">
                        <a class="nav-link" href="/api">API</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </nav>
                <div class='container'>
                    <div class="row other">
                          <div class="col-4">
                             <h2>Use Data to Understand Police Outcomes</h2>
                             <p>This website uses a machine learning model trained on 4.5 million police stops in North Carolina to better understand what factors impact police outcomes.  The rest
                                of this website is designed to allow you to explore and understand the results.</p>
                                <a href="#main" class="btn btn-success btn-lg" role="button">Start Exploring</a>
                         </div>
                         <div class="col-8">
                             <img src="https://policing-data.s3.amazonaws.com/cover.jpg" class="img-fluid" style="max-height: 700px;">
                         </div>
                    </div>
                </div>
                <div class="row highlight">
                    <p class='text-center'>Fill out the form on the left part of the screen below to see how our statistical model predicts and interprets the causes of a policing outcome.</p>
                </div>
                <div class="container-fluid" id="main">
                    {%app_entry%}
                    <footer>
                        {%config%}
                        {%scripts%}

                        {%renderer%}
                        <ul class="list-inline text-center">
                          <li class="list-inline-item">Developed by <a href="http://jonathanbech.tel">Jonathan Bechtel</a></li>
                          <li class="list-inline-item"><a href = "mailto: questions@policexray.com">questions@policexray.com</a></li>
                          <li class="list-inline-item"><a href="https://github.com/JonathanBechtel/policexray">Github Repo</a></li>
                        </ul>
                    </footer>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-p34f1UUtsS3wqzfto5wAAmdvj+osOnFyQFpp4Ua3gs/ZVWx6oOypYoCJhGGScy+8" crossorigin="anonymous"></script>
                </div>
            </body>
        </html>

"""
