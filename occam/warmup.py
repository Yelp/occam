"""TODO(fhats): This is incredibly lazy, clean this up sometime"""
from occam.views import _collect
from occam.views import collect_everything


def warmup():
    _collect(collect_everything)


if __name__ == "__main__":
    warmup()
