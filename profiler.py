import os, sys, json
from flask import request


class profiler(object):
    def __init__(
        self,
        app,
    ):
        self.framelist = []

        @app.before_request
        def before():
            sys.settrace(self.profile)

        @app.after_request
        def after(response):
            sys.settrace(None)
            self.finish()
            return response

    def profile(self, frame, event, arg):
        self.framelist.append(
            {
                "func": frame.f_code.co_name,
                "file": frame.f_code.co_filename.replace(os.getcwd(), ""),
            }
        )

    def finish(self):
        with open("data.json", "w") as f:
            json.dump(self.framelist, f)
