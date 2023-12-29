# Telegram Messages Mass Delete Script

This script can mass delete messages upto a given date which is inputted by user. 

## Getting Started

To setup the script, you need to install the requirements, setup the environment variables and run the script.

### Installing
```bash
pip install -r requirements.txt
```

### Setup Environment Variables
1. Get your Telegram API Hash and API Id from [my.telegram.org](https://my.telegram.org/).
2. Create a `.env` file in the root directory of the project.
3. Add the following lines to the `.env` file.
```env
API_HASH=<your-api-hash>
API_ID=<your-api-id>
PHONE=<your-phone-number>
```

### Running the script
```cmd
python3 main.py
```

### Usage

The script will 

1. Ask you to select the chat from which you want to delete messages.
2. Ask you to enter the date upto which you want to delete messages.
3. Scan through the messages and get to the date you entered.
4. Begin deleting messages from the date you entered.

