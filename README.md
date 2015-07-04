# DistroSeed-Dashboard
DistroSeed is an automated assistant for finding, downloading, and managing Linux Distributions.
## Major Features Include: ##

* Highly limited supported on specific distros for now.
* * Highly limited supported on specific distros for now.
* * Highly limited supported on specific distros for now.


## Configuring Development Environment: ##

### Requirements ###
- Visual Studio 2013 [Free Community Edition](https://www.visualstudio.com/en-us/products/visual-studio-community-vs.aspx)
- [Git](http://git-scm.com/downloads)
- [NodeJS](http://nodejs.org/download/)
- [Gulp](http://gulpjs.com)

### Setup ###

- Make sure all the required software mentioned above are installed.
- Clone the repository into your development machine. [*info*](https://help.github.com/articles/working-with-repositories)
- Grab the submodules `git submodule init && git submodule update`
- install the required Node Packages `npm install`
- install gulp `npm install gulp -g`
- start gulp to monitor your dev environment for any changes that need post processing using `gulp watch` command.

*Please note gulp must be running at all times while you are working with NzbDrone client source files.*


### Development ###
- Open `NzbDrone.sln` in Visual Studio
- Make sure `NzbDrone.Console` is set as the startup project


### License ###
* [GNU GPL v3](http://www.gnu.org/licenses/gpl.html)
Copyright 2010-2015
