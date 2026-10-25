# Extending LazyOwnShell with Lua Plugins

This document explains how to use Lua scripting to extend the functionality of the `LazyOwnShell` application, which is built on top of the `cmd2` framework in Python. Lua allows you to write custom plugins that can add new commands, modify existing behavior, or access application data.

![image](https://github.com/user-attachments/assets/aff3eba8-ea3a-408c-9de5-6f09d6c30a93)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Setting Up Lua Plugins](#setting-up-lua-plugins)
3. [Writing Lua Plugins](#writing-lua-plugins)
4. [Registering New Commands](#registering-new-commands)
5. [Accessing Application Data](#accessing-application-data)
6. [Error Handling](#error-handling)
7. [Example Plugins](#example-plugins)
8. [Best Practices](#best-practices)

---

## 1. Introduction

The `LazyOwnShell` application supports Lua scripting to allow users to extend its functionality without modifying the core Python code. Lua scripts (plugins) are stored in the `plugins/` directory and are automatically loaded when the application starts.

Lua plugins can:
- Add new commands to the shell.
- Modify existing commands or behaviors.
- Access and manipulate application data exposed by Python.

---

## 2. Setting Up Lua Plugins

To use Lua plugins, ensure the following:

1. Install the `lupa` library in your Python environment:
   ```bash
   pip install lupa
   ```
   ```bash
   plugins/
        init_plugins.lua
        hello.lua
        goodbye.lua
   ```
   When the application starts, it will execute init_plugins.lua, which loads all other .lua files in the plugins/ directory.

2. Writing Lua Plugins
   A Lua plugin is a script file with the .lua extension placed in the plugins/ directory. Each plugin can define functions and register them as commands in the shell.

Structure of a Lua Plugin

   ```lua
    -- Define a function for the new command
    function my_command(arg)
        -- Your logic here
        print("This is a new command: " .. (arg or "default"))
    end

    -- Register the function as a command
    register_command("my_command", my_command)
   ```
Key Functions
- register_command(command_name, lua_function):
- Registers a new command in the shell.
- command_name: The name of the command (e.g., hello).
- lua_function: The Lua function to execute when the command is called.

3. Registering New Commands

    To add a new command to the shell, follow these steps:

- Define a Lua function that implements the command logic.
- Use register_command to register the function as a command.
- Example: Adding a hello Command
- Create a file plugins/hello.lua with the following content:

   ```lua
    function hello(arg)
        local name = arg or "world"
        print("Hello, " .. name .. "!")
    end

    register_command("hello", hello)
   ```
Now, you can run the hello command in the shell:
    ```bash
    hello Lua
    Hello, Lua!
    ```
4. Best Practices
- Keep Plugins Modular : Each plugin should focus on a single feature or functionality.
- Document Your Plugins : Provide clear documentation for each plugin, including usage examples.
- Test Thoroughly : Test your plugins in isolation before integrating them into the main application.
- Handle Errors Gracefully : Use pcall to handle errors in Lua plugins and prevent crashes.

By leveraging Lua scripting, you can extend the functionality of LazyOwnShell without modifying the core Python code. This allows for greater flexibility and customization, enabling users to write their own plugins to meet specific needs. Happy coding!
