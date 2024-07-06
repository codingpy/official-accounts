from official_accounts.views import Handle


def setup_routes(app):
    app.router.add_view("/wx", Handle)
