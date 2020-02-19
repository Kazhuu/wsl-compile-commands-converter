# wsl-compile-commands-converter

## TLDR

Use `convert.py` Python script to convert `compile_commands.json` with Windows
paths to use Windows Subsystem for Linux (WSL) compatible paths. This enables
tools on WSL side to provide autofill and compiling error messages using Windows
side executables. Personally using this when running Vim on WSL and editing
source code which resides on Windows side.

## What Is This For

When you've C/C++ project which is built by CMake. It can output a
`compile_commands.json` file which contains all information needed to compile
individual files for the project. This output file can then be read by external
tool to know how to compile individual files for the project. This can for
example be used by you editor to autofill functions and inform you about
compiling errors.

Sometimes I'm working on the project which is develop on Windows with Windows
platform tools like Visual Studio, MinGW etc. I love to use Vim for all my
editing (not Visual Studio) and on Windows I'm using WSL (Windows Subsystem for
Linux) to run Vim. On WSL side you can access files on Windows side so editing
source files is possible with Vim.  For example path `C:/` can be mounted on WSL
side to `/mnt/c/`. When project is too tightly coupled with Windows platform and
cannot be compiled from WSL side even using different CMake generators. In this
case Vim on WSL side have no idea of the project structure or how to compile any
files, thus no autofill or error messages.

To overcome above, CMake on Windows side can generate `compile_commands.json`
file which will contains paths in Windows format. WSL side contains tool called
`wslpath`, which can be used to convert Windows path to WSL path. This allows
tools on WSL to execute *.exe files residing on Windows side which CMake
originally used as well. Thus allowing Vim for example to provide compile error
messages, autofill functions names etc.

This repository contains `convert.py` Python script which can be feed with
`compile_commands.json` file containing Windows paths. Script convert paths
using `wslpath` tool and output `compile_commands.json` file with corrected
paths.

## How To Use

Make CMake output `compile_commands.json` file by providing flag
`-DCMAKE_EXPORT_COMPILE_COMMANDS=1` on command line or edit CMakeLists.txt to
contain line `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`. After that CMake will
output file in somewhere in it's subdirectories in the build folder.

After this symlink this project's `convert.py` file to your project root where you
want to use it or hard code the path to it when calling Python. It's important
to know that script will write compile_commands.json to current directory where
script is executed. So make sure you execute it on your project root directory. Invoke
conversion with following:
```
python convert.py path-to-build-folder/compile_commands.json
```
This will output `compile_commands.json` file with WSL paths to current
directory.

Now use your tool of choice to read newly created `compile_commands.json` file.
For example my choice was to use Vim's plugin YouCompleteMe autocompletion engine which
will automatically read `compile_commands.json` file from your project root.
When codebase changes you need to execute Python script again. In this case you
can provide Vim keybinding to do so without leaving your editor.

## Improvements

For Vim's plugin YouCompleteMe provide `.ycm_extra_conf.py` script which will do
conversion automatically on the fly. Read more about it
[here](https://github.com/ycm-core/YouCompleteMe#option-2-provide-the-flags-manually).

There is attempt of this in this repo called `ycm_extra_conf.py` but it doesn't
fully work at the moment. It's able to parse flags and return them with
corrected paths but for some files it raises exceptions.
