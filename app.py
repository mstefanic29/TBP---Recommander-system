# https://www.geeksforgeeks.org/python-implementation-of-movie-recommender-system/

# importing module

from flask import Flask, render_template, request, jsonify
from sqlalchemy import false
app = Flask(__name__)
from pymongo import MongoClient
import pandas as pd
from bson.json_util import dumps

@app.route('/')
def index():
    client=MongoClient()
    client = MongoClient("mongodb://localhost:27017/")
    mydatabase = client["movies_system"]
    mycollection=mydatabase["Movies"]
    mycollection=mydatabase["Movies"]
    mycollection2=mydatabase["Ratings"]
    cursor=mycollection.find()
    cursor2=mycollection2.find()
    df =  pd.DataFrame(list(cursor))
    df2 = pd.DataFrame(list(cursor2))
    data = pd.merge(df, df2, on="movieId")
   
    index = data.groupby('title')['rating'].count().sort_values(ascending=False)
    index2 = pd.DataFrame(data.groupby('title')['rating'].mean()) 
    index3 = pd.DataFrame(index)
    print(index2)
    print(index3)
    index4 = pd.merge(index3,index2, on = 'title').head(25)
    print(index4.sort_values('rating_x', ascending=False))
    index4.rename(columns={" ": "Title", "rating_x": "Numbers of ratings", "rating_y": "Average rating"}, inplace=True)

  
  

    return render_template('app.html', data=index4.to_html())
    


@app.route("/autocomplete", methods=["POST"])
def autocomplete():
    print(request.form)
    # creation of MongoClient
    client=MongoClient()

    # Connect with the portnumber and host
    client = MongoClient("mongodb://localhost:27017/")

    # Access database
    mydatabase = client["movies_system"]

    # Access collection of the database
    mycollection=mydatabase["Movies"]

    cursor=mycollection.find({'title':{'$regex': request.form['q']}},{'title':1, "_id":0})
    data = (list(cursor))
    data = dumps(data)
    print(data)
    return data
    


@app.route('/program', methods=["POST"])
def program():
    # creation of MongoClient
    client=MongoClient()

    # Connect with the portnumber and host
    client = MongoClient("mongodb://localhost:27017/")

    # Access database
    mydatabase = client["movies_system"]

    # Access collection of the database
    mycollection=mydatabase["Movies"]
    mycollection2=mydatabase["Ratings"]
    mycollection3=mydatabase["Tags"]

    cursor=mycollection.find()
    cursor2=mycollection2.find()
    cursor3=mycollection3.find()

    df =  pd.DataFrame(list(cursor))
    df2 = pd.DataFrame(list(cursor2))
    df3 = pd.DataFrame(list(cursor3))


    film = request.form["movie"]

    #Merge movies and ratings
    data = pd.merge(df, df2, on="movieId")
    #print(data)

    #Calculate count of rating of all movies
    count = data.groupby('title')['rating'].count().sort_values(ascending=False)
    #print(count)

    ratings = pd.DataFrame(data.groupby('title')['rating'].mean()) 
    ratings['num of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count())
    #print(ratings)


    moviemat = data.pivot_table(index ='userId',
                columns ='title', values ='rating')
    
    
    ratings.sort_values('num of ratings', ascending = False)

    user_rating = moviemat[film]

    similarity = moviemat.corrwith(user_rating)


    corr_similarity = pd.DataFrame(similarity, columns =['Correlation'])
    corr_similarity.dropna(inplace = True)


    #corr_similarity.sort_values('Correlation', ascending = False)
    corr_similarity = corr_similarity.join(ratings['num of ratings'])

    #corr_similarity.head()
    
    r = corr_similarity[corr_similarity['num of ratings']>100].sort_values('Correlation', ascending = False)

    print(r)
    data = r.head(25).to_html()
    print(data)
    
    return render_template("rjesenje.html",data=data)
