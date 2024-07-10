# Introduction 
TODO: This Django application contains the backend code for the demo web-app. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Setup .env File
3.	Starting Servers

1. **Installation Process:**
   - Ensure you have Python installed, preferably version 3.10 or above.
   - Create a virtual environment for the project:
     ```bash
     python3.10 -m venv ./venv
     ```
   - Activate the virtual environment:
     ```bash
     source ./venv/bin/activate
     ```
   - Upgrade pip:
     ```bash
     pip install --upgrade pip
     ```
   - Install dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
2. **Setup .env File:**
   - Create a `.env` file in the root directory of the project.
   - Use the `env.example` file included in the code as a reference to set up your environment variables.

3. **Starting Servers:**
   - Start the servers by running the `start.sh` file included in the code:
     ```bash
     sh start.sh
