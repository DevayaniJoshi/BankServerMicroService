from fastapi import FastAPI

app = FastAPI()

@app.post("/user/{username}/photo/{photoId}")
def root(username:str,photoId:int,size:int,type:str="jpeg"):
    
    return {f"message":f"The user name is {username} , the id is {photoId}, the {size}, and {type}"}
