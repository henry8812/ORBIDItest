# ORBIDItest
ORBIDI technical test repository
# HubSpot-ClickUp Synchronization

This project provides an integration between HubSpot and ClickUp to synchronize HubSpot contacts as tasks in ClickUp. It allows you to keep contacts and their corresponding tasks updated in both platforms automatically.

## Prerequisites

Before getting started, make sure you have the following prerequisites installed in your development environment:

- Python 3.6 or above
- Pip (Python package manager)
- Git

## Installation

Follow the steps below to install and set up the project:

1. Clone this repository on your local machine:
git clone https://github.com/your_username/hubspot-clickup-synchronization.git

2. Navigate to the project directory:
cd hubspot-clickup-synchronization


3. Create and activate a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate


4. Install the project dependencies:
pip install -r requirements.txt


5. Copy the example environment variables file:
cp .env.example .env


6. Open the `.env` file and update the environment variables with your own HubSpot and ClickUp credentials.

7. Start the application:
uvicorn main:app --reload


8. The application will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Usage

Once you have configured the application, you can start using it to synchronize HubSpot contacts with ClickUp tasks.

1. Obtain the HubSpot contact ID you want to synchronize. You can retrieve it through the HubSpot API or from the HubSpot dashboard.

2. Send a POST request to `http://localhost:8000/contacts/sync` with the contact ID as a query parameter.

For example:
curl -X POST "http://localhost:8000/contacts/sync?contact_id=123456789"


Make sure to replace `123456789` with the actual contact ID.

3. The application will transform the contact data into a format compatible with ClickUp and create a corresponding task in ClickUp.

4. If the synchronization is successful, you will receive a response with the ClickUp task ID.

5. Verify in ClickUp that the task has been created correctly.

## Contribution

Contributions are welcome! If you find any issues or want to improve this project, feel free to open an issue or submit a pull request.

Before contributing, make sure to follow the development best practices and code style guidelines.

## License

This project is licensed under the [MIT License](LICENSE).




