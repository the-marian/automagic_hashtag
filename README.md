# automagic_hashtag
REST micro service that generates hashtags for photo. 

AutoMagic HashTag app provide a service that generates HashTags for Photos simply and fast by uploading it or sharing a URL
___
## Using
Let's take the URL  

`url=https://cdn-prod.medicalnewstoday.com/content/images/articles/324/324184/apple-cider-vinegar.jpg` [preview](https://cdn-prod.medicalnewstoday.com/content/images/articles/324/324184/apple-cider-vinegar.jpg)

Then just `curl -X GET "https://automagic-hashtag.herokuapp.com/api/?url=url&access_token=access_token" -H "accept: application/json"`

To get `access_token`, email me marian.zozulia@gmail.com with subject related to automagic_hashtag API credentials

An example response body will look like:

```
{
  "hash_tags": [
    {
      "score": 0.9639945030212402,
      "description": "Apple cider vinegar"
    },
    {
      "score": 0.941059947013855,
      "description": "Apple"
    },
    {
      "score": 0.9401142001152039,
      "description": "Natural foods"
    },
    {
      "score": 0.9273736476898193,
      "description": "Food"
    },
    {
      "score": 0.9123980402946472,
      "description": "Fruit"
    },
    {
      "score": 0.792801022529602,
      "description": "Plant"
    },
    {
      "score": 0.7708351612091064,
      "description": "Ingredient"
    },
    {
      "score": 0.6683749556541443,
      "description": "Apple juice"
    },
    {
      "score": 0.6292016506195068,
      "description": "Produce"
    },
    {
      "score": 0.5197820067405701,
      "description": "Liqueur"
    }
  ]
}
```

___
The applications on Heroku platform  “sleep” after 30 minutes of inactivity. After that a first access might be slow down.

Developed by using [FastAPI](https://fastapi.tiangolo.com) framework and Google Cloud [Vision](https://cloud.google.com/vision) API. Built for learning purposes (and fun!)
