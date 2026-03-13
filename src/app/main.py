from app.bootstrap.bootstrap import bootstrap, create_app

container = bootstrap(env="prod")
app = create_app(container=container)
