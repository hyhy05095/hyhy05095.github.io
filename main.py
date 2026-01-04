from flask import Flask, render_template, request #request에는 많은게 들어있음
from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web3_jobs
from extractors.wwr import extract_wwr_jobs


app = Flask("JobScrapper")


db = {
    
}


@app.route("/")  #syntatic sugar 간단해 보이지만 매우 복잡 def 바로위에 적어야함!!! 
def home():
    return render_template("home.html", name="nico")


@app.route("/search")
def search():
    keyword =request.args.get("keyword")
    if keyword in db:
        jobs = db[keyword]
    else:
       berlin = extract_berlin_jobs(keyword)
       web3 = extract_web3_jobs(keyword)
       wwr = extract_wwr_jobs(keyword)
       jobs = berlin + web3 + wwr
       db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)




# app.run("0.0.0.0")    #replit에서 작성했으면
if __name__ == "__main__":
    app.run(debug=True)


