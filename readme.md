## TerminalUtils

This collection is part of my micro automation journey where I try and write scripts for small things I do daily - like checking weather.

## Installation
These applications are not packaged yet, so you will have to manually copy the files to you system's path. Also, some of the applications use an external API, and you'll have to obtain an API key for yourself (it's free) before you can make requests to the API.

## Available applications
<ol>
<li>

**Weather** - get weather predictions for upto a week from today

Installation: <br/>

* Make a free acount on openweathermap.org and obtain an API key.

* Download the files to your local computer: <br/>
```wget https://raw.githubusercontent.com/Schapagain/terminal-utils/master/weather/main.py``` <br/>
```wget https://raw.githubusercontent.com/Schapagain/terminal-utils/master/weather/weather```

* Create a directory and add both files into the directory: <br/>
```mkdir weather_app && mv weather main.py weather_app```

* Check your system paths: <br/>
```echo $PATH```

* You should now see a colon seperated list of paths. Now let's move our folder created above to one of these paths: <br/>
```mv -r weather_app /usr/local/bin```

* Add the application folder to PATH and add API key to shell environment:<br/>
    * Open the shell configuration file: <br/>
    ```open ~/.bashrc``` or ```open ~/.<shell>rc``` for any shell you're using
    * Add these line to the shell configuration: <br/>
    ```export PATH="$PATH:/usr/local/bin/weather_app"``` <br/>
    ```WEATHER_API_KEY="your_api_key"```

        (This might be a poor choice of adding applications to path, and setting environment variables, but we'll run with it for now. )
    * Save the file and restart your terminal

* Now you should be able to starting using the application! <br/>
    ```weather -h```

</li>
</ol>

