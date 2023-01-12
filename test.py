import fastapi

app = fastapi.FastAPI()


@app.get("/")
def foo():
    res = fastapi.responses.RedirectResponse("/no")
    res.set_cookie("yo", "hahahaha")
    res.set_cookie("hm", "kek")
    return res


@app.get("/no")
def aoo(req: fastapi.Request):
    return req.cookies
