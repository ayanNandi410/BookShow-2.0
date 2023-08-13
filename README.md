## Folder Information

### api-backend
 contains a Flask App which on execution, sets up the Api to interact with database and handle authentication and authorization

 ****  Requires a 'files' and 'dbDir' folder for execution. if not present, please add it. ****

### client
 contains a Vue App which acts as the frontend

## Execution

### Local Environment Setup (essential for flask server)

run  ` python -m venv <environment name> ` or \
run  ` python3 -m venv <environment name> `

### Backend: 

#### Must Have a celery server running at port 6379(default)

1. start enviromnent by executing ` <env name>/bin/activate ` in Linux or ` <env name>\Scripts\activate ` in Windows
2. move to api-backend
3. execute following commands:

#### `./localSetup.sh`

Activates virtual environment and starts flask server \
In case of dependency issue, execute ` pip install -r requirements.txt `

#### ` ./localSetupWorker.sh `

Starts celery workers to execute tasks

#### ` ./localSetupBeat.sh `

Starts a routine to check for time-assigned tasks and execute them

#### Setup Mailhog

Follow installation instructions from `https://github.com/mailhog/MailHog/tree/master` \
Execute `<installation path>/go/bin/MailHog` 


### Frontend: (requires npm package manager) 

1. move to client folder
2. run ` npm install `, which installs dependencies from package.json
3. run ` npm run dev `, which starts the Vue app locally