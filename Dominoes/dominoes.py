from engine import Engine
from field import Field


def main():
    field = Field()
    field.generate([('Computer', True), ('Player', False)])

    engine = Engine(field)
    engine.play()


if __name__ == '__main__':
    main()