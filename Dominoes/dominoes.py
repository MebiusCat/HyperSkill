from field import Field


def main():
    field = Field()
    field.generate(['Computer', 'Player'])
    field.display_header()

    # print(field.stock)
    # for player in field.players:
    #     print(player)
    # print(field)
    # field.next_player()

if __name__ == '__main__':
    main()
