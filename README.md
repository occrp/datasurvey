# datasurvey

Crawl a directory of files and generate a summary of what is available. Builds on libmagic, and uses
Magic database to identify files. Is therefore similar in function to `file(1)`, except:

 * Configurable output reporters:
   * CSV list of all files
   * List of files with mime types from a 'bad match' list
   * Fancy table output
   * Aggregate reports showing number of each type of file
 * Recursion into archives such as Zip and RAR.

## Installation

You can install Datasurvey on your system by running the following as `root`:

```
$ pip install -r requirements.txt
$ python setup.py install
```

## Running with Docker

Sometimes you want to avoid running Datasurvey on bare metal, which involves installing 
dependencies and what not. Docker is the solution!

You can build a Datasurvey Docker image with:

```
$ docker build -t datasurvey /path/to/datasurvey
```

Then you can run it with:

```
$ docker run -t datasurvey
```

It'll drop you into a bash shell where you can run Datasurvey with:

```
# datasurvey [OPTIONS] PATH
```

The clever way to do this is to mount a volume you wish to use:

```
$ docker run -t datasurvey -v /path/to/data:/data:ro
# datasurvey [OPTIONS] /data
```

## Known bugs

 * Encountering archives inside archives may cause crashes


## Contact

If there are any questions, create a [Github issue](https://github.com/occrp/datasurvey).
