from official_accounts.views import index


def setup_routes(app):
    app.router.add_get("/wx", index)
