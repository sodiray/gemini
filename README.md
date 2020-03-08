# Gemini
A completely generic database migration cli tool ♊️

The benefit is:  
- You can use it in any project
- You can use it with any language (given a gemini language runtime has been developed - [see below](#language-runtime-protocol))
- It will never touch or effect your application (so many migration tools these days think their so self important they force you to hook them directly into your app 🤷)

The downside is:
- You have to write some boilerplate
- You give up some features

[should you use Gemini?](#should-you-use-gemini)

## Getting Started

### 0. Ensure Setup
If your using Gemini on a non-python project there is probably some setup (dependency install, etc.) that Gemini needs to do in order to work with that language. Run `gemini setup [runtime]` and Gemini will take care of it for you. For example, `gemini setup csx` will setup C# by installing `dotnet-scripts` on your machine. Sound scary? You will be prompted for approval with a list of changes that would be made before any work is started.

### 1. Geminiver
The first thing you will need to do is add a `geminiver` file. This is the boiler plate. Because Gemini is generic it can't make assumptions about how to talk to your database. So we will use the `geminiver` file to write those functions. If your using python it will be `geminiver.py` if your using C# it will be `geminiver.csx`. Check out [the examples](/examples) to see how its done. You will need to add the logic that goes to the database and retrieves the latest version and the code that goes to the database and sets the version. Gemini will then use those functions to keep your database up to date.

### 2. Do a dryrun
So, you wrote some code in your `geminiver`... does it work? Lets see! Gemini ships with a command that will call your get version and set version functions to help you ensure all is running in proper order. Just run `gemini dryrun`.
```
gemini dryrun --runtime csx
```

### 3. Run a migration
Create your first migration script. This command will simply generate a migration script template for you. Since this is the first migration your making - and thereby none currently exist - you need to use `--runtime` to tell Gemini what langauge you want to use for your migration scripts. Most other commands - including subsequent `migrate` commands - will attempt to auto detect the language runtime by looking at what is already in the `/migrations` directory.
```
gemini migrate --message "add user table" --runtime py
```
Again, this only creates a template. You'll need to go in the file and script out the logic to create that table in whatever way fits with your application and organization.

### 4. Run the migration
The `upgrade` command will check the current version of your database and run all child migrations in order that it finds in the migrations directory.
```
gemini upgrade
```

### 5. Made a mistake? Roll it back
Maybe your developing and you want to undo that last migration so you can make some changes to it and run it again? The `rollback` command will run the `down` function of the latest migration.
```
gemini rollback
```


## Notes For Developers
The basic flow of logic/modules in Gemini is...
```
------------------
|      cli       |
--------v---------
|    command     |
--------v---------
|    runtime     |
--------v---------
|   migrations   |
------------------
```

#### CLI
This is - and should always be - a simple module that handles cli invokations, gathers any arguments, options, and flags, and then invokes the desired command.

#### Command
Command modules are where the _business logic_ (if you can call it that) lives. This is where the core logic you would expect in Gemini lives. This module contains the logic that decides if migrations should be run, how many, and when. It detects variances in the current version of the database and the version you might attempt to run. In order to support many languages it does all this through the use of the runtime module.

#### Runtime
The runtime is funky... I'll admit. However, for its arguably _hacky_ architecture the benefit is that you can now allow Gemini to handle any programming language. Every language has its own runtime language module. Each languages runtime module contains the logic and implementation for interacting with scripts and code of that particular language. The _hacky_ part comes in when you factor in that this is not _easy_. There are great tools to help us out for a lot of languages but there is still a lot of string parsing and semi-wild dynamic script execution or command line tools used as a bridge to get the job done.

#### Migrations
It is no longer Gemini's code executing. The runtime is now dynamically loading user provided scripts and executing the code inside them.

### Language Runtime Protocol
A language runtime is a python module that exposes a standard set of functions that have been implemented to interact with migrations scripts of a specific language. The runtime module must conform to the runtime protocol (protocol requirements listed below). For example, the C# language runtime module contains functions implemented specifically to read, parse, template, and execute `.csx` migration scripts. Lets say you have an api written in Scala (or maybe your weird and you just want to manage your database changes with Scala scripts) then you would create a `runtimes/scala/runtime.py` module and implement the required functions to read, parse, template, and execute Scala scripts.

#### Required Functions
- `get_database_version()`
- `set_database_version(version: str)`
- `get_migrations()`
- `run_down(version: str)`
- `run_up(version: str)`
- `create_migration(new_version: str, parent_version: str, name: str)`
- `setup()`

## Should you use Gemini?
Gemini isn't for everyone and all projects. In order to make it generic enough to work in such a variety of projects we've had to let go of some _standard_ database migration tool features. One example is dynamically building a migration script based on changes to your model. Theoretically, we could develop this feature... it would just mean adding to the boilerplate code every user needs to write. Each user would need to write project specific boiler plate so Gemini could interact with that projects models. On the other hand - if you have an older project with no migration management, or maybe just a directory of raw SQL scripts and want to add in a migration manager, or you have a variety of project with a variety of languages and you would like to unify the migration management for CI/CD and developer sake, or you prefer not to use a tool that forces itself into your application code - Gemini might be a good tool for you. So, there are the pros, cons, limitations, and features to using Gemini.
