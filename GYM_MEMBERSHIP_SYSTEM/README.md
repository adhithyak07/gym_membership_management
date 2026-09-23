# GYM MEMBERSHIP SYSTEM
The Gym Membership System is a Python-based application that helps gyms manage their members efficiently. It uses Supabase (PostgreSQL) as a cloud database to securely store member details, membership plans, and expiry dates.
# 🔹 Features

>Add new members with personal details and membership plans (Monthly, Quarterly, Yearly).

>View all members and track their membership status.

>Renew or upgrade memberships with automatic date calculation.

>Remove expired memberships from the system.

>Record payment history for each member.
# Project Structure

GYM MEMBERSHIP SYSTEM/
|
|--src/            # core application logic
|    |__logic.py   # Bussiness logic and task 
operations    
|    |__db.py      # Database operations
|
|----api/          # Backend API
|    |__main.py    # FastAPI endpoints
|
|---frontend/      #Frontend application
|     |__app.py    #Streamlit web interface
|
|___requirements.txt  # python Dependencies
|
|___README.md    #project Documentation
|
|___.env         # python variables

## Quick Start
 
### Prerequisites

-Python 3.8 or higher
-A Supabase account
-Git(Push,cloning)


### 1.clone or Download the project

# option 1: clone with Git
git clone <repository-url>

# option 2:Download and extract the Zip file

### 2.Install Dependencies

# Install all required python packages
pip install -r requirements.txt

### 3.Set up Supabase Databases 
 
1.Create a supabase Project:

2.Create the tasks table:
 
 -Go to sql editor in your supabase dashboard
 -Run this sql command:

 --sql 

create table gymrats (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  age int not null,
  phone text unique not null,
  plan text not null,       
  start_date date default current_date,
  end_date date not null
);



create table payments (
  id serial primary key,
  member_id uuid references gymrats(id),
  amount numeric not null,
  payment_date timestamp default now(),
  method text 
);

### 4.Configure environmental variables

1.Create a `.env` file in the project root
2.Add your supabase credentials to`.env`:
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here

**Example**
SUPABASE_URL=HTTPS://ABCDEFGHIJKLMNOP;
SUPAAdghijk..

### 5.Run the Application

## Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at`https://localhost:8501`

## FastAPI Backend

cd api
python main.py

The API will be available at `https://localhost:8000`

## How to Use

## Technical Details

### Technologies Used

-**Frontend**:Streamlit(Python web framework)
-**Backend**:FastAPI(python RESTAPI framework)
-**Database**:Supabase(PostgreSQL-based backend-as-a-service)
-**Language**:Python 3.8+

### Key Components

1. **`src/db.py`**:Database operations Handles all CRUD operations with supabase
2. **`src/logic.py`**:Bussiness logic task validation and processing

### Trouble shooting

## Common Issues

## Future Enhancements


## Support

If you encounter any issues or have questions:
contact 8341143782
mail:adhithyakodithala02@gmail.com