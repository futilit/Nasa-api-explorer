import requests
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from datetime import date as Date

app=FastAPI()
app.get("/about")
def home():
    return {"message":"Hello NASA!"}
app.get("/planet/{planet_name}")
def get_planet(planet_name: str):
    return {
        "planet":planet_name,
        "message": f"you asked about {planet_name}"
    }

@app.get("/search")
def search(q: str):
    return{
        "Search Query :",q
    }
@app.get("/astronaut/{Name}")
def get_name(Name: str):
    return{
        "Name ": Name,
        "Message ":"Welcome {Name} to the nasa api exlorer"
    }

class Userquestion(BaseModel):
    Name:str
    question:str
    planet:str

@app.post("/ask")
def ask_question(data: Userquestion):
    return{
        "user":data.Name,
        "Planet":data.planet,
        "Question":data.question,
        "message":f"Tell me about {data.planet}"

    }
@app.get("/external-data")
def get_external_data():
    url="https://jsonplaceholder.typicode.com/todos/1"
    response=requests.get(url)
    print("Status :",response.status_code)
    print("Text:",response.text)
    data=response.json()
    status ="Pending"
    if (data["completed"]==False):
        print("status : Pending")
    elif (data["completed"]==True):
        print("status : Completed")
    else:
        print("Nothing")
    return {
        "Id":data["userId"],
        "Title":data["title"],
        "completed":status
    }
@app.get("/external/{todo_id}")
def get_todo(todo_id: int):
    url=f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    response=requests.get(url)
    print("Statu:",response.status_code)
    print("text:",response.text )
    data=response.json()
    if response.status_code !=200:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
    )

    return {
    "Id": data["id"],
    "Title": data["title"],
    "Completed": data["completed"]
    }
@app.get("/search")
def search(q: str):
    return {
        "query":q,
        "message":f"You searched for {q}"
    }
@app.get("/search")
def search(planet: str,year: int):
    return{
        "planet":planet,
        "year":year
    }
@app.get("/mission")
def mission(name: str,planet: str,year: int):
    return{
        "Name":name,
        "planet":planet,
        "Year":year
    }

@app.get("/asteroids")
def asteroids(date: str):
    try:
        Date.fromisoformat(date)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format.Please use YYYY-MM_DD"
        )
    
    url=f"https://api.nasa.gov/neo/rest/v1/feed?start_date={date}&end_date={date}&api_key=DEMO_KEY"
    response=requests.get(url)
    print("Status :",response.status_code)
    print("Text :",response.text)
    data=response.json()
    {"date":date}
    asteroids=data["near_earth_objects"][date]
    print(asteroids)
    first_asteroid=asteroids[0]
    print(first_asteroid)
    name=first_asteroid["name"]
    asteroid_list=[]
    for asteroid in asteroids:
        name=asteroid["name"]
        hazardous=asteroid["is_potentially_hazardous_asteroid"]
        diameter=asteroid["estimated_diameter"]["kilometers"]
        min_diameter=diameter["estimated_diameter_min"]
        max_diameter=diameter["estimated_diameter_max"]

        close_approach=asteroid["close_approach_data"][0]

        velocity=close_approach["relative_velocity"]["kilometers_per_hour"]
        miss_distance=close_approach["miss_distance"]["kilometers"]
        absolute_magnitude=asteroid["absolute_magnitude_h"]
        hazardus=asteroid["hazardous"]
        
    asteroid_info={
        "name":name,
        "hazardous":hazardous,
        "min_diameter":min_diameter,
        "max_diameter":max_diameter,
        "velocity":velocity,
        "miss_distance":miss_distance,
        "absolute_magnitude":absolute_magnitude


    }
    asteroid_list.append(asteroid_info)

    if hazardous is True:
        hazardous_status+=1

    return{
        "date":date,
        "asteroid_count":len(asteroids),
        "asteroids":asteroid_list
    }

print("SUMMARY ROUTE STARTED")
@app.get("/asteroids/summary")
def asteroid_summary(date: str):
    url=(
        f"https://api.nasa.gov/neo/rest/v1/feed"
        f"?start_date={date}&end_date={date}&api_key=DEMO_KEY"
    )

    response=requests.get(url)
    print("Nasa URL:",url)
    print("NASA Status:",response.status_code)
    print("NASA Response:",response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="NASA API request failed"
        )

    data=response.json()
    asteroids=data["near_earth_objects"][date]

    largest_asteroid=max(
        asteroids,
        key=lambda asteroid: asteroid["estimated_diameter"]["kilometers"]
        ["estimated_diameter_max"]
    )

    fastest_asteroid=max(
        asteroids,
        key=lambda asteroid: float(
            asteroid["close_approach_data"][0]
            ["relative_velocity"]["kilometers_per_hour"]

        )
    )

    hazardous_asteroid=[
        asteroid
        for asteroid in asteroids
        if asteroid["is_potentially_hazardous_asteroid"] is True
    ]

    return {
        "date":date,
        "total_asteroids":len(asteroids),
        "hazardous_asteroids":len(hazardous_asteroid),
        "largest_asteroid":largest_asteroid["name"],
        "largest_diameter_km":largest_asteroid[
            "estimated_diameter"
        ]["kilometers"]["estimated_diameter_max"],
        "fastest_asteroid":fastest_asteroid["name"],
        "fastest_velocity_km_per_hour":fastest_asteroid[
            "close_approach_data"
        ][0]["relative_velocity"]["kilometers_per_hour"]
    }


    